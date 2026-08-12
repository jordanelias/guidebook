# Wave 7 — Consolidation

**Read `00-holistic-execution-plan.md` first.** **Precondition: L1 exists.**

**Almost every item here is OWNER-GATED**, because retirement and file moves are guardrail 4.
**Retire to `_archived/` mirroring the origin path — never delete. Redirect-stub anything still
referenced.**

**The surviving test for a fold: it must not destroy a key, and identical column shape is not
identical meaning.**

**Hard ordering:** all of Wave 8 → W7.13 → W7.12. And three sequencing dependencies **no prior
document states**, found by this decomposition:

1. **W7.7's audit rewrite must follow W7.3-G1** — the banner audit reads `bpc_metadata`, which
   G1 folds away.
2. **W7.3-G5's retire ruling should precede W7.4** — the `FrozenGridError` guard lives *in*
   `db.py`, so the DELETE branch removes the frozen grid's only write-time protection.
3. **W9.5 depends on W7.4-ADOPT** — `db.py log-search` is the admission discipline a PMP walk
   needs.

**The archived corpus is directly queryable** at `_archived/data/corpus-pre-reset-2026-08-06.db`
(read-only URI). Every "archived rows" figure below was re-run against it — no branch fetch
needed.

---

## W7.1 — Retire the one-shot importer layer · **OWNER**

**Corrected scope: 20 files / 7,086 lines, not 19 / 6,074.** The 19 `.py` files sum to exactly
6,074 lines — confirmed — but the retirement act must also move
`scripts/migrations/session_2026_05_11g_data.json` (1,012 lines), the dump the replay script
reads. The plan flags the 20th file in Wave 1 and never absorbs it into W7.1 or the net.

**Two prior owner holds must be discharged in the same ruling:**
1. `scripts/migrate/_legacy_guard.py:29-36` records that commit `366766ee` **deliberately kept**
   these files because six are named in `architecture/sqlite-data-layer.md` §9's build table —
   *"archiving them would silently falsify a spec document."* The DR must amend that spec or
   license the falsification.
2. `governance/check-registry.yaml:1195-1205` holds an **open owner question** — *"fund the
   dataset, or retire the check and its generator together"* — where the generator is
   `scripts/convert/version_retrofit.py`. **Retiring it executes one branch of an unruled
   question.**

**The move:** `scripts/convert/*.py` (13) → `_archived/scripts/convert/` · `scripts/db/`
(3: `enrich_all_c_stage.py` 539, `init_db.py` 432, `migrate_all.py` 1362) →
`_archived/scripts/db/` · `scripts/migrate/{init_database.py 417, phase_jv_appendix_a.py 431}` ·
`scripts/migrations/session_2026_05_11g_{replay.py 224, data.json 1012}`.

**The caller sweep is real but severely undercounted.** All five plan entries confirmed
(`check-registry.yaml:1202`, `schema_reference_drift_audit.py:18` — also `:22,:35,:63`,
`db_path_env_audit.py:23-24`, `CLAUDE.md:253` — also `:449`, `_legacy_guard.py:23-36`), **plus
~10 more live surfaces the plan never enumerates:** `governance/context-map.yaml:587`
(regenerate) · `governance/retired-vocabulary.yaml:112,291,382,413,447,478,513` ·
`governance/concurrent-write-architecture-proposal-2026-05-11.md:22,29,30,81,113` ·
`governance/time-model.md:202` (§7 is *titled* for `version_retrofit.py`) ·
`governance/evidence-methodology.md:494` · `governance/repo-strategy-revision-co.md:14` ·
`architecture/schema-spec.md:572` · `architecture/schema-reconciliation.md:308` ·
`references/project-standards.md:488,626` (append-only — add a clarifying RULE, do not edit) ·
`skills/cell-curator_SKILL.md:21` · `schemas/directness.py:31`.
**Forward-only, `deliberately_not_swept`:** four DRs, `decision_register.yaml:2194`, two
migrations, one data migration.

**Falsifier:** an *executable* caller outside `_archived/`. None exists — no live `.py` imports or
subprocess-invokes any of the 20.

---

## W7.2 — Merge eight of the ten single-invariant audits

**Sequenced after W7.4.** **Owner-gated after all** — the eight source files are retired to
`_archived/`, which the plan's "Gate:" column omits (the same defect it caught in W7.1).

**The ten, re-verified (`wc -l`): 1,357 lines total.** `matrix_consistency` 58 ·
`table_connectivity` 82 · `metadata_integrity_audit` 114 · `pre_rehab_banner_audit` 123 ·
`source_slug_links_duplicates` 154 · `alias_provenance_audit` 156 ·
`population_integrity_audit` 157 · `reasoning_doc_citations_audit` 169 · `db_path_env_audit` 171
· `workplan_naming_audit` 173. **The two quarantined stay as files**: `table_connectivity` and
`pre_rehab_banner_audit`.

**Interface:** `scripts/audit/invariants.py --check <id>`, ids **identical to today's registry
ids** so every registry note stays true. `--list` prints ids + one-line invariant. Exit codes and
stdout preserved verbatim per check (several print counts Wave-L I4 depends on). Unknown id →
exit 2. One `CHECKS: dict[str, Callable]`; each former file becomes one function keeping its
docstring; the shared scaffold hoisted once — that hoist *is* the ~150-line saving.

**The dispatch pattern already exists: 27 of 65 active entries carry arguments beyond the script
path** — confirmed by YAML parse. Mechanism: `run_checks.py:205-206` (`expand()` substitutes
`@SESSION@`) and `:245-247` (verbatim `subprocess.run`).

**Risk:** `db_path_env_audit` audits *other scripts'* env-var honouring by AST over `scripts/**`.
After the merge it must not flag `invariants.py` itself, and its exemption bookkeeping
(`assess_cell.py`, `graph_audit.py`) must move across intact.

**Falsifier:** any of the eight behaves differently under the dispatcher, **or the merged file
exceeds ~1,200 lines** — the `db.py`-shape alarm the plan set.

---

## W7.3 — Folds G1–G4 · **G2 needs a DR amendment**

| Fold | Tables | Live / archived rows |
|---|---|---|
| G1 | `bpc_metadata` → `slugs` (1:1 on PK `slug`) | 0 / **83** |
| G2 | `citation_mining` → `source_slug_links` | 0 / **183**; target 0 / **1,011** |
| G3 | `access_duration` + `access_stakes` + `life_stage_modifiers` → `vocabulary(kind, code, …)` | **3/3/2 live** |
| G4 | `case_study_outcomes` + `case_study_strategies` → one child table | **0/0 — the only fold empty in both** |

**"DDL only, all empty" is false for four of five — confirmed.**
**No inbound FKs to any fold target — confirmed by full FK-graph enumeration over all 67 tables.**

**G2's gate.** `citation_mining` is one of the seven `CORE_INVARIANTS` of the **blocking**
`migration_reproducibility` gate — `scripts/audit/migration_reproducibility.py:55-63`, whose
comment at `:54` states *"Keep this list and the DR in sync; it is the contract."* The DR is
**`DR-2026-05-28-migration-ledger-and-reproducibility-reconciliation.md`**. Folding without
amending it silently breaks a blocking gate's contract. Note `source_slug_links` is *also* in
`CORE_INVARIANTS` — numerically invisible at 0+0 rows, but the contract text must still move.

**G3 is one schema migration plus one 8-row data migration.** **G1 widens `slugs`, the frame's
anchor table** — keep the DR-2026-08-06 frame enumeration in sync.

**Sweep note:** `CLAUDE.md:74` tells sessions to "query `bpc_metadata`/`evidence_cell_state`" —
**must be re-pointed after G1.**

---

## W7.3-G5 — `search_coverage` / `search_languages`: **retire, don't fold**

**Frozen by design, not fold candidates.** `scripts/db.py:316-325` defines
`upsert_search_coverage()` and `upsert_search_language()` whose only body is
`raise FrozenGridError(...)`. The live mechanism is `search_executions` + the `v_coverage_*`
views. Live 0 / archived **4,960** and **1,558**.

**Folding two superseded frozen tables into a new frozen table is motion without progress.**
Recommend routing them into W7.9's cut ruling.

**The dependency inversion:** the freeze *lives in* `db.py`. If W7.4's DELETE branch is taken,
the `FrozenGridError` refusal disappears and these tables lose their only write-time guard.
**Rule G5 before, or alongside, W7.4.**

**Risk worth stating:** `search_executions` is itself 0 rows, so the "live mechanism" is dormant.
Retiring the frozen grid is safe, but the coverage story then rests entirely on unexercised code.

---

## W7.4 — Resolve `scripts/db.py` · **OWNER. Recommend ADOPT.**

**1,889 lines, 43 top-level functions (AST), zero importers, zero subprocess callers** —
confirmed twice. The only textual references from code are its own docstring, a comment at
`validate_db.py:112` (itself quarantined-broken), and a printed instruction string at
`item_audit_pipeline.py:405`.

### ADOPT
1. A short D-OP DR recording adoption as the sanctioned read/query path.
2. Wire the two Wave-1 injection seams — W1.4's `next_gap_id(conn=None)`, and the walk/probe
   harness seam.
3. Keep the H05/H07 write-time enforcement and the `FrozenGridError` refusals — they become live
   guards the moment anything imports the module.
4. **Add one registered advisory smoke check** exercising `db.py --help` plus one read
   subcommand, so "zero callers" can never silently recur. That is W6.7's lesson applied to the
   fix itself.
5. No caller sweep needed — nothing breaks because nothing called it.

### DELETE — **more expensive than any document recorded**
1. **It strands an ADOPTED decision.** `DR-2026-08-06-clean-room-evidence-reset.md:104-105` names
   the resumption discipline as *"the logged-search discipline (`db.py log-search`)"*.
2. **The plan's 12-file sweep is refuted. The real sweep is ~29 live files:** **26
   `skills/*_SKILL.md`** invoke `scripts/db.py` subcommands — audit-consolidator,
   bibliography-compiler, citation-miner, connection-auditor, connection-discovery,
   content-gap-analyzer, cross-population-conflict-mapper, economics-auditor,
   economics-researcher, evidence-auditor, find-and-replace, functional-deficit-auditor,
   functional-deficit-researcher, gap-driven-mining, github-io, guidebook-auditor,
   item-audit-pipeline, literature-review-planner, multilingual-research, research-log-manager,
   sensory-coherence-checker, structure-auditor, supersession-audit, supplemental-integrator,
   toc-editor, workplan-orchestrator — **plus `CLAUDE.md:39,112,169`** and
   `item_audit_pipeline.py:405`. Skills are **governed identifiers**; a rename is a governed
   event.
3. Re-home `next_gap_id` before the file moves — W1.4 needs it either way.

**The 26-skill surface is the strongest argument for ADOPT.** The plan's 12-file sweep would
have left ~17 files instructing sessions to run a tool that no longer exists.

---

## W7.5 — `governance/frozen-surfaces.yaml` · **OWNER**

`.ignore:47-49` gates itself: *"Changing this file is OWNER-GATED, same as a retirement."*

**Schema:** `surfaces[]` with `path`, `classes: [search_hidden, reference_only]`, `reason`,
`negations` (e.g. `sessions/**` carries `!sessions/LATEST`, `!sessions/LATEST-RESEARCH`),
`adjudicated_by`. Plus a `citation_semantics:` block carrying **cited-as-of-date semantics, not a
resolution guarantee**.

**Two generators**, both `--check`-capable on the `context_map_fresh` pattern. Preserve
`.ignore`'s header prose verbatim — the `**`-negation syntax note at `:41-45` was *tested*.
`validate_cross_refs.py:245-254` hardcodes 8 `REFERENCE_ONLY` prefixes (`parts/`,
`references/bpc/`, `references/bpc-reasoning/`, `references/connections/`,
`references/connection-reasoning/`, `specs/`, `site/`, `_archived/`) with a *"SCOPE statement, not
an amnesty"* comment at `:241-244` — better to read the YAML at runtime than regenerate a tuple.

**The two lists intersect only at `_archived/`** — the `classes:` field is what lets one file
serve two deliberately different scopes without merging them.

**The REF/GAP citation figures, re-derived precisely — the plan states them two different ways
and neither is complete:**

| | REF-IDs | GAP-IDs |
|---|---|---|
| `decisions/` | **81** | **28** |
| `attestations/` | **42** | **27** |
| union | **117** (110 resolve in the archive, **0 live**) | **40** |

Write the YAML from that four-cell table.

---

## W7.6 — Retire `references/global-reference-registry.{md,json}` · **OWNER**

**The two authority sentences, verbatim at HEAD:**
- Line 6: *"**Purpose:** Single source of truth for all references cited anywhere in the
  guidebook…"*
- Line 601 (the file's last line): *"**Authority:** This registry is the single source of truth.
  If a BPC Key sources table and this registry conflict, the registry governs."*

**These contradict CLAUDE.md §2 outright, and they go regardless of where the file lives.**

**ID figures re-derived:** 531 distinct REF-IDs — confirmed. **0 live** — confirmed
(`evidence_sources` is empty). **496 resolve in the archived corpus** — confirmed against its 863
rows. **35 never existed in any database** — confirmed (531 − 496).
**"367 missing" is NOT REPRODUCIBLE.** No natural reading matches; the metadata classes are 56
COMPLETE / 16 PMID-ONLY / 64 GREY / 395 AUTHOR-TITLE-ONLY. **Do not propagate the figure** —
trace its origin first or drop it.

**Sequencing:** run W7.1 first and two of the seven callers (`convert_sources.py:6,97,293,313`,
`db/migrate_all.py:841-842`) vanish with it. Live callers remaining:
`governance/conceptual-model.md:107`, `references/citation-tagging-protocol.md:9,17,100`,
`references/phase-b-handoff.md:229,250`, `references/claim-reference-join.md:162`,
`working/evidence-migration/registry-reconciliation.md:6` — **plus two the plan omits**:
`DR-2026-07-12-evidence-architecture-unification.md` and its impact appendix (forward-only).

The redirect stub must **invert** the two authority sentences, not merely point elsewhere.

---

## W7.7 — One banner on all per-slug BPC files · **OWNER**

**86 per-slug files — confirmed.** 85 in topic subdirectories plus
`references/bpc/thermoregulation-built-environment.md` sitting flat in the root. (17 `.md` sit
flat there; the other 16 are population archives, `index.md`, `_template.md` — a different class.)

**The silent exemption, confirmed at `scripts/validate_bpc.py:79-86`** (the `is_frozen_flat`
assignment spans `:83-86`, not the cited `:79-85`): any file whose dirname is exactly
`references/bpc` is exempted from Metadata and Key-sources checks as a *"pre-CO-0006 frozen flat
archive"* — **which wrongly captures a full synthesis file.**
**Fix by list, not by location** — exempt the 16 known flat archives explicitly, or move the file
into its topic subdirectory (an owner-gated move).

**`pre_rehab_banner_audit` is RED on 68, not 6 — confirmed by running it.** Exit 1, *"Invariant
2: cohort slugs without DB banner state (68)"*, *"DB slugs in RETRACTED-PRE-REHAB: 0"*. The reset
emptied `bpc_metadata` underneath its DB-side invariants. **The quarantine note still names six
specific slugs and is stale.**

**16 per-slug files carry no banner** (86 census − 70 bannered, from the audit's own cohort
count). Enumerate by diffing, and **regenerate the dossier rather than trusting it.**

**Sequencing (new):** the audit rewrite must follow **W7.3-G1**, or `db_state()` breaks entirely
when `bpc_metadata` folds away. Invariant 2 cannot go green while `bpc_metadata` = 0 rows by
ratified reset — the quarantine reason should say *that*.

---

## W7.8 — Generate `workplan/INDEX.md` · no gate

**Baseline re-derived: 75 top-level `.md` / 32,411 lines** — the plan's "74 / 31,338" **went
stale within a day**, which is the strongest possible argument for the item it sits in.
`workplan/deprecated/` = 16 `.md` (outside `.ignore`); `_superseded/` = 20 `.md` (inside).

**Generator** `scripts/generate/workplan_index.py`, beside `context_map.py`. Deterministic, pure
function of the filesystem, **no HEAD sha** — `context_map_fresh`'s own note records that
recording HEAD makes the check permanently red.

**Columns:** file · date · status (`pre-reset`/`post-reset`/`superseded`/`deprecated`/`stub`) ·
wave ids · register ids · lines · supersedes/superseded_by (from W8.7's banners).

**Freshness check** `workplan_index_fresh`, modelled exactly on `context_map_fresh`
(`level: advisory`, `min_items: 1`, battery `render`): `--check` regenerates to memory and diffs,
exit 1 on drift.

**Risk:** the index is itself a workplan file — exclude it from its own census.

---

## W7.9 — Cut `situations` and `external_root_registry` · **OWNER, LAST**

**Both 0 rows live AND archived — confirmed.**

**Correction: three views break, not one.** `v_root_id_conflicts` queries only
`source_value_extractions` and **survives** — confirmed. But **`v_value_independence`,
`v_registry_duplicate_descriptions` and `v_unregistered_roots`** all reference
`external_root_registry`. **The plan names only the first; the third appears in no document at
all.** That under-sweep is itself the finding.

**Two exposures:**
- **D-METH** — `v_value_independence` is the pipeline contract's cited H1 mechanism. Its
  `root_id IN (SELECT root_id FROM external_root_registry)` arm admits non-REF roots. The ruling
  is whether post-cut independence counts on `root_ref_id` alone (rewrite) or the view retires
  with the table (and the contract's H1 citation is amended).
- **DG-NON** — `situations` is the native Co-1 entity. **Correction: four governance documents
  name the entity**, not five: `governance/functional-taxonomy.md:97,112,324,412` (§5.4, *"never
  subordinated"*), `governance/held-tensions.md:155,345,358,363,382`,
  `decisions/RATIFICATION-RECORD-2026-07-21.md:32`, and generated `context-map.yaml`.
  **`armature_v4_resolutions.md:587` is generic prose ("situations where…"), not the entity** —
  do not count it.

Take W5.5's wire-or-retire ruling on the 11 unread views in the same sitting.

---

## W7.10 — `disposition:` and `exit_condition:` on the quarantine schema · no gate

**Sequenced after W0.1** (membership 15 → 14 quarantined).

**Ground truth confirmed exactly:** 16 entries — **15 `status: quarantined`**
(`table_connectivity`, `validate_db`, `validate_item`, `validate_conflict`, **`validate_conflicts`**,
`schema_reference_drift_audit`, `adjudication_integrity`, `code_currency_audit`,
`pre_rehab_banner_audit`, `jurisdictional_divergence`, `full_db_metadata_verification`,
`contamination_sampler`, `check_phase_a_complete`, `validate_commits`, `validate_audit_runs`)
**plus one `status: vacuous`** — `validate_temporal` at `:1184-1186`. **`validate_conflicts`, the
live plural validator, is quarantined** — confirming AC-25 against sweep §1.7a.

**Schema:** `disposition:` ∈ {`not-a-gate`, `vacuous`, `red-with-findings`, `wrong-venue`},
mandatory; `exit_condition:` mandatory when disposition ∈ {`vacuous`, `red-with-findings`}.
Normalise `validate_temporal` to `status: quarantined` + `disposition: vacuous`.

**`--selftest` assertion** beside C1b (`run_checks.py:520`): every entry has a valid
`disposition`; every promotable one has a non-empty `exit_condition`; **and the entry key-set is
exactly `{id, cmd, status, reason, disposition, exit_condition?}`** — per W1's R-12 lesson, a
successfully-parsing wrong shape is otherwise invisible.

---

## W7.11 — The two unregistered surfaces · **OWNER**

`references/methodology/` = **10 files**. `working/` = **39 files, 1.1 MB** — confirmed.
**REF-ID resolution over `working/`: 188 distinct, 0 live, 173 resolve in the archive, 15 in
neither** — confirmed exactly.

**The containment percentages (98/91/93/85) are CARRIED, not re-derived** — the plan states no
derivation recipe (which target files, which metric). **Recover the recipe from the sweep
document before trusting them**, per W6.6.

**Per-class proposal:** methodology's `throughline-*` and economics files → frozen-reference ·
`working/evidence-migration/**` → frozen (92% of its REF-IDs are pre-reset) ·
`working/taxonomy/staged_schema_functional_axes.sql` → **live**, it is doctrine-named ·
`working/pilot/**` → frozen (cited by DR-2026-07-12, forward-only).

**Trap:** `working/evidence-migration/db/migrations/0001-jurisdiction-hygiene.sql` looks like a
migration but sits outside `scripts/migrations/`. **Classify it explicitly so nobody replays it.**

Whatever is ruled frozen enters `frozen-surfaces.yaml` (W7.5) — **not a new mechanism**
(guardrail 3).

---

## W7.12 — Seven documents to four · **OWNER. W8 FIRST — NON-NEGOTIABLE.**

**Keep:** `2026-08-12-resolution-plan.md`, `2026-08-11-consolidated-review-and-plan.md`,
`2026-08-11-consolidation-sweep-and-adversarial-pass.md`,
`2026-08-11-per-stage-table-anatomy.md`.
**Retire (after W8 ports):** `2026-08-11-reconciled-findings-register.md`,
`2026-08-11-pr93-reconciliation-and-shared-code.md`, `2026-08-11-fold-or-cut-ledger.md`.
*(W8.3 offers the ledger a keep-as-fifth-with-banner alternative — owner's call, and it changes
the net.)*

Each retirement is `git mv` to `_archived/workplan/` **plus a redirect stub at the origin path**
naming where the content went, where the full text lives, and where the loss-audit is.

**File count rises, it does not fall** — 75 → 76 under retire-with-stub (3 stubs + `INDEX.md`).
Only lines fall, by ~880. The plan's "74 → 75" was computed against the stale baseline;
recompute at execution.

**Port-completeness check:** diff each retiree's finding-IDs against the keepers'. A unique
finding with no ported home is the defect this wave exists to prevent.

---

## W7.13 — Rename the consolidated review's Class IDs to `RR-` · no gate

**`RR-` confirmed free repo-wide.** Occurrences to rename in
`workplan/2026-08-11-consolidated-review-and-plan.md`: definition rows **`:179-186`** (C1–C8) and
back-references at **`:243`** (C2) and **`:397`** (C1, with E7).

**Exclusion confirmed: `:182`'s evidence cell reads "rem C1"** — that is the *remediation
register's* C1, cited as provenance. **Do not rename it.**

**Also out of scope:** the resolution plan's `:470` "current C1–C7" (those are `run_checks.py`
selftest check-names — **a fifth C-series, living in code**), the remediation register's C1–C13,
the locator probes' C1–C17, and `pmp_audit.py`'s C1–C5 flags.

**G1–G5 remain out of scope — confirmed cited externally** at `per-stage-table-anatomy.md:92,250`
and throughout the resolution plan, so the "cited nowhere" premise fails for them.

---

## W7.14 — The stage-tables artifact: **re-derive, don't preserve** · no gate

**`git log --all --diff-filter=A -- '*stages.json'` returns nothing — confirmed.** The artifacts
were never committed on any ref, and the authoring session's container is gone.

**Source:** `workplan/2026-08-11-remediation-and-pipeline-anatomy.md`, **512,173 bytes**, whose
**Part 2 spans lines 1203–6641** (Part 3 begins `:6642`). **Read Part 2 only, by offset — never
the whole file.**

Write `scripts/generate/pipeline_stage_tables.py` emitting
`references/pipeline-stage-tables.json` with `derived_from:
"…remediation-and-pipeline-anatomy.md Part 2 @ <commit>"` in its header — **because this is a new
extraction, not a preservation.**

**Cross-check against W8.6's corrections before committing** — the unwritable-output count is
**14, not 13**, and the five→eight propagation at `:81`, `:166`, `:246` is uncorrected in the
source. **Do not bake the source's known errors into the JSON.**

**Standing lesson for `project-standards.md`:** evidence that lives only in a session container
is not preserved by naming it in a workplan.

---

## Re-derivation notes — the corrections this wave adds

| Claim | Status |
|---|---|
| W7.1 = 19 files / 6,074 lines | **REVISED — 20 files / 7,086 lines** with the JSON dump |
| W7.1's caller sweep = 5 entries | **REVISED — ~15 live surfaces + ~9 forward-only** |
| W7.2's ten scripts / 1,357 lines; "27 of 65" | **CONFIRMED exactly** |
| W7.3: four of five folds non-empty in the archive; no inbound FKs | **CONFIRMED** |
| `citation_mining` in a blocking gate's `CORE_INVARIANTS` | **CONFIRMED** — `migration_reproducibility.py:55-63`, DR-2026-05-28 |
| `db.py` 1,889 lines / 43 functions / zero importers | **CONFIRMED** |
| W7.4 DELETE = 12-file sweep | **REFUTED — ~29 files, 26 of them skills** |
| W7.5 REF/GAP counts | **REVISED — decisions 81/28, attestations 42/27; union 117 REF (110 archived, 0 live), 40 GAP** |
| W7.6: 531 ids, 0 live, 496 archived, 35 never existed | **CONFIRMED** |
| W7.6: "367 missing" | **NOT REPRODUCIBLE — do not propagate** |
| W7.7: 86 files; silent exemption; RED on 68 | **CONFIRMED** (exemption spans `:79-86`) |
| W7.8: 74 files / 31,338 lines | **REFUTED — 75 / 32,411** |
| W7.9: one view breaks | **REVISED — three break**; `v_root_id_conflicts` survives |
| W7.9: five governance documents name `situations` | **REVISED — four**; the armature hit is prose |
| W7.10: 15 quarantined + 1 vacuous; `validate_conflicts` quarantined | **CONFIRMED** |
| W7.11: 39 files, 188/173/0/15 REF-IDs | **CONFIRMED**; containment percentages **CARRIED** |
| W7.13: `RR-` free; `:182` exclusion | **CONFIRMED** |
| W7.14: artifacts never existed; source ~512 KB | **CONFIRMED**; Part 2 = `:1203-6641` |
