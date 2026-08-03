# Prune-and-reinvest plan — cutting the apparatus down to what enforces the pipeline

**Date:** 2026-08-02 · **Status:** PROPOSED · **Supersedes:** Step 6 of
`workplan/consolidation-and-compliance-plan-2026-08-01.md` ("revisit the tool question later")

Four independent read-only audits, run 2026-08-02, measured the whole enforcement substrate by
execution: all 58 registry checks (each mutation-tested), all 159 Python files, the DB's 63 tables
and every handshake between them, and the hooks/CI/workflow layer. Every number below came from a
command that was run. Nothing here is transcribed from prose.

---

## 1. The criterion

The owner's test, restated so it can be applied file by file:

> An enforcement artifact earns its place if it either
> **(A)** catches a row-level violation in a real table, or
> **(B)** makes session N+1 start on the same guardrails session N ended on.
> **Disqualifier, applying to both:** it must be able to fire, and someone must read it when it does.
> Enforcement whose subject is the enforcement apparatus itself fails both limbs.

Limb A is the pipeline: topics → sources → evidence → synthesis → specifications → site.
Limb B is process continuity: how to commit, where work stands, what is queued, what was decided.
Both are legitimate. Neither justifies an artifact that cannot fail.

---

## 2. What the audits found, corrected

Two working assumptions were wrong and are corrected here so the plan is not built on them.

**Wrong assumption 1: "most checks are paperwork."** Derived from the `basis:` field, which records
what a check *declares*, not what it *does*. Measured by actual subject: **35 of 58 checks are
pipeline-substantive, 23 are paperwork** — roughly 59:41 in the pipeline's favour.

**Wrong assumption 2: "the registry is the fat."** It is the healthiest component. Under adversarial
mutation — corrupt the target, confirm the check goes red — **48 of 58 are KEEP-AS-IS**. Only 2 are
genuine prunes.

The real findings:

| Finding | Measured |
|---|---|
| Blocking gates structurally incapable of exiting 1 | **3** |
| Registry checks that are vacuous | **2** |
| Unregistered Python files, of 159 total | **90** |
| Of those, archivable | **64** |
| `main` branch-protected? | **No** (API-verified) → 30 "blocking" controls are advisory in fact |
| Pipeline-contract criteria with no check | **6 of 19** |
| Continuity pointers stale | `sessions/LATEST` 7 weeks · `handoff-next-session.md` 11 weeks |
| Sources with no topic link | **65 of 863** |
| Sources with no extraction row | **856 of 863** — and indistinguishable from "nothing to extract" |
| Rival evidence tables serving target role (c) | **5**, totalling 167 rows against 863 sources |
| Spec pages rendering an empty best-practice banner | **79 of 87** |
| Distinct REF-ids appearing across the whole site | **1** |

The teeth are inverted. Of 27 blocking checks, 18 are pipeline and 9 paperwork — but the *deep*
pipeline QC is systematically soft: the entire `research` battery is advisory except its own
selftest, `migration_reproducibility_deep` is advisory while the blocking version compares 7 scalars,
and `adjudication_integrity` (274 tier inconsistencies) is quarantined. The R1–R15 contract — the one
declaring research invalid without compliance — has **zero blocking enforcement anywhere.**

---

## 3. PRUNE

### 3.1 Registry checks — 2 out, 1 merged, 3 demoted

| Check | Action | Why |
|---|---|---|
| `validate_population` | **PRUNE** | Vacuous. Scans `references/{bpc,search-log,connections}` for YAML-frontmatter population codes (BPC uses HTML comments — there are none) and `data/specifications` (does not exist). Prints "No files … to validate", exits 0. DB-side population invariants are already covered by `population_integrity_audit` + `test_db_integrity` A02/A03 + `validate_axes`. |
| `validate_temporal` | **PRUNE** | Vacuous. Loads `data/temporal/**` and `data/sources/*.yaml`; neither exists. Reports "0 rules, 0 standards, 0 versions, 0 supersedence links" and passes. T-09 ("launch_phase singleton required") returns pass *because* the directory is absent. |
| `citation_mining_backlog_t2` | **MERGE** into `_t3` | Same script, tier scope 1–2 ⊂ 1–3. Its 168 outstanding rows are a strict subset of t3's 467. Two copies of one report. |
| `citation_mining_backlog_t3` | **DEMOTE** to report | A 467-row work queue, not an invariant. |
| `attestation_verdict` | **DEMOTE** | Informational by design; keep out of the gate set. |
| `test_jurisdictional_divergence` | **DEMOTE** | Green, but its subject script is quarantined. Rot insurance only; never promote. |

Removing the two prunes breaks nothing executable. Each needs one prose line corrected:
`references/project-standards.md` RULE A7/A9, `governance/population-taxonomy.md` §4.1,
`governance/time-model.md` §6, `references/tooling-register.md`. Re-register `validate_temporal` if
`data/temporal/` ever lands.

### 3.2 Scripts — 64 files to `_archived/`, in four waves

House rule holds: **retire to `_archived/` mirroring the origin path; never delete.** References in
`sessions/`, `decisions/`, `audits/`, and `workplan/` are historical records that describe what was
true then and must not be rewritten to tidy a filename.

| Wave | Count | Contents | Risk |
|---|---|---|---|
| **1** | 21 | `probes/generate_*` (5, read `/tmp/*.json` inputs that no longer exist), `probes/probe_ato_author_year_search`, `probes/probe_ato_no_identifier_title_search`, `probes/probe_multi_source_recovery`, `probes/recover_truncated_dois`, `probes/validate_correction_dry_run`, `scripts/test/test_co0009_pipeline.py`, `convert/{__init__,convert_economics,convert_fdr,convert_items,convert_throughlines}`, `db/{apply_connections_batch1,enrich_measurements_batch1,enrich_measurements_batch2}`, `migrate/{phase_01_slugs,phase_02_populations}` | **Zero** — caller sweep across the whole repo including `.github/`, `.claude/`, `governance/`, `references/`, `skills/` returned nothing |
| **2** | 37 | remaining `convert/` (13), remaining `migrate/` (7), `migrations/*.py` (4 — **leave the sibling `.sql` ledger untouched**), `probes/probe_ato_verified_{doi,pmid}`, `db/` (6), `tag_de_claims`, `tag_fg_claims`, `verify_resolved_dois`, `migrate_evidence_sources_v2`, `reconcile_ledger_dr_2026_05_28` | Zero mechanically; historical references only |
| **3** | 2 | `db/migrate_all.py`, `migrate/migrate_items.py` | **Caller fix first** — see §4.2 |
| **4** | 4 | `generate/room_page.py`, `tests/test_adjudication_integrity.py`, `tests/test_generate_parts_4_2.py`, `probes/citation_mining_pipeline.py` | **Owner decision** — see §6 |

Waves 1–2 (58 files) are the bulk and carry no risk. They are one-shot converters and migrators from
the April–May 2026 YAML→SQLite transition, superseded by baseline migration `012`; their output
directories (`data/items`, `data/populations`, …) no longer exist.

### 3.3 Never-fail compute

The `tests` CI job is **9 of 9 advisory** — 21 seconds of enforcement-shaped compute per run with no
failure state. Either promote the checks that deserve teeth (§5.2) or move the job to a schedule.

---

## 4. REPAIR

### 4.1 The three gates that cannot fire *(highest priority — these are the owner's criterion exactly)*

| Gate | Defect, proven by mutation | Fix |
|---|---|---|
| `doctrine_recheck` — **blocking** | Registered with `--cross-ref`, which runs only pass 2.3, whose findings are all WARNING; exit 1 requires ERROR. Deleting a CANONICAL governance doc → **exit 0** with the flag, exit 1 without it. | Drop `--cross-ref`; run the drift + register passes. |
| `audit_evidence_metadata` | Registered command omits `--strict`; code returns 0 unconditionally. A DB with every `metadata_quality`/`verification_status` set to garbage → **exit 0**. (`--strict`'s own condition, `ready_count==0`, is also wrong for a gate.) | Give it a real fail condition and register it with the flag. |
| `matrix_consistency` | The document side is a **transcription hardcoded inside the check**. Flipping a cell in `governance/evidence-architecture.md` §3 → exit 0; mutating `schemas/directness.py` → exit 1. It enforces code↔private-copy, not doc↔code as its `basis` claims. | Parse the document table. |

Two further repairs of the same class:

- **`citation_mining_session` has a mutation escape.** A source with no `source_slug_links` row is
  exempt from the gate entirely — the same 65 orphan sources, arriving from the other side.
  §5.1's `source_orphan_audit` closes it.
- **`validate_jurisdiction` cannot fail on its subject.** 55 warnings that never escalate; its
  canonical-24 jurisdiction list predates the Phase-3 corpus it scans, and its `data/sources` leg
  scans a nonexistent directory. Repoint or retire the second leg; refresh the enum.

### 4.2 The continuity layer (limb B) — repair, don't prune

Limb B is legitimate and currently broken in ways that cost real enforcement.

1. **`sessions/LATEST` is serving two incompatible consumers.** It means both "most recent session"
   (continuity) and "most recent *research* session" (the subject of the **blocking**
   `citation_mining_session` check). It points at 2026-06-11; the newest record is 2026-08-01.
   Advancing it makes the blocking check report *"Total in scope: 191, Outstanding: 0"* — it passes
   by having nothing in scope. **Both states of that gate are meaningless.**
   *Fix:* split the pointer. `sessions/LATEST` = continuity, advanced every session.
   `sessions/LATEST-RESEARCH` = the mining gate's subject, advanced only by research sessions.
2. **`sessions/handoff-next-session.md` is 11 weeks stale** — points at HEAD `de364a88`, a
   2026-05-13 session record, and branch `main`. It is the most load-bearing continuity artifact and
   the most stale thing in the repo. *Fix:* rewrite at every session close; make it the single
   handoff, and add a check that its named HEAD is an ancestor of the current one.
3. **`workplan/` cannot be sorted.** CLAUDE.md §9 says "sort by date and read the newest", but
   `website-preparation.md`, `search-coverage-completion-workplan.md`, and
   `workplan-jurisdiction-sweep.md` carry no date. The instruction is unfollowable as written.
   *Fix:* enforce `NNNN-NN-NN-slug.md` naming; retire or rename the undated files.
4. **Three connection registers** — `connection-register.md`, `-active.md`, `-archive.md`.
   *Fix:* one register; the DB is canonical, the file derives.
5. **Two live skills instruct running a broken script against a database that does not exist.**
   `skills/item-specification-writer_SKILL.md:27` and `skills/cell-curator_SKILL.md:16` both say:
   *"If `specification` queries return empty, run `python3 scripts/db/migrate_all.py`."*
   `data/db/` **does not exist**; running it creates an empty legacy DB, then fails. This is offered
   at precisely the moment a session is confused about missing data. *Fix first, before Wave 3.*
6. **CLAUDE.md contradicts itself, and is loaded every session.** §0 says *"Two GitHub Actions
   workflows gate `main` (ci.yml, audit.yml)"*; `audit.yml` was retired 2026-08-01; §7 correctly says
   four. Two copies of the roster in one always-loaded file.

**Cost note, since it inverts the intuition:** the SessionStart hook is 51 lines, ~750 tokens, and
only 12% redundant with CLAUDE.md — it is the sole per-session carrier of 13 of the 15 research
rules. **CLAUDE.md is ~7,300 tokens per session, ten times the hook.** If per-session cost is a
concern, the onboarding document is the expensive artifact, not the contract.

### 4.3 Drift sources — enforcement that manufactures the error it exists to prevent

- **`research-contract-baseline.json` can grant itself amnesty.** Hand-editable ratchet;
  `--write-baseline` absorbs *new* debt into the baseline, and nothing gates an increase. A ratchet
  that can be loosened is not one. *Fix:* baseline increases fail the check.
- **`research_contract_sync` is advisory**, so the generated hook can be hand-edited and CI only
  murmurs. The single-source guarantee has a soft back door. *Fix:* promote to blocking.
- **`db_meta.schema_version = 11` vs `PRAGMA user_version = 38`.** Two version markers disagreeing.
  *Fix:* drop the `db_meta` row (CLAUDE.md already calls it a stale init-time artifact).

---

## 5. REINVEST

Pruning alone leaves the product unguarded. The reinvestment is small — three checks and four schema
changes — and it is the first enforcement aimed at the handshakes.

### 5.1 Three checks that do not exist and should

1. **`source_orphan_audit`** — handshake (b)↔(a). *Invariant:* every synthesis-eligible
   `evidence_sources` row (tier 1–3) has ≥1 `source_slug_links` row, **or** an explicit recorded
   disposition. *Today:* 65 of 863 sources link to no topic; `graph_audit` merely counts them at
   info level, and the blocking mining gate structurally exempts them.
2. **`bpc_citation_link_handshake`** — handshake (c)↔(d); the pipeline contract's
   `judgment/derivation-handshake` criterion, currently INCOMPLETE. *Invariant:* every `REF-\d{5}`
   cited in `references/bpc/<topic>/<slug>.md` has a `source_slug_links(slug, ref_id)` row and
   resolves in `evidence_sources`. *Today:* 5 of 123 cited refs across 13 BPC files violate it.
   `check_rendered_docs` already enforces exactly this — but only for 2 HTML files.
3. **`search_coverage_handshake`** — table (a) integrity. *Invariant:* for every `bpc_metadata` row
   with `search_complete=1` (49 of 83), each jurisdiction/language claimed in `jurisdictions_searched`
   is backed by ≥1 `search_executions` row for that slug. *Today:* nothing cross-checks coverage
   *claims* against the search log. This is the check that makes the research-tracking table
   unfalsifiable by prose.

### 5.2 Promotions

- `research_dod` advisory → **blocking**. The R1–R15 contract currently has no blocking enforcement
  anywhere.
- `research_contract_sync` advisory → **blocking** (closes the back door in §4.3).

### 5.3 Schema changes to make the target shape expressible *(migrations, per the standing rule)*

| # | Change | Why |
|---|---|---|
| 1 | `evidence_sources.mining_status NOT NULL ∈ {pending, extracted, no-extractable-data}` | **Table (b)'s defining column does not exist.** 856 of 863 sources have no extraction row and are indistinguishable from "read, nothing to extract" — the exact failure the column was described to prevent |
| 2 | Junction table `cell_refs(cell_id FK, ref_id FK)` replacing `evidence_cell_state.governing_refs` JSON text | The c→d handshake that feeds the site is an unconstrained string. Zero dangling today; a typo orphans a published best practice silently |
| 3 | `jurisdictional_values.ref_id FK → evidence_sources NOT NULL` | The largest evidence table (109 rows) links to sources by free-text `standard_name`. All 109 rows are structurally unverifiable |
| 4 | Backfill `item_bpc_links` from `items.bpc_source_slug`, then deprecate the column | DR-2026-07-12 / migration 013 made the bridge authoritative. It has **3 rows**; the column it replaced has **87**. The official mechanism is empty and the deprecated one is load-bearing |

---

## 6. Owner decisions ⚑

| # | Decision | Why it is yours |
|---|---|---|
| ⚑1 | **Turn on branch protection for `main`.** | Rated the single highest-leverage change. Without it, 30 blocking controls are advisory in fact — PR #76 merged with a blocking check red, and 5 red runs since stopped nothing. Every blocking-vs-advisory decision below is cosmetic until this is on. **Do not require `DB integrity` until its content backlog clears**, or no data-touching PR will ever merge |
| ⚑2 | **Consolidate the five rival (c)-layer tables** into one evidence table with mandatory `ref_id`. | D-SCHEMA. 167 rows across 5 tables against 863 sources; none is a general evidence table |
| ⚑3 | `generate/room_page.py` — fix or archive. | Crashes: `no such table: room`. Six phantom tables; tied to the website-v0 path |
| ⚑4 | `test_adjudication_integrity.py` — wire, archive, or leave quarantined. | Honestly red (274 tier inconsistencies), wired to nothing. Couple to the fate of its quarantined parent |
| ⚑5 | `test_generate_parts_4_2.py` — re-fixture and register, or archive. | Vacuously green (`SKIP — test DB not present: /tmp/work14.db`). It is the **only** test of a live generator. Recommend keep + re-fixture |
| ⚑6 | `probes/citation_mining_pipeline.py` — keep or archive with the other probes. | Produced committed provenance on 2026-07-19. Keep if the coverage loop continues |

Carried from the prior plan and still open: ratify `verification_status`; widen DR-2026-05-28's
exemption list (column-scoped) vs requiring migrations from the scheduled jobs; decide what
`schemas/*.py` mirrors; the 6-slug banner drift; retire `schema_reference_drift_audit`.

---

## 7. Sequencing

Each step is independently landable and leaves the tree green-or-better.

| Step | Work | Gated on |
|---|---|---|
| **1** | Fix the two skill files pointing at the nonexistent DB (§4.2.5); fix CLAUDE.md §0 (§4.2.6) | nothing — do first, they actively mislead |
| **2** | Repair the three gates that cannot fire (§4.1) | nothing |
| **3** | Archive Waves 1–2 (58 files) | nothing |
| **4** | Prune/merge/demote the 6 registry checks (§3.1) | nothing |
| **5** | Split `sessions/LATEST`; rewrite the handoff; date the workplans; one connection register (§4.2) | nothing |
| **6** | Close the baseline back door; promote `research_contract_sync` (§4.3, §5.2) | nothing |
| **7** | Wave 3 archive (2 files) | step 1 |
| **8** | Schema changes 1–4 as migrations (§5.3) | ⚑2 for the wider consolidation; 1–4 stand alone |
| **9** | Write the three handshake checks (§5.1) | step 8 for #1; #2 and #3 need no schema change |
| **10** | Promote `research_dod` to blocking | steps 8–9 |
| **11** | Branch protection | ⚑1 |
| **12** | Wave 4 archive | ⚑3–⚑6 |

Steps 1–7 need no owner decision and remove most of the surface. Steps 8–10 are the reinvestment.
Steps 11–12 are gated.

---

## 8. What this buys

**Removed:** 64 script files (40% of the Python surface), 2 vacuous checks, 1 duplicate report,
3 demotions, and one CI job's worth of never-fail compute.

**Repaired:** 3 blocking gates that could not fail, 1 mutation escape, 2 drift sources, 6 continuity
artifacts — including one that has been quietly disabling a blocking check for seven weeks, and two
skill files that direct sessions to run a broken script against a database that does not exist.

**Gained:** the first enforcement of the inter-table handshakes — three checks asserting row-level
invariants across (a)→(b)→(c)→(d), plus the schema to express "this source's data has not been
scraped yet", which is currently unrepresentable.

**Net:** a smaller apparatus, pointed at the pipeline instead of at itself, with the property that
every remaining check has been watched failing.

### Definition of done

- [ ] No registry check passes over an empty set (the vacuity guard already enforces `EXAMINED: n`)
- [ ] No blocking check is structurally incapable of exiting 1 — each has been watched going red
- [ ] Every artifact in `scripts/` is registry-referenced, imported by something live, or archived
- [ ] Each of the five handshakes (a)→(b)→(c)→(d)→(e) has at least one check asserting a row invariant
- [ ] `sessions/LATEST`, the handoff, and `workplan/` are accurate at session close and machine-sortable
- [ ] `pipeline_contract_audit` reports 0 INCOMPLETE criteria, or each remaining one carries a dated owner decision
