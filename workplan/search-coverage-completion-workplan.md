# Search-Coverage Completion Workplan

**Status:** Authoritative execution plan · **DB:** `data/guidebook.db` (read-only audit; one table family written forward) · **Baseline date:** 2026-06-22

> Mission: a multi-modal site that renders policy-grade, dynamically-weighted evidence whose methodology is fully transparent — you can show WHICH TERMS were searched, in WHICH JURISDICTIONS, in WHICH LANGUAGES, HOW DEEP, and across WHICH BRANCHES of the evidence-value hierarchy. This plan makes all five axes *completable* and *auditable*.

---

## 1. Objective & Scope

Make search/collection coverage **complete and transparent across five axes simultaneously** — Terms, Jurisdictions, Languages, Depth, and Evidence-Value-Hierarchy Branch — for the policy-grade corpus. Today coverage is a pair of disconnected, hand-maintained placeholder grids: `search_coverage` (81 slugs × 47 jurisdictions = 3807 rows, only 627 SEARCHED + 28 THIN ≈ 16.6% touched, depth = 3 booleans with `tier6_attempted=0` everywhere) and `search_languages` (81 × 19 = 1539 rows, 502 SEARCHED + 184 PARTIAL ≈ 44.6% touched), joined by **nothing** because `lang_jur_map` is empty (0 rows). No table records which of the 30 terms / 880 aliases were ever fired; verbatim query text survives in only ≈47 recoverable rows (20 `evidence_sources.search_queries_used` + 11 `spec_value_probes.search_query` + 16 `derivation_chain`). The objective is to replace placeholder grids with a **single logged event table (`search_executions`)** at the grain of one executed search, derive every coverage matrix as a VIEW over that log, populate `lang_jur_map` to bridge jurisdiction↔language, and drive execution by a mission-value priority queue until each prioritized cell reaches a defined saturation or a DEFERRED-WITH-REASON state. Scope covers forward coverage of all 82 ACTIVE slugs and honest backfill of the ≈47 query-bearing rows that survive; it explicitly excludes reconstructing un-logged history (the 627 SEARCHED rows, all THIN labels, and all of `search_languages`), which is term-wise unrecoverable.

---

## 2. The Coverage Model

### 2.1 Unit of coverage — the 5-axis cell

The atomic **coverage cell** is:

```
cell = (slug, jurisdiction, language, hierarchy_branch)
```

where `hierarchy_branch` is the existing, already-populated evidence-value vocabulary on `evidence_sources` — `tier` (1–6), `evidence_type` {clinical, sr_meta, standard_eb, national_fw, code, co1, co2, grey}, and `scope` {intrinsic, lower_control, high_control, national, international}. **Depth** is not a cell coordinate; it is a *measured attribute* of how thoroughly a cell was worked (queries fired, languages exhausted, backward/forward mining done, saturation reached). The full grid is intentionally large; §3–§4 define which cells are *required* vs *legitimately deferred*, so completeness is judged against the prioritized required set, never the raw Cartesian product.

### 2.2 The event table — `search_executions` (the single source of truth)

One row = one executed search. Coverage is never written by hand again; it is *derived* from this log (Standard S2). DDL sketch (STRICT, reusing the established STRICT pattern from `item_population_links` / `spec_value_probes`):

```sql
CREATE TABLE search_executions (
  exec_id            INTEGER PRIMARY KEY,
  slug              TEXT NOT NULL REFERENCES slugs(slug),
  jurisdiction      TEXT,                 -- NULL = jurisdiction-agnostic search
  language          TEXT NOT NULL,        -- ISO; one of the 19
  -- hierarchy branch the search TARGETED (diffable against what was FOUND):
  target_tier       INTEGER CHECK (target_tier BETWEEN 1 AND 6),
  target_evidence_type TEXT CHECK (target_evidence_type IN
    ('clinical','sr_meta','standard_eb','national_fw','code','co1','co2','grey')),
  target_scope      TEXT CHECK (target_scope IN
    ('intrinsic','lower_control','high_control','national','international')),
  -- the verbatim, replayable query:
  query_text        TEXT NOT NULL,
  terms_used        TEXT,                 -- JSON array of term_id, json_valid()
  engine            TEXT NOT NULL,        -- pubmed|crossref|scholar|biorxiv|medrxiv|wix|web|registry|manual
  -- depth, as real method not booleans:
  depth_method      TEXT NOT NULL CHECK (depth_method IN ('scoping','systematic')),
  mining_direction  TEXT CHECK (mining_direction IN ('none','backward','forward','both')),
  -- yield:
  results_found     INTEGER NOT NULL DEFAULT 0,
  results_screened  INTEGER NOT NULL DEFAULT 0,
  results_admitted  INTEGER NOT NULL DEFAULT 0,
  saturation_signal TEXT CHECK (saturation_signal IN ('none','partial','saturated')),
  admitted_ref_ids  TEXT,                 -- JSON array of evidence_sources.ref_id, json_valid()
  deferred_reason   TEXT,                 -- non-NULL => deliberate no-search for this cell
  session           TEXT NOT NULL,
  executed_at       TEXT NOT NULL DEFAULT (datetime('now')),
  CHECK (terms_used IS NULL OR json_valid(terms_used)),
  CHECK (admitted_ref_ids IS NULL OR json_valid(admitted_ref_ids))
) STRICT;
CREATE INDEX ix_se_cell ON search_executions(slug,jurisdiction,language);
CREATE INDEX ix_se_branch ON search_executions(target_tier,target_evidence_type,target_scope);
```

An FTS5 companion (`search_executions_fts` over `query_text, terms_used, deferred_reason`) gives free-text recall of "what did we ever search for X" (Standard S4 — FTS5 is greenfield here).

### 2.3 The bridge — populate `lang_jur_map`

`lang_jur_map(language, jurisdiction, role, notes)` is empty; until filled, the two grids cannot be crossed. **Phase 0 deliverable:** populate it across the 47 jurisdictions with `role ∈ {official, regional, diaspora, lingua_franca}`. This both (a) tells the priority engine which (jurisdiction, language) pairs are *required* vs *not applicable*, and (b) flags the 5 languages (AR, BN, HI, ID, SW) that have **zero** controlled-vocabulary aliases today, so vocabulary build-out is scheduled where the bridge says those languages matter.

### 2.4 Derived coverage views (replace the placeholder grids — S2)

```sql
-- jurisdiction coverage, formerly hand-kept in search_coverage:
CREATE VIEW v_coverage_jurisdiction AS
SELECT slug, jurisdiction,
       COUNT(*) AS searches, SUM(results_admitted) AS admitted,
       MAX(depth_method='systematic') AS reached_systematic,
       MAX(saturation_signal='saturated') AS saturated
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY slug, jurisdiction;

-- language coverage, formerly search_languages:
CREATE VIEW v_coverage_language AS
SELECT slug, language, COUNT(*) AS searches, SUM(results_admitted) AS admitted
FROM search_executions WHERE deferred_reason IS NULL GROUP BY slug, language;

-- hierarchy-branch coverage: TARGETED vs FOUND, per cell:
CREATE VIEW v_coverage_branch AS
SELECT se.slug, se.jurisdiction, se.target_tier, se.target_evidence_type, se.target_scope,
       COUNT(*) AS targeted_searches, SUM(se.results_admitted) AS admitted
FROM search_executions se WHERE se.deferred_reason IS NULL
GROUP BY 1,2,3,4,5;
```

The legacy `search_coverage` / `search_languages` tables are frozen read-only as historical artifacts; their numbers are superseded by these views.

---

## 3. Gap & Done Definitions

- **Uncovered (gap) cell:** a `(slug, jurisdiction, language, branch)` that the `lang_jur_map` bridge marks *required* (jurisdiction is in-scope for the slug, language has `role` for that jurisdiction) and that has **zero** non-deferred rows in `search_executions`. The 36 OPEN `gaps` rows, the 14 zero-source slugs, and the one slug with no coverage row at all (`manoeuvring-footprint-vs-turning-radius-methodology`) are pre-seeded as known gaps.
- **Searched (touched):** ≥1 logged `scoping` search.
- **Saturated (done):** a `systematic` search has been logged for the cell's required branches AND `saturation_signal='saturated'` (a query revision returned no newly-admitted sources) AND backward/forward mining (`mining_direction` ≠ 'none') has been attempted on admitted tier-1/2/3 anchors. `tier6_attempted=0` historically — tier 6 (codes/standards) must be explicitly targeted at least once per required cell before that cell can be "done."
- **DEFERRED-WITH-REASON (legitimate, not a gap):** a row with `deferred_reason` non-NULL — e.g. "language not official/diaspora for this jurisdiction per lang_jur_map," "no controlled vocabulary yet for AR/BN/HI/ID/SW — blocked on vocab build," "jurisdiction has no domestic regulatory instrument for this topic." Deferred cells are counted and surfaced, never silently dropped.

---

## 4. Prioritization — mission-value scoring (S1)

Each candidate required cell gets a score; the execution loop always pops the highest. Weights are tunable; initial model:

```
score = 3*population_relevance      -- item_population_links coverage thinness for the slug
      + 3*jurisdiction_relevance    -- lang_jur_map role (official=3, regional=2, diaspora=1)
      + 3*open_gap_bonus            -- slug/jurisdiction named in an OPEN gaps row
      + 2*source_starvation         -- slug in the 14 zero-source set => max; else 689-link density inverse
      + 2*branch_thinness           -- required branch with 0 admitted (esp. tier6, never run)
      + 1*language_underservice     -- language NOT-RUN/PARTIAL in legacy search_languages
```

A nightly materialized `v_priority_queue` view ranks cells. **First execution batches (named concretely):**

- **Batch 1 — Zero-source + no-grid slugs (highest starvation).** The 14 slugs with zero sources in `source_slug_links` plus `manoeuvring-footprint-vs-turning-radius-methodology`. For each, run EN + the official languages (per lang_jur_map) of its top-3 in-scope jurisdictions, targeting tiers 1–3 first, then tier 6 (codes). Closes the most policy-visible holes and proves the loop end-to-end.
- **Batch 2 — OPEN-gap cells.** The 36 OPEN `gaps` rows, run through `gap-driven-mining` with `gap_mining.search_strategy_record` finally written (table is currently empty). Each becomes ≥1 logged `search_executions` row regardless of yield.
- **Batch 3 — Tier-6 + cross-population thin branches.** Every required cell where `target_tier=6` has never been logged (universal today) and the global-south / cross-population / deaf-classroom thin areas. Simultaneously stand up controlled vocabulary for AR, BN, HI, ID, SW where the bridge says they are required, unblocking those languages.

---

## 5. The Execution Loop (repeatable search session)

1. **Pick next cell** — pop top of `v_priority_queue`.
2. **Generate queries** — run `scripts/generate_search_queries.py` (slug → `items.bpc_source_slug` → `term_item_links` → `term_aliases`, emitting `{language, standard_query, adversarial_query, terms_used}`). Known limits to fix in-loop: it reaches only **18 slugs** (extend `term_item_links` beyond its 50 rows / 27 mapped slugs) and **14 languages** (add the 5 missing-vocabulary languages). If a cell's slug/language is unreachable, either build the missing term links/aliases or log a `deferred_reason`.
3. **Execute via connectors** — fire queries on the matched engine: PubMed / CrossRef / Scholar / bioRxiv / medRxiv MCP for literature; web/registry for grey + national frameworks; per the `citation-miner` skill for backward/forward mining of admitted anchors; per `multilingual-search-remediation` for non-EN languages.
4. **Log EVERY search** — write one `search_executions` row per fired query *before* screening, capturing `query_text`, `terms_used`, `engine`, `target_*` branch, `depth_method`, `mining_direction`, and yields. No silent searches.
5. **Verify locators** — resolve DOIs/URLs via existing `resolve-dois.yml` / `verify-urls.yml` CI; only RESOLVED locators advance (today only 52/640 are live-URL-confirmed — raise this for newly admitted sources).
6. **Admit & score** — admitted sources land in `evidence_sources` with `tier/evidence_type/scope` set; `admitted_ref_ids` back-links them to the execution; `source_slug_links` connects content.
7. **Saturation check** — revise/expand the query; if no new admits, set `saturation_signal='saturated'`. Attempt mining on tier-1/2/3 anchors. Mark cell done or queue follow-up branches.
8. **Refresh views** — coverage views and `v_priority_queue` recompute automatically; the cell's status changes are now data-driven.

---

## 6. Transparency Surface

Anyone can answer "what did we search across all five axes?" from the log alone:

- **Per-cell:** `v_coverage_jurisdiction`, `v_coverage_language`, `v_coverage_branch` give touched/saturated/targeted-vs-found at a glance.
- **Per-term & verbatim query:** `search_executions.query_text` + `terms_used` + the FTS5 index answer "which terms/aliases fired, where, in what language, how deep."
- **Targeted-vs-found diff:** `v_coverage_branch` compared against admitted-source tiers shows where we *looked* for tier-6/codes but found nothing — the honest negative-result surface.
- **Per-source provenance:** every admitted source links back through `admitted_ref_ids` to the exact executed search (slug, jurisdiction, language, engine, query, session, date) — full chain of custody.
- **Publish:** expose the views via Datasette (read-only) for the methodology page; the site's "methodology" panel renders the five-axis coverage straight from these views, never from a hand-kept grid.

---

## 7. Phased Roadmap

- **Phase 0 — Foundations (DDL + bridge).** Create `search_executions` (STRICT + CHECK + json_valid), the FTS5 companion, the derived views; populate `lang_jur_map` for all 47 jurisdictions with `role` semantics. **DoD:** views return rows; bridge non-empty; legacy grids frozen.
- **Phase 1 — Backfill what survives.** Migrate the ≈47 recoverable query-bearing rows (20 `search_queries_used` + 11 `spec_value_probes.search_query` + 16 `derivation_chain`) into `search_executions` with `engine='manual'` and a `backfill` flag. **DoD:** every recoverable historical query is a logged event; remainder explicitly marked unrecoverable. *Honest note: the 627 SEARCHED rows, 28 THIN labels, and all 1539 search_languages rows carry no query text and are NOT reconstructable — they govern nothing forward.*
- **Phase 2 — Batch 1 (zero-source + no-grid slugs).** Run the loop for the 14 zero-source slugs + the 1 ungridded slug. **DoD:** each has ≥1 saturated required cell; orphan-source count addressed.
- **Phase 3 — Batch 2 (OPEN gaps).** Drive the 36 OPEN gaps with `gap_mining.search_strategy_record` written. **DoD:** 0 OPEN gaps without a logged search.
- **Phase 4 — Batch 3 (tier-6 + thin branches + 5 missing-vocab languages).** **DoD:** `target_tier=6` logged for every required cell; vocabulary exists for AR/BN/HI/ID/SW where required; generator reaches all in-scope slugs/languages.
- **Phase 5 — Saturation sweep.** Work the priority queue to exhaustion; convert remaining untouched required cells to saturated or DEFERRED-WITH-REASON. **DoD:** required-cell completion ≥ target with zero undocumented gaps.

---

## 8. Tracking & Enforcement

- **Progress metric:** `% of required cells saturated` and `% with ≥1 logged search`, computed live from the views — replaces the meaningless "16.6% / 44.6% touched" placeholder figures.
- **No placeholder drift:** the legacy tables are read-only; the only writable coverage object is `search_executions`. Coverage cannot be faked because it is derived.
- **CI / audit checks (extend existing workflows):**
  - reject any `search_executions` insert failing CHECK/`json_valid` (STRICT enforces).
  - audit: every admitted `evidence_sources.ref_id` appears in some `admitted_ref_ids` (no provenance-less sources); fail CI on orphans beyond the known 21.
  - audit: no required cell marked "done" without a `target_tier=6` row and a `saturation_signal` set.
  - locator gate: newly admitted sources must reach `url_resolution_outcome='RESOLVED'` (lift the 52/640 live-confirmed ratio over time).
  - drift check: assert legacy `search_coverage`/`search_languages` row counts are unchanged (frozen).
- **Honest backfill ceiling (restated):** ≈47 query rows recoverable; everything else forward-only. The plan governs what we search from here, transparently and completably.
