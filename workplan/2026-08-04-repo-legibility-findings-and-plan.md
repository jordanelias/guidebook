# Repo legibility: findings from a full read, and the plan they produced

**Date:** 2026-08-04 · **Baseline:** `6dae668d` (= `main` after PR #82/#83)
**Status:** ACTIVE — batches A, B and C executed (see `git log`); D, F, G-shrunk, J outstanding.

## Why this file exists

The owner's goal, verbatim: *"I just want a very clean working tree that doesn't get
bogged down by Claude Code constantly pulling up stale information or getting confused
when scanning because too much context."*

The operative metric is therefore **agent legibility**: when a session greps or scans
for a fact, how many answers come back and how many are wrong. "Stale" here means
*readable and wrong*, not merely old — `_archived/` is largely fine because it is
unambiguously marked. Rank by **likelihood-of-being-read × wrongness**, not by file
count or bytes.

Seven agents each read a slice of the repository **line by line** — 61 skills, 124
scripts, 3 tools, 32 schemas, 47 governance docs, roughly 62,000 lines — with coverage
tables proving the read. This is the distilled result. It is committed because the
reading was the expensive part and it existed nowhere but session context.

**How to use it:** every unverified figure below is a lead, not a fact. Re-derive
before acting. Readers were wrong at least three times (a link-row count off by two
orders of magnitude; a mis-scoped resolution query; three path errors), and the
orchestrator was wrong twice more in ways its own compliance check caught. Items
marked `[VERIFIED-BY-OPUS]` were independently re-checked.

## What has been executed

| Batch | Commit | What |
|---|---|---|
| A | `6329973f` | CLAUDE.md: `decisions` table no longer "empty scaffolding"; test-registry claims corrected |
| B | `80258778` | `validate_temporal` quarantined; `citation_mining_session` refuses an unresolvable `--session`; `research_batch_dod --selftest` asserts *which* rules fire; `test_db_integrity` registry note superseded |
| — | `01c61aff` | Three defects the compliance check found in B, incl. a session-guard false-negative class |
| C | `60bf6b75` | `workplan-orchestrator`: nonexistent canonical plan, `/tmp` DB, half-wrong population table, placeholder paths, five live skills listed as deprecated, superseded roadmap |
| E | *this commit* | The seven legacy importers can no longer open the canonical DB |

**Outstanding, in the order recommended by review:** J (retired-vocabulary tripwire,
built first as the sweep's instrument, advisory) · D (skills fact sweep) · F (doctrine
false statements) · G-shrunk (the two generator lines rendering `UNVERIFIED-1` into
committed pages, plus `db.py`'s crash and help text).

**Dropped deliberately:** H (schema mirrors — widest blast radius, lowest legibility
gain, no gate demands the mirror be complete; if it matters it is a
generate-from-`PRAGMA` project, not 76 hand-typed fields) and I (dashboards — an
owner-facing display surface, not an agent-grep surface).

---

Seven agents each read their slice line-by-line (coverage tables provided, ~62,000 lines
total). This digest is the main thread's distillation. **Items marked [VERIFIED-BY-OPUS]
were independently re-checked against the live repo/DB by the orchestrator.** Everything
else is the reader's claim and must be re-derived before acting.

Live baseline: `user_version` 52 · DB integrity 63/69 (failing I2, C02, C03, C04, D05, G02)
· 863 evidence_sources · 157 decisions · 23 populations · 106 slugs · 93 items · 15 cells.

---

## A. BLOCKING GATES THAT CERTIFY NOTHING (highest severity)

**A1. `validate_temporal.py` — blocking, examines zero records. [VERIFIED-BY-OPUS]**
Registered `level: blocking`, `kinds: [schema, data]` (check-registry ~line 419). Reads
`data/temporal/` — **which does not exist**. Run output: `Temporal validation: 0 rules,
0 standards, 0 versions, 0 supersedence links / All checks passed.` exit 0. No `min_items`
guard — the exact defect the 2026-08-01 rework fixed in `validate_schema.py`.

**A2. `citation_mining_session` — blocking, passes on a nonexistent session. [VERIFIED-BY-OPUS]**
Ran with `--session no-such-session-xyz.md`: `Total with citation_mining row: 9 (4.7%) /
Outstanding: 0`, exit 0. `sessions/LATEST` currently points at a June session, so this is
its behaviour on every run. A typo'd session name is indistinguishable from compliance.
Also: `JOIN source_slug_links` means 15 of 191 T1–2 sources with no slug link can never
appear as outstanding. CLAUDE.md §10 names this defect (W4.1 split is the fix).

**A3. `research_batch_dod --selftest` — blocking, verifies 1 of 9 rules.**
Builds a corpus violating nine rules, declares `expected = {R1…R11}`, then asserts only
`rc == 1`. The expected set is printed, never checked. Also exits **0** when no DB present.

---

## B. LIVE HAZARDS

**B1. `scripts/migrate/*.py` write the CANONICAL DB — the safety framing is inverted. [VERIFIED-BY-OPUS]**
CLAUDE.md §7 warns that `scripts/db/**` targets `data/db/guidebook.db`, "a different,
legacy file". True — and `data/db/` **does not exist**, so those three files are inert.
But 6 of 9 `scripts/migrate/*.py` use
`DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))` — canonical by
default — and write with plain INSERT+commit outside the migration system.
- `migrate_connections.py` is fully runnable today: all 11 INSERT columns exist in the live
  13-column `connections` table; input `references/connections/_index.md` present; no
  network/PAT needed. Writes land below the blocking gate's detection floor.
- `migrate_items.py` takes **zero required arguments** and opens the canonical DB
  immediately; saved only because it names `applicable_groups`, a column that no longer
  exists (crashes before commit).
- `migrate_slugs.py`, `migrate_decisions.py`, `migrate_gaps.py`, `migrate_bpc_metadata.py`
  same pattern; `migrate_evidence_sources.py` crashes on retired `doi_less_key`.

**B2. A governance doc licenses the act CLAUDE.md calls absolute. [VERIFIED-BY-OPUS]**
`governance/migration-based-writes-adopted-2026-05-11.md` (Status: **Adopted**, no
supersession banner), line 69: *"Single-agent sessions on a quiet repo can continue using
`db.py` if convenient — the CI reproducibility check (below) is forgiving for the bootstrap
window."* Directly contradicts CLAUDE.md §0 rule 4 ("The rule is absolute") and
research-contract.yaml's "Never hand-edit the DB". The blocking reproducibility gate
compares only `user_version` + COUNT(*) on six tables, so it cannot catch the result.

---

## C. FALSE STATEMENTS IN CANONICAL DOCTRINE

**C1. `governance/evidence-methodology.md:128` — asserts a view exclusion that does not exist. [VERIFIED-BY-OPUS]**
*"it becomes a queryably distinct weak-band row of `v_best_practice` once the DR-2026-07-21
§5 engine follow-up lands — until then the view still excludes it."* Live: the view has
`regulatory_stratum_only` and `strength_band` columns and returns **3 rows** with
`strength_band='weak'` (migration 029). The paired sentence in `evidence-architecture.md:105`
was corrected 2026-08-04; this one was missed. **The corpus now asserts both a fact and its
negation.**

**C2. `governance/mission-PROVISIONAL.md:49` — repealed absolute doctrine at full strength. [VERIFIED-BY-OPUS]**
*"A best-practice claim derived solely from code consensus is in error."* — the absolute
form repealed by DR-2026-07-21 Option A. No supersession banner; file header says
"PROVISIONAL — committed 2026-04-26". Also carries the pre-reconciliation tier ladder
(T2 = NGO/advocacy, T3 = systematic reviews) and Tier-1/Tier-2-as-design-mode vocabulary.
CLAUDE.md guardrail 2 calls for a redirect stub; this is the full old text.

**C3. Marker scheme: two-marker ●/○ vs operative three-marker ●/◐/○.**
`mission-and-epistemics.md:136` states the two-marker scheme; `tier-system.md` §5 (operative)
states three. Also in `armature_v4.md:35,399`, `armature_v4_resolutions.md:23`,
`armature_v4_integration.md:16`, **and `schemas/enums.py:180-189` (`EvidenceMarker`)** —
which therefore cannot represent ◐, a value both tools emit.

**C4. Retired D-0157 vocabulary asserted as the current enum, in the DEPLOYED PI.**
`project-instructions-v10_14.md` rules #6 and #10 gate on
`verification_status ∈ {VERIFIED, UNVERIFIED-1}`. No row can hold `UNVERIFIED-1` since
today. Same in `evidence-methodology.md:48,115,199-206,464`, `co1-operational.md:203,398,
423-456`, `migration-survival.md:79,176,246`. PI also names `audit.yml` (retired 2026-08-01)
as live enforcement.

**C5. Population taxonomy: three incompatible schemes in ratified docs.**
Canonical = 23 flat codes (DR-2026-07-23; verified: `populations` = 23 rows, matches
`PopulationCode` exactly). `functional-taxonomy.md` (RATIFIED, **no banner**) describes 22
codes and keys §4/§6 to `VIS`/`UPL`/`DBL`/`OFS`/`CFS`/`PCS` — none of which exist.
`held-tensions.md:393-401` still lists the reconciliation as open (closed by DR-2026-07-23).
`population-taxonomy.md` contradicts itself: line 2 "SUPERSEDED", line 209 "CANONICAL".

**C6. Other governance contradictions:** freshness windows differ across `time-model.md`
§4.3 / `legal-regulatory.md:57` / `tier-system.md:57` (legal-regulatory misquotes A9 and
inverts Co-1); jurisdiction count 24 vs its own 25-row table vs 27-code enum; DAR expands to
"Adaptable Readiness" (mission) vs "Ageing and Resilience" (`armature_v4.md:46`);
`repo-strategy.md:36,50` says direct-push, CLAUDE.md §8 says branch+PR;
`mission-and-epistemics.md` line 2 "CANONICAL" vs line 190 "Not yet operative".

---

## D. SILENT DEGRADATION (the class that already fired once today)

**D1. `regenerate_vetting_surface.py:205` — already fired.**
`vs_ok = vs in ("VERIFIED", "UNVERIFIED-1")`. `UNVERIFIED-1` retired today; all **111**
UNVERIFIED sources now silently render as "weak" bibliography. No error, no count change —
the verdict distribution just moved.

**D2. `tools/evidentiary_audit.py:105-114` — `is_disputed()` is two-thirds dead.**
Leg 1 (`status == "DISPUTED"`) matches nothing; leg 2 (`closure_reason='disputed-existence'`)
matches nothing; only the substring `"DISPUTED 2026-07-20 correctness-sweep"` in
`verification_note` still fires (7 rows → 10 instances). Any note normalisation re-zeroes it.

**D3. `population_page.py:97` and `spec_page.py:117` render the literal `UNVERIFIED-1`
into committed pages** — live today in `site/populations/mob.html`.

**D4. `pipeline_completeness.py:669-679`** asserts as template prose a data fact it never
checks ("every item pointing at a BPC slug points at a RETRACTED-PRE-REHAB one" — true today
87/87, false the moment one is re-pointed). Integrity-gate chips at 523–576 are hardcoded
booleans; building or retiring a gate changes nothing.

**D5. Token-keyed predicates that silently widen/narrow:** `evidentiary_audit.py:245`
(`status='ACTIVE'` silently excludes 23 STUB slugs), `:287` (`practice`/"Co-3" stream matches
zero rows and is in no enum), `:64` (frozen list of past pollution codes), grade thresholds
duplicated in Python and JS; `pipeline_completeness.py:97,99-101,131-136` (GREY/PMID-ONLY/NULL
fall in no bucket).

---

## E. SCHEMA MIRROR DRIFT (32 Pydantic models vs live tables)

- `evidence_source.py`: **21 fields vs 97 columns**; `authors`→`author_display`,
  `year`→`pub_year`, `title`→`pub_title`; docstring claims 531 records (live 863). **REGENERATE**
- `population.py`: only 1 of 18 fields matches a column by name (`code`→`population_code`,
  `label`→`display_name`, `definition`→`description`); docstring describes a nested taxonomy
  and a `population_resolved` view that do not exist. **REGENERATE**
- `item.py`: `item_id` required but NULL in every live row — the model validates no real row;
  the live payload (`pmp_*` columns) is unmodeled. **REGENERATE**
- `connection.py`: `primary_target` has no column (moved to `connection_targets` junction);
  273 live rows. `gap.py`: `date`→`created_at`. `conflict.py`: `population_a`→`pop_a`.
- Honest mirrors (keep): `jurisdictional_value.py`, `population_links.py`, `slug.py`,
  `source_value_extraction.py` (its 22-of-33 subset annotation verified exactly right),
  `decision.py`.
- **`validate_pydantic_schemas.py` contains two false claims in its own curation notes**:
  "no `room` table exists" (rooms = 17 rows) and case_studies/economics "not DB entities"
  (both exist). Maps only 15 of 64 models; `SearchExecution` is unmapped and has already
  drifted two columns while its docstring claims "drift is a CI-caught bug".

---

## F. SKILLS (61 files) — the worst stale-context injection

**F1. Six skills carry "canonical" population tables that disagree with the DB on ~half the
codes.** `workplan-orchestrator:205-227`, `table-formatter:43-44`, `guidebook-auditor:91-113`,
`item-specification-writer:177`, `cross-population-conflict-mapper:34-45`,
`functional-deficit-auditor:88-102`. Codes `VIS, DBL, OFS, NEU, IntD, VIS/DEAF` do not exist.
`table-formatter` mandates a `VIS/DEAF` column "canonical, never reorder" while two other
skills call `VIS/DEAF` an error on sight. All three treat **BAR** as a doctrine violation;
BAR is an active population with 372 `item_population_links` rows.

**F2. `workplan-orchestrator` is the skill triggered at the start of any complex task**, and
it instructs: load `workplan/workplan-co0007-v4.md` as "the only operative plan" (**file does
not exist**), read `/tmp/guidebook.db`, trust a May-2026 roadmap, and treat five
currently-active skills as deprecated. Complete stale-context injection at the exact moment
an agent has nothing to contradict it.

**F3. Skills that write to dead schema:** `question-author` UPDATEs a `specification` table
that does not exist (every instruction in §2–3 fails); `bibliography-compiler` names columns
(`authors`, `year`, `title`, `doi_less_key`) none of which exist and denies columns
(`language`, `journal_name`) that do — contradicted by `citation-miner:141-144`, which is right.

**F4. Placeholder strings from a botched find-and-replace ship as file paths:**
`references/SQLite slugs table`, `SQLite gaps table`, `SQLT decisions table` in
`relational-integrity-checker:21,33,41-43`, `functional-deficit-researcher:218,241`,
`session-consolidator:78,105`, `workplan-orchestrator:307-309`. They read as instructions to
GET/PUT files with those names.

**F5. Skills instructing writes to archived tombstones:** `functional-deficit-researcher:210,212`
appends to `references/best-practices-compendium.md` and `references/search-log.md`, both
ARCHIVED stubs saying "Do not edit this file". `gap_register.md` (deleted) is a write target in
`find-and-replace:143`, `structure-auditor:109`, `toc-editor:229-234`,
`supplemental-integrator:59`, `sensory-coherence-checker:107`, `guidebook-auditor:155`.

**F6. Eleven contradiction pairs** between skills on the same act (markers, population codes,
part numbering, item-code prefixes, Scholar Gateway as a citation graph, which skills are
deprecated). Full list in the skills reader's §3.

**F7. Registry omissions:** `skill-registry.md` omits `integrity-protocol` (invoked by
check-registry:532) and `supersession-audit` (used by 3 attestations) — an agent auditing
"unregistered skill files" would wrongly conclude they are retireable.

---

## G. STALE PROSE IN CODE COMMENTS (the corrected-today class, still recurring)

- `assess_cell.py:127` — `PILOT_CELLS` still pins `("B-10","NEU")`; NEU→BRAIN rename means
  `validate_population()` raises against any current-schema DB. **The engine cannot complete
  a run.** Also `:26-27` docstring says the extraction table is empty (body corrected to 8);
  `:439-440` "25 vs 22 codes" (both now 23); `:518-519` "1/92 populated" (now 3/93).
- `pilot_renderings.py:285-291, 314-341` — describes 8 NULL shas, two failing shas, a
  document "frozen at the 7-cell era", and "20 'None' publications". **All resolved today**;
  the file documents warts that no longer exist.
- `build_site.py:7-15` — "87 files … six items have no page, including A-18" (now 93/93 fresh).
- `db.py:375` — selects `es.title`; column is `pub_title`. **`db.py unmined --slug` crashes.**
  [VERIFIED-BY-OPUS] Also `:767-771` CLI help teaches retired `UNVERIFIED-1` and its
  `--verification-status` choices contain a literal duplicate; `:762` omits `COMPLETE-STATUTORY`
  (a live value); `:1120` `validate` subcommand shells to the quarantined, broken `validate_db.py`.
- `validate_cross_refs.py` — docstring promises 4 checks; `SLUG_REF_RE`/`SECTION_RE`/`HEADING_RE`
  defined at lines 50-53 and **never used**; `--fast` accepted and ignored. Blocking, always-on.
  [VERIFIED-BY-OPUS]
- `validate_evidence_state.py:98` — `r.get(...)` where `r` is undefined (should be `data`):
  latent NameError; also tests retired `UNVERIFIED-CLOSED`/`CLOSED-DELETED`.
- `check-registry.yaml:246-264` — the `test_db_integrity` note records the pre-D-0157
  distribution (VERIFIED 757, VERIFIED-2 71, UNVERIFIED-1 25, DISPUTED 7, …) and concludes
  *"ratifying it is a D-SCHEMA decision for the owner, not a unilateral edit"* — that decision
  is D-0157, made today. Live: VERIFIED 752 / UNVERIFIED 111, nothing else. [VERIFIED-BY-OPUS]
  Note also says "26/35 checks pass"; suite is now 69 checks, 63 pass.
- **CLAUDE.md:141-142** — *"`decisions` in the DB is empty scaffolding"*. It holds **157 rows**
  as of today. Flagged independently by four of the seven readers. [VERIFIED-BY-OPUS]
- `CLAUDE.md §7` — "only `test_db_integrity` is in the registry; eight more … wired to nothing"
  and "each prints `RESULTS: X/Y`": **ten** of twelve are now registered; only three print that line.

---

## H. ORPHANS / RETIREMENT CANDIDATES (with the blockers)

- `scripts/audit/table_connectivity.py` — in neither `checks:` nor `quarantine:`. Nothing runs
  it. The registry's own lines 48-51 describe this as the failure mode it exists to prevent.
- `scripts/generate/room_page.py` — queries **6 nonexistent tables** (`room`, `room_item`,
  `room_item_population`, `specification`, `room_dar_provision`, `room_conflict`); crashes on
  every invocation.
- `scripts/migrate_evidence_sources_v2.py` — 869 lines, hardcoded `/home/claude/` paths, reads
  and writes columns/tables that no longer exist. The single largest block of context noise in
  `scripts/`.
- `item_audit_pipeline.py` — orphan (the skill drives `db.py` instead), interactive `input()`
  that hangs non-TTY runners, `DELETE FROM connections/conflicts/gaps` against the canonical DB,
  and marks manual steps complete without their having run.
- `check_phase_a_complete.py`, `validate_db.py`, `validate_items.py` — quarantined and broken.
- `test_generate_parts_4_2.py` — **exits 0 having asserted nothing** (`/tmp/work14.db` absent).

**BLOCKERS on the "archive the legacy dirs" proposal (all must be cleared first):**
1. Commit `366766ee` (2026-08-03) archived 33 siblings and **deliberately kept** these,
   recording that six `scripts/migrate/` files are named in
   `architecture/sqlite-data-layer.md` §9's build table and archiving them "would silently
   falsify a spec document". That doc update is the precondition.
2. `convert_sources.py` was **maintained yesterday** under D-0157 (commit `1652b681`).
3. `scripts/db/enrich_all_c_stage.py` + `migrate_all.py` + `convert_rooms.py` hold the **only
   source-form record** of the room curation: 47 room DAR provisions with construction stage
   and drawing reference, 7 room conflict resolutions, ~150 room×item×population triples,
   ~30 connection endpoints with citations. Their only other copy is the frozen
   `site/rooms/*.html`, which `build_site.py` says cannot be regenerated. **Capture before archiving.**
4. `migrate_all.py` imports `convert_doctrines`, `convert_specialists`, `convert_rooms`,
   `db/init_db` — archive those five as one unit.

---

## I. THINGS THAT ARE GOOD (do not "fix")

- `graph/build.py:26-41` refuses to open the canonical DB by path AND by basename, and the
  refusal is mutation-tested. **No audit script writes the canonical DB.**
- `graph_audit.py` — 13-case mutation harness including known-debt soundness.
- `register_integrity_check.py` — map-lint guards against checker and renderer sharing a lie;
  DB→doc completeness direction; per-element amended I3. De-quarantine was justified.
- `pipeline_contract_audit.py` — its existence≠running correction is the model for this work.
- `source_value_extraction.py` — the model of an honest subset annotation.
- `project-instructions-v10_7…v10_13` — 9-line redirect stubs; exactly what CLAUDE.md promises.
- All 7 `ci_helpers/` — clean, no fixes needed.
- `pipeline-operations.md` — model of dated-measurement hygiene.
