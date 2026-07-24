# Research-Matrix Completion — Autonomous Execution Plan (2026-07-24)

**Status:** PROPOSED — owner-gated. This is an *execution* plan, not a new methodology.
It operationalizes the already-RATIFIED coverage-completion loop
(`workplan/coverage-completion-loop-methodology-2026-07-21.md`, §8 owner-resolved) and the
"what" it references (`workplan/search-coverage-completion-workplan.md`). It spins up **no new
register or competing sweep** (CLAUDE.md §9 guardrail 3); it names the concrete, autonomous
steps that drive the existing apparatus to done and bakes in the four completion requirements:
**(a) attempt every in-scope cell, (b) 100% accuracy, (c) route spillover findings to the
correct slug, (d) vet and backfill continuously.**

**Governs:** the cadence and mechanism by which the search matrix — `search_coverage`
(slug × jurisdiction), `search_languages` (slug × language), their planned successor event log
`search_executions`, `lang_jur_map`, `term_aliases`, `gaps`, and `evidence_sources` — is worked
forward until every *required* cell is SATURATED or DEFERRED-WITH-REASON.

---

## 1. The matrix, measured against `data/guidebook.db` (2026-07-24)

*Volatile — re-derive before acting; these are today's readings, not a target to paper over.*

| Axis | Table | Measured state | Reading |
|---|---|---|---|
| Slug set | `slugs` | 80 ACTIVE · 23 STUB · 3 MERGED | STUB = research-target stubs (in scope); MERGED redirect out of scope |
| Jurisdiction cells | `search_coverage` (4,960 rows; 105 slugs × 48 juris) | 640 SEARCHED · 33 THIN · 1 NO-DATA · **4,286 NOT-RUN** | **~86% NOT-RUN** |
| Language cells | `search_languages` (1,558 rows; 82 slugs × 19 langs) | 509 SEARCHED · 190 PARTIAL · **859 NOT-RUN** | ~45% touched; **STUB slugs have zero language rows** |
| Dead languages | `search_languages` | **AR/BN/HI/SW = 0 SEARCHED (82 NOT-RUN each); ID = 1** | 5 of 19 languages effectively unrun |
| Bridge / log substrate | `lang_jur_map`, `gap_mining`, `search_executions` | **empty (0) / empty (0) / does-not-exist** | the loop's memory + required-vs-N/A bridge were designed, never built |
| Open gaps | `gaps` | **39 OPEN** | each must become ≥1 logged search |
| Ungridded slug | `slugs` | `manoeuvring-footprint-vs-turning-radius-methodology` has **no `search_coverage` row at all** | pre-seeded known gap |

**Denominator (the "matrix" to fill).** In-scope slugs = **80 ACTIVE + 23 STUB = 103**
(MERGED excluded — they redirect via `merged_into`). Selected axes = **19 languages × 48
jurisdictions**. The raw Cartesian product (103 × 19 × 48 ≈ 94k) is *not* the target: the
target is the **`lang_jur_map`-required subset**. "Attempted" means *every required cell carries
≥1 logged search (yield may be zero); every non-required cell is explicitly DEFERRED-WITH-REASON.*
Coverage-to-green is explicitly **not** the metric (loop methodology §4).

## 2. What blocks autonomous completion today (root causes, not symptoms)

1. **No required-vs-N/A bridge.** `lang_jur_map` is empty, so "which (slug, jurisdiction,
   language) cells are *required*" is undefined. Without it the priority queue can't rank and
   "done" can't be judged. **Precondition, not payload.**
2. **No logged-search memory.** A cell reading SEARCHED today can't prove *what* was searched
   (verbatim query text survives for ~47 rows only). Any loop that hand-writes coverage inherits
   this un-auditability — it must instead *log each executed search* and derive coverage. The
   `search_executions` event log is designed (`search-coverage-completion-workplan.md` §2.2) but
   absent.
3. **Vocabulary blocker (the five zeros).** `term_aliases` carries controlled vocabulary for
   **14 languages** (44–91 aliases each); **AR, BN, HI, ID, SW have zero aliases.**
   `scripts/generate_search_queries.py` derives queries from `term_aliases` — no terms → no
   queries. The five zeros are a *missing prerequisite*, not skipped work (CO-0005
   `[UNVERIFIED-TERMS]`). **No loop can search a language it has no vocabulary for.**
4. **Generator reach.** `generate_search_queries.py` reaches only ~18 slugs / 14 languages
   (`term_item_links` is thin). It must be extended, in-loop, before a cell it can't reach is
   worked — or that cell logs a `deferred_reason`.

None of these are "search harder" problems; they are substrate. **Phase 0/1 build the substrate;
Phases 2+ drive the queue.** Attempting net-new search before the bridge exists just re-creates
the un-auditable grid.

## 3. Hard constraints the autonomous loop must honor (non-negotiable)

- **Migrations-only (CLAUDE.md rule 4).** Every DB write ships as `emit_data_migration.py →
  migrate_db.py`; never hand-edit `data/guidebook.db` or an existing `data_*.sql`. Verify
  reproducibility (`migrate_db.py --rebuild /tmp/rebuilt.db`) before every push.
- **Schema changes are owner-gated Decisions.** Creating `search_executions` (+ its views/FTS)
  is a **D-SCHEMA** change: new `scripts/migrations/NNN_slug.sql` (bump `user_version`) **plus**
  the mirrored `schemas/*.py` Pydantic model (drift is a CI-caught bug). `lang_jur_map` already
  exists (populating it is data, not schema).
- **Opus-class synthesis floor (PI rule #2 / DR-2026-06-10).** Only Opus-class models write
  `best_practice_synthesis`. Lower-tier sessions do inventory, verification, multilingual search,
  and comparison tables, then **queue** the doc — they stop at the synthesis boundary.
- **No unattended judgment (loop methodology §3–§5).** The loop automates *cadence + mechanical
  scaffolding*; every act of judgment stays gated. The loop MUST NOT, unattended: admit a source
  that fails re-retrieval; change any adjudicated/consensus figure; ratify a gap closure; or
  invent vocabulary by back-translation. Those **escalate and stop for review.**
- **PR-gated, never `main`.** Each batch opens a PR against `main`; it never merges, never pushes
  `main`. Effective cadence = owner review speed.
- **Connector reality (loop methodology §9).** MCP-tool-created triggers run fresh sessions with
  **built-in tools only — WebSearch + WebFetch available; PubMed / Scholar / Consensus / bioRxiv /
  GitHub MCP not.** Consequence: academic-database evidence and MCP-database cells must be worked
  in a **connector-holding session** (like this one), not the autonomous cron; grey/national/
  standards/in-language web research *is* reachable autonomously. This plan therefore splits work
  into a **connector track** (interactive/this-session) and an **autonomous track** (cron).

## 4. The four completion requirements — how each is mechanically guaranteed

1. **Attempt every in-scope cell.** Done ⇔ every `lang_jur_map`-required cell has ≥1
   `search_executions` row (yield may be 0) **or** a non-NULL `deferred_reason`. Progress metric =
   *% required cells with ≥1 logged search* and *% saturated-or-deferred* — never "% reading
   SEARCHED." A logged, adversarially-constructed, zero-yield search is a completed unit of work
   (owner directive 2026-07-21: "okay if nothing surfaces so long as we know we tried hard").
2. **100% accuracy.** Enforced by a chain of existing gates, run every batch:
   - **Source reality:** every admitted source confirmed real; two failed searches →
     `CLOSED-DELETED`; quantified claims need DOI + page/table or `[UNVERIFIED-QUANT]`
     (CLAUDE.md §6 citation discipline).
   - **Locator re-retrieval:** DOIs/URLs must re-retrieve via a real tool call before a source
     advances (`resolve-dois` / `verify-urls`); no re-retrieval → not admitted.
   - **Adversarial pass (DR-2026-05-09/-05-13):** multilingual queries "naturally find
     translations of the same consensus" and non-English standards "may mirror ISO/EN/ADA without
     independent evidence" — so every multilingual admission gets an explicit adversarial
     term-combination and independence check before it counts.
   - **Vocabulary integrity:** no machine back-translation; AR/BN/HI/ID/SW terms carry
     `[UNVERIFIED-TERMS]` until authoritative-source or native-speaker verification (CO-0005;
     owner gate 4 resolved: authoritative-source sufficient, unconfirmed never asserted).
   - **Reproducibility:** `migrate_db.py --rebuild` byte-matches before push; the always-on
     `audit.yml` reproducibility gate re-checks on the PR.
   - **Verification-consistency:** run `scripts/audit/research_protocol_audit.py`,
     `validate_evidence_state.py`, `test_db_integrity.py`, `tools/evidentiary_audit.py` each
     batch; an audit-grade drop **pauses and surfaces** (loop methodology §5 escalation).
3. **Spillover routed to the correct slug.** A search for slug X routinely surfaces a source more
   relevant to slug Y (recent git log: "re-home 3 spillover sources", "narrow REF-00907
   attribution"). Every candidate is triaged to its **best-fit slug** before linking: add to
   `evidence_sources` once (dedup by DOI — see `dedup-audit-same-doi-multi-refid` workplan), link
   via `source_slug_links` / `evidence_population_match` to *whichever* slug(s) it actually
   evidences, and record the originating search on `search_executions.admitted_ref_ids`. Filing a
   source under the slug that happened to surface it, when it belongs elsewhere, is a
   **filing error** the batch audit flags (`source_slug_links_duplicates`, orphan-source check).
4. **Vet and backfill continuously.** Not a terminal phase — every batch: (i) re-verifies any
   "divergence"/prior-audit claim against *current* files before acting (CLAUDE.md §9 guardrail 1),
   (ii) backfills attestations/citations for any grandfathered artifact it touches
   (backfill-on-touch), (iii) mines backward/forward on admitted T1/T2/T3 anchors (`citation-miner`),
   (iv) converts newly-discovered holes into `gaps` rows rather than dropping them, and (v)
   re-runs the audit battery so drift is caught within the same batch, not a later sweep.

## 5. Phased execution (each phase = a batch class the loop pops; owner-gated at the marked gates)

**Phase 0 — Bridge + substrate (CONNECTOR TRACK; owner-gated ⚑).**
- **0a — Populate `lang_jur_map`** across all 48 jurisdictions with `role ∈ {official, regional,
  diaspora, lingua_franca}`, curated *from* the functional/jurisdictional facts (work-from-axes;
  no invented umbrellas). This defines required-vs-N/A and unblocks the priority queue.
  Deliverable: `lang_jur_map` non-empty; every (slug, jurisdiction, language) classifiable.
  *Data migration — not owner-gated for schema, but the role taxonomy is a DG-NON call (owner
  confirms the role vocabulary).* ⚑
- **0b — Stand up the logger.** Owner Gate 1 already resolved to **"thin append-only logger
  first, evolvable to full `search_executions` later."** Ship the minimum `search_executions`-shaped
  append table (STRICT + CHECK + `json_valid`) via a schema migration **+ mirrored Pydantic model**,
  plus the derived coverage views (`v_coverage_jurisdiction/-language/-branch`). Freeze legacy
  `search_coverage`/`search_languages` as read-only historical artifacts. **D-SCHEMA — owner
  sign-off on the migration + `schemas/*.py`.** ⚑
- **0c — Backfill what survives.** Migrate the ~47 recoverable query-bearing rows
  (`evidence_sources.search_queries_used` + `spec_value_probes.search_query` + derivation chains)
  into `search_executions` with `engine='manual'`, flagged `backfill`. Mark the rest explicitly
  unrecoverable (honest; the 640 SEARCHED / 33 THIN labels carry no query text).

**Phase 1 — Unblock the five dead languages (CONNECTOR TRACK; verification-gated).**
Build verified `term_aliases` for AR/BN/HI/ID/SW **only where `lang_jur_map` marks them required**
(e.g. HI/BN for IN/BD, AR for EG/MA, ID for ID). Authoritative-source verification, **no
back-translation**; anything unconfirmed stays `[UNVERIFIED-TERMS]` and is never asserted.
Extend `generate_search_queries.py` reach (`term_item_links`) so the generator reaches all in-scope
slugs/languages or logs a `deferred_reason`. **DoD:** generator reaches 19/19 languages or a logged
reason each stays deferred.

**Phase 2 — Drive the priority queue (BOTH TRACKS; bounded batches).**
Mission-value score = `3·population_thinness + 3·jurisdiction_role + 3·open_gap_bonus +
2·source_starvation + 2·branch_thinness(incl. never-run tier-6) + 1·language_underservice`.
Pop the highest, per batch (default **12 cells or 1 vocab/substrate build**). Batch order:
- **2a — the ungridded slug + OPEN gaps.** Seed `manoeuvring-footprint-vs-turning-radius-methodology`
  a coverage row; drive the **39 OPEN gaps** through `gap-driven-mining` with
  `gap_mining.search_strategy_record` written (table currently empty). Each becomes ≥1 logged search.
- **2b — never-run tier-6 / regulatory branch** for every required cell (`tier6_attempted=0`
  everywhere today) — targeted at least once per required cell, walled off from full-strength
  anchoring per the weak-band (○) rule (tier-system Option A).
- **2c — the language/jurisdiction long tail**, de-grade payload order: **within-corpus relinks
  (zero-fabrication) before net-new search**; empties kept; no forced full-band on
  genuinely-constrained slugs. **Autonomous cron handles grey/national/standards/in-language web
  cells; connector sessions handle PubMed/Scholar/Consensus/bioRxiv cells.**
- One adversarial pass every few batches (DR-2026-05-09); continuous vet/backfill per §4.4.

**Phase 3 — Saturation sweep + honest deferral.** Convert every remaining required cell to
`saturated` or `DEFERRED-WITH-REASON`; publish the five-axis coverage from the log. The loop
**self-disables** when the required-cell queue drains.

## 6. The autonomous mechanism (concrete)

- **Shape:** the ratified scheduled trigger, fresh session per bounded batch
  (`create_new_session_on_fire=true`), routine id `trig_01PBSBLySykFKYt2XhmQZJvt`
  ("Coverage-completion loop (guidebook)", daily `0 14 * * *` UTC). Each firing = one bounded,
  reviewable unit; self-throttles while a prior `coverage-loop:` PR is open (effective cadence =
  owner review speed); self-disables on drain.
- **Per-iteration mechanical steps:** pop cell → generate standard + adversarial queries → search
  on the matched engine → **log every fired query as one `search_executions` row before screening**
  (no silent searches; empties kept) → verify locators by real re-retrieval → **stage** candidate
  admissions / any figure a new source would move to a batch diff (never live) → saturation check +
  backward/forward mining → run the audit battery → open PR with the batch diff + audit delta.
- **Escalation gates (loop stops and asks):** a source would move an adjudicated/consensus figure
  → human + Opus synthesis; a cell needs new controlled vocabulary → Phase-1 vocab task with its
  own verification gate; multilingual admission pending adversarial verification; audit-grade
  regression → pause and surface.
- **Two tracks, one queue:** the autonomous cron pops only cells reachable with WebSearch/WebFetch
  (grey, national frameworks, standards bodies, government, in-language web); cells needing
  academic databases or GitHub MCP are tagged `connector-required` and worked in a connector-holding
  session. Both write the same `search_executions` log, so coverage is unified and derived.

## 7. Owner decision gates (⚑ — nothing past these executes without sign-off)

1. **Phase 0a role taxonomy** for `lang_jur_map` ({official, regional, diaspora, lingua_franca}
   and the per-jurisdiction assignments) — **DG-NON** (jurisdiction inclusion/scope is owner-only).
2. **Phase 0b `search_executions` schema migration + Pydantic model** — **D-SCHEMA**, CODEOWNERS
   (`scripts/migrations/`, `schemas/` are protected).
3. **Scope of the STUB slugs (23):** confirm they are in the completion denominator now, or defer
   them to a later batch class — **DG-NON** (work-product inclusion).
4. **Promotion of the cron from manual → daily:** already resolved to daily PR-gated, but the
   first 2–3 batches run manual to calibrate yield and fabrication surface before the cron is left
   to fire unattended (loop methodology §5 cadence).

Everything upstream of these gates (this plan; re-derivation of the facts in §1; the audit
battery) is non-mutating and proceeds now. Everything downstream is staged and PR-gated.

## 8. What this plan deliberately does NOT do

- Does **not** spin up a new register or a competing methodology — it executes the ratified loop.
- Does **not** hand-write coverage — coverage is derived from the `search_executions` log.
- Does **not** admit any source unattended that fails re-retrieval, move any adjudicated figure,
  ratify any gap, or invent vocabulary by back-translation.
- Does **not** author `best_practice_synthesis` from a non-Opus session — it queues at the boundary.
- Does **not** target coverage-to-green or quota parity — a logged, honest zero-yield search is a win.
