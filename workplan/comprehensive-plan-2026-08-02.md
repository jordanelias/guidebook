# Comprehensive plan — align the apparatus to the pipeline, then get back to research

**Date:** 2026-08-02 · **Status:** PROPOSED · **Author:** tooling session, branch `claude/resume-infrastructure-work-zvl5ft`

**Supersedes:** `workplan/consolidation-and-compliance-plan-2026-08-01.md` (both parts) and
`workplan/prune-and-reinvest-plan-2026-08-02.md`. Those remain as the record of how the findings
were reached; this is the single plan to work from.

**Fidelity statement.** Every number in this document was produced by a command run against this
clone on 2026-08-02, not transcribed from prose. §9 records the provenance of each. Four
independent read-only audits ran that day: all 58 registry checks under adversarial mutation, all
159 Python files with full-repo caller sweeps, the 63 DB tables with every handshake measured in
both directions, and the hooks/CI/workflow layer. Where an audit's number was load-bearing for a
decision here, it was re-derived independently before being used.

---

## 1. The target shape

This is the destination, stated by the owner. Everything below is judged against it.

### 1.1 The pipeline

| # | Stage |
|---|---|
| 1 | Identify a research topic |
| 2 | Perform research across languages and jurisdictions |
| 3 | Adjudicate whether the research is valuable |
| 4 | Log the source in detail and associate it to the topic |
| 5 | Derive the relevant information into a table; assess relevance to disability group / access need / functional impairment |
| 6 | Identify whether other information in the source is relevant to another topic; if so, flag and queue it for a different research pass |
| 7 | Run an adversarial pass for quality control — accurate evidence, accurate sourcing |
| 8 | Review against ethical doctrine, evidence hierarchy, project mission, definitions of best practice |
| 9 | Identify whether the topic decomposes into multiple design specifications (mobility circulation → corridor widths, doors, thresholds, stairs) |
| 10 | Analyse and synthesise the available evidence into best practices per specification |
| 11 | Specifications built on a template, assigned a category of information |
| 12 | Build the catalogue of specifications / rooms / buildings / case studies |

Stages 9–12 may instead run as economic case studies or building typologies; the structure is parallel.

### 1.2 The tables

| | Role | Must contain |
|---|---|---|
| **(a)** | Research tracking | every topic/slug; which languages and jurisdictions have been searched; **count of sources secured per evidence tier** |
| **(b)** | Sources matrix | every source examined; its language; the topics it applies to; **whether its data still needs to be scraped** |
| **(c)** | Evidence | the actual data / values / process from each source; its tier; where it came from |
| **(d)** | Best-practice synthesis | the analysed, synthesised layer — may have many empty columns |
| **(e)** | Specifications / items / rooms | best practices and their sources, formatted onto the template |

The website renders each page from these tables.

### 1.3 What compliance is for

Verbatim: *"we need to have contracts to ensure compliance with processing through pipeline as well
as handshakes/pointers through tables so that there is always a link from one table to another so
nothing gets orphaned"* and *"our compliance mechanisms are largely about whether we have actually
filled out the table correctly and done the handshakes correctly and whether we have veered/deviated
from how we derive best practices or syntheses."*

---

## 2. Where the project actually is against that shape

`PRAGMA user_version = 38` · 63 tables · 13 views · `PRAGMA foreign_key_check` → **0 violations**
(declared FKs are clean and enforced; the damage is entirely in links never declared as FKs).

### 2.1 Table-by-table

| Role | Served by | Populated | Verdict |
|---|---|---|---|
| **(a)** | `slugs` (106) · `search_coverage` (4 960) · `search_languages` (1 558) · `lang_jur_map` (70) · `search_executions` (84) | 86.7% of the jurisdiction grid NOT-RUN | **Strongest part of the schema** — but the *third column of (a), per-tier source counts per topic, is stored nowhere.** It is derivable ad hoc; it is not tracked, so it cannot be asserted against |
| **(b)** | `evidence_sources` (863) · `source_slug_links` (1 013) · `evidence_source_authors` (1 478) | healthy | **Missing its defining column.** No table anywhere records whether a source's data has been scraped |
| **(c)** | **five rival tables** — `jurisdictional_values` (109) · `spec_value_probes` (31) · `reasoning_doc_citations` (14) · `source_value_extractions` (8) · `economics_entries` (5) | **167 evidence rows against 863 sources** | No general evidence table exists. The largest, `jurisdictional_values`, has **no `ref_id` at all** |
| **(d)** | `evidence_cell_state` (15) · `convergence_assessment` (14) | 15 cells of a 93 × 23 = 2 139 grid | Structurally sound, almost unfilled |
| **(e)** | `items` (93) · `item_population_links` (372) · `item_bpc_links` (3) | — | The decreed bridge has 3 rows; the column it replaced has 87 |
| **website** | `scripts/generate/spec_page.py` | 87 pages | 79 render an empty best-practice banner; **1 distinct REF-id appears across the entire site** |

### 2.2 The handshakes, measured

| From → to | Join | FK? | Orphans |
|---|---|---|---|
| (b) sources → (a) topics | `ref_id` | yes on link side | **65 of 863 sources have no topic link** (46 of them tier 1–3) |
| (b) → (c) extraction | `ref_id` | FK exists; **no completeness mechanism** | **856 of 863 sources have no extraction row** |
| (c) → (d) synthesis | `evidence_cell_state.governing_refs` — **JSON text** | **none** | 0 dangling today; nothing prevents one |
| (d) → (e) items | `item_code` | yes | **82 of 93 items have no synthesis cell; 66 have no evidence row in any table** |
| (e) → bridge | `item_code` | yes | **91 of 93 items missing from `item_bpc_links`** |
| (c) `jurisdictional_values` → sources | free-text `standard_name` | **none** | **all 109 rows structurally unverifiable** |
| (e) → website | filename | **none** | 6 items unpublished; script is run by hand |

### 2.3 Stage 6 — the queue

Real, triple-headed, stalled:

- `search_candidates` — 18 rows: ADMITTED 4, MISCELLANEOUS 3, **PENDING-VERIFICATION 9, REHOME 2**. The 11 undrained have sat since 24–25 July.
- `connections` — 23 PENDING untouched since early May; **31 of 273 have no target rows at all**.
- `gap_mining` — the table built specifically to log drain attempts — **0 rows, never used**.

### 2.4 The apparatus

| | Measured |
|---|---|
| Registry checks | 58 — under mutation, **48 KEEP-AS-IS**, 4 repoint, 1 merge, 3 demote, **2 prune** |
| Checks by actual subject | 35 pipeline-substantive : 23 paperwork (≈59:41) |
| **Blocking gates structurally incapable of exiting 1** | **3** |
| Python files | 159 · **90 unregistered** · **64 archivable** |
| `main` branch-protected | **No** (API-verified) → 30 "blocking" controls advisory in fact |
| Pipeline-contract criteria with no check | **6 of 19** — including `judgment/derivation-handshake` and `synthesis/opus-routing` |
| CI wall time | 46–63 s · preflight 23 s · SessionStart hook ~750 tokens · CLAUDE.md ~7 300 tokens/session |
| Real git hooks installed | **0** (only the 14 default `.sample` files) |

**The teeth are inverted.** Of 27 blocking checks, 18 are pipeline and 9 paperwork — but the deep
pipeline QC is systematically soft: the whole `research` battery is advisory except its own selftest,
`migration_reproducibility_deep` is advisory while the blocking version compares 7 scalars, and
`adjudication_integrity` (274 tier inconsistencies) is quarantined. **The R1–R15 contract — the one
declaring research invalid without compliance — has zero blocking enforcement anywhere.**

### 2.5 The blocking gate that is red — decomposed

`test_db_integrity` at 26/35 has been treated as an opaque content backlog. It is not. It splits
cleanly into a **decision** and a **research task**:

**B-class — 111 rows across 11 unratified vocabulary values. One D-SCHEMA decision, no research.**

| Check | Rows | Unratified values |
|---|---|---|
| B01 `verification_status` | 81 | `VERIFIED-2` (71) · `DISPUTED` (7) · `VERIFIED-WITH-CORRECTION` (2) · `VERIFIED-1` (1) |
| B02 `metadata_quality` | 9 | `PARTIAL` (5) · `high` (2) · `medium` (2) |
| B05 `source_type` | 19 | `code` (16) · `grey_literature` (2) · `magazine_article` (1) |
| B06 `gaps.status` | 2 | `CLOSED-DECIDED` (2) |

Of these, **104 rows carry semantically real states** that need ratifying (`VERIFIED-1/-2` are
confidence tiers; `DISPUTED` and `VERIFIED-WITH-CORRECTION` are genuine outcomes; `code` is the
statutory-code source type this project is full of). **7 rows are normalisation**
(`grey_literature`→`grey`, `magazine_article`→`other`). **4 rows are junk** — `high`/`medium`,
lowercase values from a foreign vocabulary that never belonged.

**C/G-class — 120 distinct rows of genuine metadata backfill. This is research work.**

| Check | Rows |
|---|---|
| C01 VERIFIED with no audit trail | 7 |
| C02 DOI with no `doi_resolution_outcome` | 105 |
| C03 COMPLETE with no author | 80 |
| G02 COMPLETE person-authored with no author row | 113 |
| **distinct rows implicated** | **120** |

R10 applies: every locator must be re-retrieved. No back-filling from memory.

---

## 3. The criterion

> An enforcement artifact earns its place if it either
> **(A)** catches a row-level violation in a real table, or
> **(B)** makes session N+1 start on the same guardrails session N ended on.
> **Disqualifier, both limbs:** it must be able to fire, and someone must read it when it does.
> Enforcement whose subject is the enforcement apparatus itself fails both.

Limb B — commit conventions, handoffs, registers, workplans — is legitimate and is **repaired, not
pruned**. But it must be small and each artifact must have exactly one consumer.

---

## 4. Workstreams

Eight workstreams. W1–W4 need no owner decision and can start immediately. W5–W6 are the
reinvestment. W7 is the research backlog. W8 closes the apparatus phase.

---

### W1 — Stop active harm *(≈30 min, no decision needed, do first)*

Three artifacts currently mislead a session that trusts them.

**W1.1 Two live skills direct sessions to run a broken script against a database that does not exist.**
`skills/item-specification-writer_SKILL.md:27` and `skills/cell-curator_SKILL.md:16` both say:
*"If `specification` queries return empty, run `python3 scripts/db/migrate_all.py`."*
`data/db/` does not exist (verified). Running it **creates** an empty legacy database, then fails on
missing tables — and it is offered at precisely the moment a session is confused about missing data.
→ Replace with the canonical path: query `data/guidebook.db`; if a schema change is needed, emit a
migration. Skill edits are governed events — record the change.

**W1.2 `CLAUDE.md` contradicts itself and is loaded every session.** §0: *"Two GitHub Actions
workflows gate `main` (ci.yml, audit.yml)"*. `audit.yml` was retired 2026-08-01. §7 correctly says
four. → Fix §0.

**W1.3 `sessions/handoff-next-session.md` is 11 weeks stale** — names HEAD `de364a88`, a 2026-05-13
session record, and branch `main`. → Rewrite to current state (W4.2 makes it stay current).

**Verification:** `grep -rn "scripts/db/migrate_all" skills/` returns nothing; `CLAUDE.md` §0 and §7
agree; the handoff's named HEAD is an ancestor of `HEAD`.

---

### W2 — Repair enforcement that cannot fire *(≈3 h, no decision needed)*

These are the owner's criterion in its purest form: enforcement that is not working, and whose
existence creates false confidence.

| Target | Defect, proven by mutation | Fix |
|---|---|---|
| **`doctrine_recheck`** — *blocking* | Registered with `--cross-ref`, which runs only pass 2.3, whose findings are all WARNING; exit 1 requires ERROR. **Deleting a CANONICAL governance document exits 0** with the flag, 1 without it | Drop `--cross-ref`; run the drift + register passes |
| **`audit_evidence_metadata`** | Registered command omits `--strict`; code returns 0 unconditionally. **A DB with every `metadata_quality`/`verification_status` set to garbage exits 0.** `--strict`'s own condition (`ready_count==0`) is also wrong for a gate | Give it a real fail condition; register with the flag |
| **`matrix_consistency`** | The document side is a **transcription hardcoded inside the check**. Flipping a cell in `governance/evidence-architecture.md` §3 exits 0; mutating `schemas/directness.py` exits 1. It enforces code↔private-copy, not doc↔code as its `basis` claims | Parse the document table |
| **`citation_mining_session`** — *blocking* | **Mutation escape:** a source with no `source_slug_links` row is exempt from the gate entirely — the same 65 orphan sources, from the other side | Closed by W6.1 |
| **`validate_jurisdiction`** | 55 warnings that never escalate; its canonical-24 list predates the corpus it scans; its `data/sources` leg scans a nonexistent directory | Refresh the enum; retire the dead leg |

**Verification:** for each, re-run the exact mutation and confirm the check now exits 1. A repair is
not done until it has been watched going red.

---

### W3 — Prune the surface *(≈2 h, no decision needed for Waves 1–2)*

**W3.1 Registry: 2 out, 1 merged, 3 demoted.**

| Check | Action | Why |
|---|---|---|
| `validate_population` | **PRUNE** | Vacuous. Scans `references/{bpc,search-log,connections}` for YAML-frontmatter codes (BPC uses HTML comments — there are none) and `data/specifications` (does not exist). Prints "No files … to validate", exits 0. Covered by `population_integrity_audit` + `test_db_integrity` A02/A03 + `validate_axes` |
| `validate_temporal` | **PRUNE** | Vacuous. Loads `data/temporal/**` and `data/sources/*.yaml`; neither exists. T-09 passes *because* the directory is absent |
| `citation_mining_backlog_t2` | **MERGE** into `_t3` | Same script; tier 1–2 ⊂ 1–3. Its 168 rows are a strict subset of t3's 467 |
| `citation_mining_backlog_t3` | **DEMOTE** | A 467-row work queue, not an invariant |
| `attestation_verdict` | **DEMOTE** | Informational by design |
| `test_jurisdictional_divergence` | **DEMOTE** | Green, but its subject script is quarantined. Rot insurance only |

Prose to correct alongside: `references/project-standards.md` RULE A7/A9,
`governance/population-taxonomy.md` §4.1, `governance/time-model.md` §6,
`references/tooling-register.md`. Re-register `validate_temporal` if `data/temporal/` ever lands.

**W3.2 Scripts: 64 files to `_archived/`.** House rule holds — **retire to `_archived/` mirroring the
origin path; never delete.** References in `sessions/`, `decisions/`, `audits/`, `workplan/` are
historical records describing what was true then; they must not be rewritten to tidy a filename.

| Wave | Files | Contents | Risk |
|---|---|---|---|
| **1** | **21** | `probes/generate_*` ×5 (read `/tmp/*.json` inputs long gone) · `probes/probe_ato_author_year_search` · `probes/probe_ato_no_identifier_title_search` · `probes/probe_multi_source_recovery` · `probes/recover_truncated_dois` · `probes/validate_correction_dry_run` · `scripts/test/test_co0009_pipeline.py` · `convert/{__init__,economics,fdr,items,throughlines}` · `db/{apply_connections_batch1,enrich_measurements_batch1,enrich_measurements_batch2}` · `migrate/{phase_01_slugs,phase_02_populations}` | **Zero** — full-repo caller sweep incl. `.github/`, `.claude/`, `governance/`, `references/`, `skills/` returned nothing |
| **2** | **37** | remaining `convert/` (13) · remaining `migrate/` (7) · `migrations/*.py` (4 — **leave the sibling `.sql` ledger untouched**) · `probes/probe_ato_verified_{doi,pmid}` · `db/` (6) · `tag_de_claims` · `tag_fg_claims` · `verify_resolved_dois` · `migrate_evidence_sources_v2` · `reconcile_ledger_dr_2026_05_28` | Zero mechanically; historical references only |
| **3** | **2** | `db/migrate_all.py` · `migrate/migrate_items.py` | **After W1.1** (skills) and after amending the error string at `scripts/item_audit_pipeline.py:240` |
| **4** | **4** | `generate/room_page.py` · `tests/test_adjudication_integrity.py` · `tests/test_generate_parts_4_2.py` · `probes/citation_mining_pipeline.py` | **Owner-gated** — ⚑3–⚑6 |

Waves 1–2 are one-shot converters and migrators from the April–May 2026 YAML→SQLite transition,
superseded by baseline migration `012`; their output directories (`data/items`, `data/populations`, …)
no longer exist.

**W3.3 Never-fail compute.** The `tests` CI job is **9 of 9 advisory** — 21 s per run with no failure
state. Either promote what deserves teeth (W6.3) or move the job to a schedule.

**Verification:** `python3 scripts/run_checks.py --selftest` passes; `scripts/preflight.sh --all`
unchanged except the removed checks; every archived file's callers re-swept and clean.

---

### W4 — Repair session continuity *(≈3 h, no decision needed)*

Limb B, kept but made small and single-purpose.

**W4.1 Split `sessions/LATEST`.** It is being asked to mean two incompatible things: "most recent
session" (continuity) and "most recent *research* session" (the subject of the **blocking**
`citation_mining_session` check). It points at 2026-06-11; the newest record is 2026-08-01. Advancing
it makes the blocking check report *"Total in scope: 191, Outstanding: 0"* — it passes by having
nothing in scope. **Both states of the gate are meaningless.**
→ `sessions/LATEST` = continuity, advanced every session. `sessions/LATEST-RESEARCH` = the mining
gate's subject, advanced only by research sessions. Point `run_checks.py:494` at the latter.

**W4.2 One handoff, kept current.** `sessions/handoff-next-session.md` is rewritten at every session
close. Add a check: the HEAD it names must be an ancestor of the current HEAD. That is a limb-B
invariant that can actually fire.

**W4.3 Make `workplan/` sortable.** CLAUDE.md §9 says "sort by date and read the newest", but
`website-preparation.md`, `search-coverage-completion-workplan.md`, and `workplan-jurisdiction-sweep.md`
carry no date — the instruction is unfollowable as written. → Enforce `YYYY-MM-DD-slug.md`; rename or
retire the undated files.

**W4.4 One connection register.** `connection-register.md`, `-active.md`, `-archive.md` are three
copies. The DB is canonical; the file derives.

**W4.5 Close the two drift back doors.**
- `governance/research-contract-baseline.json` is a hand-editable ratchet, and `--write-baseline`
  absorbs *new* debt with nothing gating an increase. **A ratchet that can be loosened is not one.**
  → Baseline increases fail the check.
- `research_contract_sync` is advisory, so the generated hook in `.claude/settings.json` can be
  hand-edited with only a murmur. → Promote to blocking.

**W4.6 One schema-version marker.** `db_meta.schema_version = 11` vs `PRAGMA user_version = 38`.
→ Drop the `db_meta` row; CLAUDE.md already calls it a stale init-time artifact.

**Cost note, since it inverts the intuition:** the SessionStart hook is 51 lines, ~750 tokens, only
12% redundant with CLAUDE.md, and the sole per-session carrier of 13 of the 15 research rules.
**CLAUDE.md is ~7 300 tokens per session — ten times the hook.** If per-session cost matters, trim
the onboarding document, not the contract.

**Verification:** the mining gate examines a non-empty, current set; the handoff check fires when the
handoff goes stale; `ls workplan/ | sort` is chronological.

---

### W5 — Make the schema express the target shape *(≈4 h + ⚑2; migrations only)*

All changes ship as migrations via `scripts/emit_data_migration.py` → `scripts/migrate_db.py`.
Never hand-edit `data/guidebook.db`. Verify with `python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db`.

| # | Change | Why |
|---|---|---|
| **5.1** | `evidence_sources.mining_status NOT NULL ∈ {pending, extracted, no-extractable-data}`, defaulted `pending`, backfilled `extracted` where an extraction row exists | **Table (b)'s defining column does not exist.** 856 of 863 sources have no extraction row and are indistinguishable from "read, nothing to extract" — the exact failure the column was described to prevent |
| **5.2** | Junction `cell_refs(cell_id FK, ref_id FK)` replacing `evidence_cell_state.governing_refs` JSON text; CHECK that `stated`/`provisional` cells have ≥1 row | The (c)→(d) handshake that feeds the website is an unconstrained string. 0 dangling today; a typo orphans a published best practice silently, and `v_best_practice` reads it |
| **5.3** | `jurisdictional_values.ref_id FK → evidence_sources`, NOT NULL after backfill | The largest evidence table (109 rows) links to sources by free-text `standard_name`. **All 109 rows are structurally unverifiable** |
| **5.4** | Backfill `item_bpc_links` from `items.bpc_source_slug` (87 rows), then deprecate the column | DR-2026-07-12 / migration 013 made the bridge authoritative. It has **3 rows**; the column it replaced has **87**. The official mechanism is empty and the deprecated one is load-bearing |
| **5.5** | Per-tier source counts per topic — a view over `source_slug_links ⋈ evidence_sources.tier` | **(a)'s third column** is currently derivable but not tracked, so no check can assert against it |
| **5.6** ⚑2 | Consolidate the five rival (c)-layer tables into one evidence table with mandatory `ref_id` | 167 rows across 5 tables against 863 sources; none is a general evidence table |

5.1–5.5 stand alone and need no decision. 5.6 is ⚑2 and is the largest single improvement to (c).

---

### W6 — Enforce the handshakes *(≈4 h; the first enforcement aimed at the product)*

**W6.1 `source_orphan_audit`** — (b)↔(a). *Invariant:* every synthesis-eligible `evidence_sources`
row (tier 1–3) has ≥1 `source_slug_links` row **or** an explicit recorded disposition.
*Today:* **65 of 863 sources link to no topic, 46 of them tier 1–3.** `graph_audit` merely counts
them at info level, and the blocking mining gate structurally exempts them. This check also closes
W2's mutation escape.

**W6.2 `bpc_citation_link_handshake`** — (c)↔(d); the pipeline contract's
`judgment/derivation-handshake` criterion, currently INCOMPLETE. *Invariant:* every `REF-\d{5}` cited
in `references/bpc/<topic>/<slug>.md` has a `source_slug_links(slug, ref_id)` row and resolves in
`evidence_sources`. *Today:* **5 of 123 cited refs across 13 BPC files violate it.**
`check_rendered_docs` already enforces exactly this — but only for 2 HTML files.

**W6.3 `search_coverage_handshake`** — (a) integrity. *Invariant:* for every `bpc_metadata` row with
`search_complete=1` (49 of 83), each jurisdiction/language claimed in `jurisdictions_searched` is
backed by ≥1 `search_executions` row for that slug. *Today:* nothing cross-checks coverage *claims*
against the search log. **This is the check that makes the research-tracking table unfalsifiable by
prose.**

**W6.4 `mining_status_drain`** — stage 6. *Invariant:* no `evidence_sources` row sits at
`mining_status='pending'` past a stated horizon without an entry explaining why; `search_candidates`
in PENDING-VERIFICATION/REHOME and `connections` in PENDING carry a terminal-state SLA.
*Today:* 11 undrained candidates since 24–25 July; 23 PENDING connections since early May;
**`gap_mining` has 0 rows — the drain-attempt ledger has never been used.**

**W6.5 Promotions.** `research_dod` advisory → **blocking** (the R1–R15 contract currently has no
blocking enforcement anywhere). `research_contract_sync` advisory → **blocking** (W4.5).

**Verification, non-negotiable:** each new check is mutation-tested before it is registered —
corrupt the target, watch it go red. A check that has not been watched failing does not get a
registry entry.

---

### W7 — Clear the data backlog *(1 decision + ~1 h + several research sessions)*

**W7.1 B-class: 111 rows, one decision.** ⚑7 ratifies or migrates the 11 unratified values (§2.5).
Ratify the 104 semantically real rows; normalise 7 (`grey_literature`→`grey`,
`magazine_article`→`other`); investigate and correct 4 junk rows (`high`/`medium`).
**One D-SCHEMA decision plus one small migration takes B01/B02/B05/B06 green.**

**W7.2 C/G-class: 120 distinct rows — research work.** C01 (7) · C02 (105) · C03 (80) · G02 (113),
120 distinct. R10 applies: re-retrieve every locator; no back-filling from memory. Sequence C02 first
— it is the largest and most mechanical (DOI present, resolution outcome absent, and
`resolve-dois.yml` already exists to do it).

**W7.3 Then, and only then, `test_db_integrity` can be a required check** (⚑1's carve-out lifts).

---

### W8 — Close the apparatus phase and return to research

**W8.1** Land PR #77 and the follow-on PRs from W1–W6.
**W8.2** Write one Decision Record covering the pruning, the three repaired gates, the schema
changes, and the new handshake checks — with the mutation evidence for each.
**W8.3** Re-attest the affected artifacts within `RE_ATTESTATION_WINDOW`.
**W8.4** Update `references/tooling-register.md` to the post-prune state; update CLAUDE.md §7.
**W8.5** Write the handoff (W4.2 format) naming the first research topic.
**W8.6** Stop. The next session is a research session, gated by
`python3 scripts/audit/research_batch_dod.py --session <id>`.

---

## 5. Sequencing

```
W1 ─────────────────────────────────────────────► (do first; nothing depends on it, it depends on nothing)
      │
      └─► W3.2 Wave 3 (needs W1.1)

W2 ─────────────────────────────────────────────► independent
W3.1 / W3.2 Waves 1-2 ──────────────────────────► independent
W4 ─────────────────────────────────────────────► independent

W5.1 ─────► W6.1  (mining_status enables the orphan/drain checks)
W5.2 ─────► W6.2  (cell_refs enables the citation handshake)
W5.5 ─────► W6.3  (tier-count view enables the coverage handshake)
W6.1-6.4 ─► W6.5  (promote only after the new checks are green)

⚑7 ─────► W7.1 ─────► W7.2 ─────► W7.3 ─────► ⚑1 full protection
                                                    │
W8 ◄────────────────────────────────────────────────┘
```

**W1–W4 need no owner decision and remove most of the surface.** They can be landed as four small
PRs this week. W5–W6 are the reinvestment. W7 is the research backlog and is the only part measured
in sessions rather than hours.

---

## 6. Owner decisions ⚑

| # | Decision | Why it is yours | Blocks |
|---|---|---|---|
| **⚑1** | **Turn on branch protection for `main`** | The single highest-leverage change. `main` is unprotected (API-verified), so 30 blocking controls are advisory in fact — PR #76 merged with a blocking check red and 5 red runs since stopped nothing. **Do not require `DB integrity` until W7 completes**, or no data-touching PR will ever merge | W7.3 |
| **⚑2** | Consolidate the five rival (c)-layer tables into one evidence table with mandatory `ref_id` | D-SCHEMA. 167 rows across 5 tables against 863 sources | W5.6 |
| **⚑3** | `generate/room_page.py` — fix or archive | Crashes: `no such table: room`. Six phantom tables; tied to the website-v0 path | W3.2 Wave 4 |
| **⚑4** | `tests/test_adjudication_integrity.py` — wire, archive, or leave quarantined | Honestly red (274 tier inconsistencies), wired to nothing | W3.2 Wave 4 |
| **⚑5** | `tests/test_generate_parts_4_2.py` — re-fixture and register, or archive | Vacuously green (`SKIP — test DB not present: /tmp/work14.db`). **The only test of a live generator.** Recommend keep + re-fixture | W3.2 Wave 4 |
| **⚑6** | `probes/citation_mining_pipeline.py` — keep or archive | Produced committed provenance 2026-07-19. Keep if the coverage loop continues | W3.2 Wave 4 |
| **⚑7** | **Ratify the 11 unratified vocabulary values** (§2.5) | D-SCHEMA. Takes 111 rows and four B-class checks green in one sitting | W7.1 |

Carried and still open: widen DR-2026-05-28's exemption list (column-scoped) vs requiring migrations
from the scheduled jobs; decide what `schemas/*.py` mirrors; the 6-slug banner drift; retire
`schema_reference_drift_audit`.

---

## 7. Definition of done

**Apparatus**
- [ ] No registry check passes over an empty set — the vacuity guard enforces `EXAMINED: n`
- [ ] No blocking check is structurally incapable of exiting 1 — each has been **watched going red**
- [ ] Every file in `scripts/` is registry-referenced, imported by something live, or archived
- [ ] `pipeline_contract_audit` reports 0 INCOMPLETE criteria, or each carries a dated owner decision
- [ ] No contract exists in two hand-transcribed copies, and no artifact serves two consumers

**Pipeline**
- [ ] Each handshake (a)→(b)→(c)→(d)→(e) has ≥1 check asserting a row invariant
- [ ] `mining_status` is NOT NULL on every source — "logged but unscraped" is queryable
- [ ] `governing_refs` is a junction table with FKs, not a JSON string
- [ ] `item_bpc_links` covers every item with a BPC source; `items.bpc_source_slug` is deprecated
- [ ] 0 tier-1–3 sources without a topic link or a recorded disposition

**Continuity**
- [ ] `sessions/LATEST` and `sessions/LATEST-RESEARCH` are distinct and current
- [ ] The handoff names an ancestor of HEAD, checked mechanically
- [ ] `workplan/` is machine-sortable; one connection register
- [ ] No skill instructs an action against a path that does not exist

**Data**
- [ ] `test_db_integrity` 35/35 and required in branch protection

---

## 8. Risk register

| Risk | Mitigation |
|---|---|
| Archiving breaks a caller the sweep missed | Waves are ordered by proven risk; `run_checks.py --selftest` verifies every registered path exists; Wave 3 is explicitly caller-gated |
| A new handshake check is itself vacuous — the defect this whole effort exists to remove | Every new check declares `min_items`, prints `EXAMINED: n`, and is mutation-tested **before** registration |
| Ratifying the 11 values launders real data errors as vocabulary | Split explicitly: 104 ratify, 7 normalise, **4 investigate**. `high`/`medium` are not ratified |
| Schema changes break reproducibility | Every change is a migration; `migrate_db.py --rebuild` before every push |
| Branch protection deadlocks the repo | ⚑1 carries the explicit carve-out: `DB integrity` is not required until W7 completes |
| The plan itself becomes another stale artifact | It supersedes two plans rather than joining them; W4.3 makes `workplan/` sortable so the newest is findable |

---

## 9. Provenance

Every number above traces to one of these, run 2026-08-02 against this clone:

| Claim | Derivation |
|---|---|
| Backlog counts (B/C/G class, 111 + 120 rows, 11 values) | Direct SQL against `data/guidebook.db` (read-only), allowed-value lists read from `scripts/tests/test_db_integrity.py:95–163` |
| 863 sources · 65 orphans · 46 tier-1–3 · 856 unmined · 15 cells · 93 items · 3 vs 87 bridge rows · 0 `gap_mining` · `search_candidates` dispositions · `user_version` 38 | Direct SQL, re-derived independently of the audit that first reported them |
| 58 checks · 48 KEEP · 3 gates that cannot fire · mutation results | Per-check audit — each check run, then its target corrupted in a scratch clone and scratch DB; canonical repo never touched |
| 159 files · 90 unregistered · 64 archivable · wave assignments | Script audit — full-repo caller sweep including `.github/`, `.claude/`, `governance/`, `references/`, `skills/`, docs |
| Branch protection off · CI timings · hook token counts · 6 of 19 criteria | Substrate audit — live GitHub API, executed workflows, measured payloads |
| 63 tables · handshake orphan rates · site render counts | DB audit — `sqlite_master`, `PRAGMA table_info`/`foreign_key_list`, per-pair orphan queries |
| `basis:` distribution (29 unattributed / 15 hygiene / 14 attributed) | `governance/check-registry.yaml`, parsed |

**Two corrections recorded, since both shaped earlier drafts and both were wrong.**
The `basis:` field measures what a check *declares*, not what it *does* — by actual subject the
registry is 59:41 pipeline, not mostly paperwork. And the registry is not the fat: under mutation,
48 of 58 checks survive. The fat is 90 unregistered scripts, three gates that cannot fire, and a
continuity layer that has been quietly disabling a blocking gate for seven weeks.
