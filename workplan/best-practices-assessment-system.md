# Best-Practices Assessment System — Design

**Status:** Design (authored directly, 2026-06-22, single-author; multi-agent panel deferred — monthly spend limit).
**Authority:** `governance/mission-PROVISIONAL.md` doctrine #2/#3/#4 + the 7-point test. This system *operationalizes* that doctrine; it does not invent a competing methodology.
**Core gap it closes:** the mission defines a per-cell best-practice determination, but `evidence_cell_state` is **empty (0 rows)** — the determination engine is unbuilt.

---

## 1. The principle

Your mission already prescribes *how* best practice is decided. "Best practice is determined by the evidence hierarchy, not code consensus" (doctrine #2), and every `(parameter × population)` cell must carry one of four states (doctrine #4): **`stated`** (≥Tier 3 OR Co‑1 OR Co‑2), **`provisional`**, **`pending`**, **`not_applicable`**. The system's job is to *apply* this consistently, dynamically, and auditably across all cells. It must never let a determination be "best practice" on Tier‑6 (code) evidence alone — code is the floor.

So the system = **a deterministic assessment function + a clean place to store its output + a dynamic presentation layer + enforcement gates.**

---

## 2. Unit of assessment — the cell

```
cell = (slug, population)        -- matches bpc_metadata + doctrine "(parameter × population)"
       [× jurisdiction]          -- optional refinement for policymaker jurisdiction-comparison
       [× design_mode]           -- Universal / Tier1 Population-Informed / Tier2 (doctrine #5)
```

`slug` is the parameter/topic (82 active); `population` is the disability group (22). Evidence reaches a cell via `source_slug_links (ref_id ↔ slug)` filtered to the population, with each `evidence_sources` row carrying `tier`, `evidence_type` {clinical, sr_meta, standard_eb, national_fw, code, co1, co2, grey}, `scope`, `directness`. (Confirm the exact slug→population attribution join during Phase 1 — it is the one structural dependency to nail.)

---

## 3. The determination algorithm (doctrine #2 + #3 + #4)

For each cell, deterministically:

1. **Gather** all admitted evidence for `(slug, population)` with tier + evidence_type + scope + directness + within-population range.
2. **Classify dimensions present:** clinical (Tier 1), lived-experience (Co‑1), OT‑CPG (Co‑2), systematic (Tier 3), standards/frameworks (Tier 4‑5), code (Tier 6).
3. **Assign state:**
   - `stated` ⟺ at least one of {≥Tier 3, Co‑1, Co‑2} is present **and** survives supersession.
   - `provisional` ⟺ partial — rich in ≥1 dimension but below the `stated` bar; render with confidence flag.
   - `pending` ⟺ sparse across all dimensions → emit `[BEST-PRACTICE-PENDING]` + link to a `gaps` row.
   - `not_applicable` ⟺ parameter has no design implication for this population → **explicit rationale required**.
   - **Hard rule (doctrine #2):** if the *only* evidence is Tier 6, the cell can never be `stated`. It becomes `provisional`/`pending` with a `code_floor_only = 1` flag and the code value recorded as the regulatory minimum, not the aspiration.
4. **Co‑1 / Tier‑1 reconciliation (doctrine #3):** if both present →
   - agree → `convergence` recorded as *itself* evidence (raises confidence);
   - disagree → `divergence` flag set + a `synthesis_approach` is **required** for the cell (rendered, not hidden).
5. **Within-population variability (doctrine #1):** the determination stores a **range**, not a point; median is the Tier‑1 default (doctrine #5).
6. **Falsification condition:** every `stated`/`provisional` cell records *what evidence would overturn it* (defends against the known BPC‑hallucination failure mode; ties to `gaps.falsification_condition`).

The function is **pure**: same evidence + same `rule_version` ⇒ same state. That is what makes it auditable and reproducible.

---

## 4. The data model — fill `evidence_cell_state` (clean data, S4)

**SUPERSEDED (2026-07-13):** the sketch below is superseded by the actual migration, per `decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md`'s own "Consequences if ratified" section: *"`workplan/best-practices-assessment-system.md` §4's SQL sketch is superseded by the actual migration; its phasing plan (§8) is otherwise unaffected."* The live schema (`scripts/migrations/026_reconcile_evidence_cell_state.sql`, `027_regulatory_stratum_only.sql`) keeps `evidence_cell_state`'s identity as `(item_code, population_code)` — not `(slug, population, jurisdiction)` as sketched below — and structures the within-population range as `value_min`/`value_max`/`value_unit` rather than a free-text `value_range`. Jurisdiction-specific values live in the separate `jurisdictional_values` table, deliberately not folded into this one (conflating a jurisdiction-agnostic best-practice determination with a jurisdiction-specific code floor is exactly the failure mode this schema exists to prevent — see `governance/tier-system.md` §3). The sketch is left below for the phasing-plan context (§8, unaffected); do not implement against it — implement against the live migrations.

Replace the empty table with a STRICT, CHECK-constrained, **derived** table (written by the assessment function, never by hand):

```sql
-- sketch; finalize as migration 026 -- SUPERSEDED, see note above; kept for phasing-plan context only
CREATE TABLE evidence_cell_state (
  slug            TEXT NOT NULL,
  population      TEXT NOT NULL,
  jurisdiction    TEXT,                       -- NULL = jurisdiction-agnostic determination
  state           TEXT NOT NULL CHECK (state IN ('stated','provisional','pending','not_applicable')),
  tier_basis      TEXT,                        -- e.g. 'T1+CO1' / 'T3' / 'T6-only'
  evidence_types  TEXT CHECK (json_valid(evidence_types)),   -- JSON array of dimensions present
  governing_refs  TEXT CHECK (json_valid(governing_refs)),   -- JSON array of ref_ids that establish it
  convergence     TEXT CHECK (convergence IN ('converge','diverge','single','none')),
  synthesis_approach TEXT,                      -- REQUIRED when convergence='diverge'
  code_floor_only INTEGER NOT NULL DEFAULT 0,
  value_range     TEXT,                         -- within-population range (doctrine #1)
  confidence      TEXT CHECK (confidence IN ('high','medium','low')),
  gap_id          TEXT REFERENCES gaps(gap_id), -- REQUIRED when state='pending'
  na_rationale    TEXT,                          -- REQUIRED when state='not_applicable'
  falsification   TEXT,
  rule_version    TEXT NOT NULL,                 -- which algorithm version produced this
  derivation_sha  TEXT NOT NULL,                 -- hash of (sorted governing_refs + rule_version)
  computed_at     TEXT NOT NULL,
  computed_by     TEXT NOT NULL,
  PRIMARY KEY (slug, population, jurisdiction)
) STRICT;
```

Derived **views** (the transparent surfaces, never drift):
- `v_best_practice` — current `stated`/`provisional` determinations with governing evidence.
- `v_pending` — `pending` cells joined to their `gaps` row (the live "what we owe" list).
- `v_divergence` — cells where Co‑1 and Tier‑1 disagree and a synthesis approach is owed.
- `v_code_floor_only` — cells resting only on code (the cells most needing better evidence).

Provenance is intrinsic: a row **cannot exist** without `governing_refs` (anti-hallucination), and `derivation_sha` makes "is this determination current for its evidence?" a one-query check.

---

## 5. Dynamic weighting — same evidence, user-conditioned framing (S1)

The **determination is fixed**; the **emphasis re-ranks** by audience × use-pattern (the mission's dynamic-weighting goal). A small profile table parameterizes a view — it changes *what is foregrounded*, never the 4‑state verdict (code stays the floor for everyone, so no profile can manufacture best practice from code):

| Audience · use-pattern | Weighting profile |
|---|---|
| Designer · aspiration/decision-frame | emphasize Tier 1 + Co‑1; show best-practice value *above* code; surface DAR provisions |
| Disabled person · representation-checking | foreground Co‑1; answer "is my lived experience acknowledged here?" |
| Policymaker · jurisdiction-comparison | surface Tier 4‑6 + per-jurisdiction values; show the code‑vs‑best‑practice **delta** |
| OT · specialist-handoff | emphasize Tier 1 clinical + Tier 1 range for Tier‑2 person-specific resolution |

```sql
CREATE TABLE weighting_profile (
  audience TEXT NOT NULL, use_pattern TEXT NOT NULL,
  tier_weights TEXT NOT NULL CHECK (json_valid(tier_weights)),  -- per-tier/evidence_type emphasis
  notes TEXT, PRIMARY KEY (audience, use_pattern)
) STRICT;
```
The site queries `evidence_cell_state` through the active profile to render a user-conditioned view — this is the "dynamically interpret the table per user requirements" mechanism, made sound.

---

## 6. Mission test as enforcement gates (S2 verifiable)

Encode doctrine + the 7-point test as an audit script (`scripts/audit/best_practice_integrity.py`, exit 1 on violation; promote to blocking CI):

1. No cell `stated` on Tier‑6-only evidence (doctrine #2). 
2. Every non-`not_applicable` cell has a determination **or** a `[BEST-PRACTICE-PENDING]`+`gap_id` (doctrine #4 "silence is not the default").
3. Every `diverge` cell has a `synthesis_approach` (doctrine #3).
4. Every `not_applicable` has `na_rationale`; every `stated`/`provisional` has `governing_refs` that resolve to verifiable rows (test #7 clean data).
5. Every `stated`/`provisional` has a `falsification` condition.
6. `derivation_sha` current vs the live evidence set (flags stale determinations after new evidence/supersession).

---

## 7. The assessment process (repeatable loop)

```
trigger (new admitted evidence | supersession event | scheduled re-assess)
  → for each affected (slug, population):
       gather evidence → run determination fn → upsert evidence_cell_state (via migration/controlled writer)
       → run §6 gates → route diverge/pending to human synthesis queue
  → views refresh automatically
```
Integrates downstream of the **search-coverage pipeline** (coverage admits evidence → evidence triggers re-assessment) and with `citation-verifier` / `supersession_check`. Determinations are **forward-written** (migration discipline), so the determination history is itself reproducible.

---

## 8. Phasing

- **Phase 0 — schema:** migration 026 = STRICT `evidence_cell_state` + `weighting_profile` + the four views + CHECK/json_valid. (low risk)
- **Phase 1 — engine + backfill:** implement the pure determination function; nail the slug→population→evidence join; backfill all `(slug × population)` cells that have evidence; emit `pending`+gap for the rest. This is where the *first real best-practice table* comes into existence.
- **Phase 2 — gates:** `best_practice_integrity.py` audit → blocking CI.
- **Phase 3 — dynamic weighting:** seed `weighting_profile` for the 4 audience use-patterns; parameterized rendering view.
- **Phase 4 — surface:** per-audience "why is this best practice?" view (Datasette/site), showing governing evidence, code-floor delta, within-population range, and divergence synthesis.

**Honest limit (doctrine §3):** pre-launch, Co‑1 is engaged at the *evidence* level only (published corpus), not participation. Every Co‑1-governed determination records this partial-honoring limit; it is declared, not hidden.

---

## 9. Why this is "proper" by your own test

It grounds best practice in the hierarchy not code (#3); surfaces where Co‑1 vs Tier‑1 govern, converge, and diverge (#4); never goes silent on thin evidence (#4 → `pending`); keeps data verifiable and methodology declared (#7 → `governing_refs` + `rule_version` + `falsification`); and teaches rather than dictates by exposing the evidence and the range rather than a single imposed number (#1, #6). Every determination is a reproducible, falsifiable, provenance-bearing artifact — policy-grade by construction.
