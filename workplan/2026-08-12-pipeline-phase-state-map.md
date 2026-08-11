# 2026-08-12 — What the data looks like at each phase, and how it moves between them

**CONTENT VALIDITY:** NOT CONTENT — STRUCTURAL TEST ARTEFACT, NOT ADMISSIBLE AS EVIDENCE
(Owner directive 2026-08-12: pre-existing items must not seed content research. Every numeric
value, `REF-9xxxx` identifier, standard name and locator below was used to exercise the machine,
not to establish a fact. Values were copied from rows already in `jurisdictional_values`; none
was independently re-retrieved, no DOI was pre-checked, no locator re-verified — so R3, R9 and
R10 are unsatisfied by construction. **Nothing here may be mined, promoted, cited, or treated as
a starting point for a corridor-width, turning-space or swept-path determination.** The findings
this document reports are about structure and stand independently of the values used to reach
them.)

**Derived from:** the corridor-width / turning-radius walk of 2026-08-12. Every row count and
every column name below was observed in that run, not read off a design document. The complete
action/IO log is `workplan/2026-08-12-pipeline-walk-trial-log.md`; the analysis is
`workplan/2026-08-12-commit-91-adversarial-review.md`.

**Subject:** `E-08 — Corridor Clear Width`, topic `accessible-circulation-geometry`, with a
second thread on `E-12` for turning radius vs swept path.

**How to read this.** Each phase gets: what exists when it starts, what it writes, **what key
carries the work forward**, and what is lost or unenforced at the boundary. The handoff column
is the important one — a pipeline is only as strong as the key each stage passes to the next.

---

## The spine, in one diagram

```
  items ──┬─ item_bpc_links ─┐
          │  (FK, FK)        │
          └─ item_population_links (FK)
                             │
                          slugs ──── search_executions ─── search_admissions
                             │          (FK slug)            (FK exec_id, FK ref_id)
                             │                                       │
                    source_slug_links ─────────────────────── evidence_sources
                       (FK ref, FK slug)                        (PK ref_id)
                             │                                  │        │
                             │                    source_value_extractions│
                             │                     (FK ref, slug, item,   │
                             │                      population_code)      │
                             │                                            │
                             │                          evidence_population_match
                             │                           (FK ref_id · target_population
                             │                            has NO KEY  ◀── BROKEN LEG)
                             │
                    ┌────────┴─────────┐
                    │  assess_cell.py  │  ◀── reads slug + tier + evidence_type ONLY
                    └────────┬─────────┘      never reads extractions, values, paradigms
                             │
                    evidence_cell_state ──── cell_source_links ──── evidence_sources
                    (FK item, FK population)   (FK cell, FK ref)
                     governing_refs = JSON  ◀── NEVER JOINED. Dual store, writer fills
                     value_min/max/unit     ◀── WRITTEN AS NULL, ALWAYS
                             │
                       spec_page.py  ──▶  site/specs/e-08.html
                       (reads the junction, not the JSON)
```

Two legs of `DR-2026-08-06 §1`'s four-leg promise have no key at all: **the population served**
(`target_population`, free text) and **the doctrine that governed the judgement** (no column
exists anywhere).

---

## Phase 1 — Topic & taxonomy creation

| | |
|---|---|
| **Starts with** | `items` 93 rows, `populations` 23, `slugs` 106, `item_population_links` 372, `item_axis_links` 158 — the pre-content skeleton, all populated |
| **Writes** | `item_bpc_links` (item_code, slug, link_type ∈ primary/parameter/context/secondary) |
| **Observed** | 0 → 1 row. E-08 ↔ `accessible-circulation-geometry`, `primary` |
| **Carries forward** | `slug` |

**State of the data.** E-08 already carried `items.bpc_source_slug = 'accessible-circulation-geometry'`
as a denormalised text pointer. `item_bpc_links` — the FK-valid bridge — held **zero rows across
the whole corpus**. Both now say the same thing.

**What is lost at the boundary.** Nothing, but note the duplication is live: two representations
of one fact, one keyed and one not, and `spec_page.py` reads the keyed one while
`assess_cell.py` reads neither — it takes the slug from a source-code literal.

---

## Phase 2 — Scope & question framing

| | |
|---|---|
| **Starts with** | a slug |
| **Writes** | `bpc_metadata` (slug PK, population, pico_complete, search_complete, bpc_complete, citation_mining_complete, supersession_check_complete, closure_definition_version) |
| **Observed** | 0 → 2 rows |
| **Carries forward** | `slug` + closure flags |

**Where it narrows the world.** `bpc_metadata.population` is **singular** and **un-keyed** —
`TEXT NOT NULL`, no FK. E-08 has thirteen populations in `item_population_links`; the scope row
can name one. I set `MOB` because the column forces a choice the domain does not have.

**Probe result.** I filed a second scope row with `population = 'NOT-A-REAL-POPULATION'`.
Accepted, no error. The same concept is FK-keyed in four other tables.

---

## Phase 3 — Search execution

| | |
|---|---|
| **Starts with** | a slug and a scope |
| **Writes** | `search_executions` (exec_id, slug FK, language, target_tier, target_evidence_type, target_scope, **query_text**, engine, depth_method, results_*, admitted_ref_ids JSON, findings_note) |
| **Observed** | 0 → 1 row |
| **Carries forward** | `exec_id` |

**The best-defended table in the schema.** `STRICT`, with real CHECK constraints on
`target_tier` (1–6), `target_evidence_type` (the 8-value enum), `target_scope`, `depth_method`
and `saturation_signal`, and it stores the query verbatim so a stranger can replay it.

**The asymmetry worth naming.** The *search* has a tier vocabulary enforced by CHECK. The
*source it admits* does not — `evidence_sources.tier` is a bare INTEGER (Phase 5).

---

## Phase 4 — Screening & admission

| | |
|---|---|
| **Writes** | `search_admissions` (exec_id FK, ref_id FK, PK both) |
| **Observed** | 0 → 7 rows, after two failures |
| **Carries forward** | `ref_id` |

**The stage order is not what the documentation says.** `search_admissions.ref_id REFERENCES
evidence_sources(ref_id)`, so admission cannot complete before the source exists. The real order
is **4a → 5 → 4b**.

**Two breaks live here.** Attempting 4 before 5 produced `ERROR: 1 new FK violations`, exit 1 —
**and wrote the row anyway, and ledgered the migration** (Break 1). Re-submitting the identical
violation with the word "bootstrap" in the summary was accepted at exit 0 (Break 2). The
corrected 7-row admission then collided on the primary key of the row that "had not been
written", failed, and wedged the queue (Break 3).

---

## Phase 5 — Source verification

| | |
|---|---|
| **Writes** | `evidence_sources` — 90+ columns |
| **Observed** | 0 → 10 rows (7 code standards, 2 T1 paradigm sources, 1 illegal probe) |
| **Carries forward** | `ref_id` |

**Where the vocabularies stop being enforced.** `evidence_sources` has CHECK constraints on
`scope`, `data_capture_status`, `citation_mining_status`, `processing_blocked_reason`,
`verification_disposition`, `verification_method` and `verification_closure_reason` — and
**none on `tier` and none on `evidence_type`**, the two columns the entire doctrine turns on.

**Probe result.** `tier = 99`, `evidence_type = 'not-a-real-evidence-type'` — accepted, and it
persists. This is where the audited document's fabricated `T99` band came from.

The seven corridor sources are all `tier = 6`, `evidence_type = 'code'`, `scope = 'international'`,
`verification_status = 'VERIFIED'`.

---

## Phase 6 — Citation mining

| | |
|---|---|
| **Writes** | `citation_mining` (slug FK, local_ref_id, global_ref_id FK, backward, forward, **connections_produced**, deferred_reason) |
| **Observed** | 0 → 7 rows |

**The one un-keyed exit.** `connections_produced` is a JSON array of connection ids with **no
foreign key** to `connections`. It is the only link from mining into the connection layer, and
it is a string.

---

## Phase 7 — Value extraction

| | |
|---|---|
| **Writes** | `source_value_extractions` — the richest table in the schema |
| **Observed** | 0 → 9 rows |
| **Carries forward** | `extraction_id` — **which nothing downstream consumes** |

**This is where the real numbers finally exist**, and where the schema is at its most ambitious:

- `claimed_value`, `claimed_unit`, `claim_type` (numerical/range/qualitative/framework/absent)
- **`measurement_paradigm`** ∈ `swept_path_dynamic`, `static_turning_circle`, `static_clearance`,
  `anthropometric_percentile`, `instrumented_physical_measurement`, `route_metric`,
  `field_observation`, `participatory_spatial`, `stated_unmeasured`
- **`device_class`** ∈ manual/power/scooter/bariatric/walker/mixed
- `root_type` ∈ `measurement_primary`, `participatory_finding`, `committee_assertion`,
  `derived_calculation`, `untraced`; plus `root_ref_id`, `echo_of`, **`contested`**
- sixteen `loc_*` columns — the full locator hierarchy from migration 053

**The observed data:**

| ref | jurisdiction | value | paradigm | locator |
|---|---|---|---|---|
| REF-90001 | ISO | 1200 mm | static_clearance | 8 / 8.2 |
| REF-90002 | GB | 1200 mm | static_clearance | 5 / 5.4 |
| REF-90003 | DE | 1500 mm | static_clearance | 4 / 4.3.3 |
| REF-90004 | AU | 1000 mm | static_clearance | 6 / 6.3 |
| REF-90005 | NO | 1500 mm | static_clearance | 12-6 / 12-6(2) |
| REF-90006 | US | 915 mm | static_clearance | 403 / 403.5.1 |
| REF-90007 | — | **9999 mm** | *(none)* | *(all 16 NULL)* |
| REF-90010 | — | 1500 mm | **static_turning_circle** | 3.2 |
| REF-90011 | — | 1830 mm | **swept_path_dynamic** | 4.1 |

**Two things are unenforced.** Migration 053's locator hierarchy has **no enforcer anywhere in
the repository**: the `9999` row has all sixteen `loc_*` columns NULL, `extraction_method =
'skim'` and `extraction_status = 'verified'`, and nothing objects. And the `skim` → `verified`
transition is unguarded.

**What is lost at the boundary — this is the largest single loss in the pipeline.**
Nothing downstream reads this table. `assess_cell.py` never opens it. So `claimed_value`,
`measurement_paradigm`, `device_class`, `contested`, `echo_of` and all sixteen locator columns
**stop here**. The most carefully designed table in the schema is a terminus.

---

## Phase 8 — Population matching & directness

| | |
|---|---|
| **Writes** | `evidence_population_match` (match_id PK, ref_id FK, **target_population — no FK**, study_population, sample_size, match_grade ∈ EXACT/PARTIAL/PROXY/MISMATCH) |
| **Observed** | 0 → 8 rows |
| **Carries forward** | a **regex match**, not a key |

**The broken leg.** The consumer is `assess_cell.py:180`:

```python
if target and _re.search(rf"\b{_re.escape(population)}\b", target, _re.I):
```

**Probe result.** `target_population = 'WHEELCHAIR-USERS-GENERALLY'` was accepted — a broad
umbrella of exactly the kind `governance/functional-taxonomy.md` §3.3 and the 2026-07-22
work-from-axes rule prohibit. And it fails *silently*: the string contains no population code,
so the regex matches nothing and the row reads as **absent** rather than **malformed**.

All seven code sources were graded `PROXY` per R13 — committee standards with no study
population.

---

## Phase 9 — Cell determination

| | |
|---|---|
| **Writes** | `evidence_cell_state` (UNIQUE(item_code, population_code)) + `convergence_assessment` + `gaps` |
| **Observed** | 0 → 2 rows — **written by hand**, because no tool could |

**There is no general writer.** `scripts/assess/assess_cell.py` is the only determination engine
and its cells are a module-level literal of seven hardcoded `(item, population, slug)` triples.
The `item_bpc_links` bridge built in Phase 1 is never consulted. Then the run aborts anyway:
`next_gap_id` returns `GAP-1` on the post-reset empty `gaps` table, and
`schemas/evidence_state.py` requires three or four digits.

**What the engine reads when it does run:** `source_slug_links` → `evidence_sources`, taking
`tier`, `evidence_type`, `co1_source_type`, `verification_status`, `scope`, `jurisdiction`. That
is all. `classify()` buckets on `tier` and `evidence_type` alone.

**What it writes for the value:**

```python
… tier_basis, governing_refs, rule_version, derivation_sha, code_floor_only,
value_min, value_max, value_unit, falsification_condition, …
#            None,      None,       None      ← unconditionally
```

**The pipeline determines a state, never a number.** There is no code path anywhere from N
extracted values to one determined value.

**The dual store diverges here.** `governing_refs` holds a 7-element JSON array;
`cell_source_links` holds **0 rows**. `assess_cell.py` writes the JSON and never the junction;
three renderers read the junction and never the JSON.

**The observed determinations:**

| cell | state | tier_basis | code_floor_only | regulatory_stratum_only | value | gap |
|---|---|---|---|---|---|---|
| E-08 × MOB | `stated` | `T6-only(regulatory_stratum_only)` | 1 | 1 | 1200–1500 mm | — |
| E-08 × DEAFBLIND | `pending` | — | 0 | 0 | — | GAP-901 |
| E-08 × LPA *(and 10 others)* | *no row* | | | | | |

---

## Phase 10 — Synthesis

| | |
|---|---|
| **Reads** | a determination |
| **Writes** | `references/bpc/<topic>/<slug>.md` and `references/bpc-reasoning/<slug>.md` |
| **Carries forward** | **a filename stem** |

**Two artefact chains, joined by no key.** The file chain and the DB chain never meet:
`validate_reasoning.py` globs `*.md` and never opens the database; `validate_bpc.py` likewise
(`grep -c sqlite3` → 0 and 0). A reasoning doc can name a BPC that does not exist.

**Nothing enforces the entry contract.** No registered check reads a cell-state row as a
precondition for a BPC or reasoning-doc commit.

**This is also where the value is actually decided** — in prose, by a human, under the Opus
floor, with no input contract and no acceptance condition.

---

## Phase 11 — Adversarial QA & audit

| | |
|---|---|
| **Observed** | `test_db_integrity` 70/70 · `validate_evidence_state` pass · `validate_bpc` 102/102 · `pmp_audit` pass — **all green with the walk's contradictions in place** |

Green against: a `tier = 99` source, a `9999 mm` unlocated extraction claiming `verified`, an
un-keyed umbrella population, a determination whose 7 governing sources are invisible to every
reader, and two T1 sources disagreeing 1500 vs 1830 on the same parameter with `contested = 0`.

---

## Phase 12 — Render

| | |
|---|---|
| **Reads** | `items`, `item_population_links`, `item_bpc_links`, `bpc_metadata`, `evidence_cell_state`, `cell_source_links` |
| **Writes** | `site/specs/e-08.html` |

**Renders correctly:** all thirteen populations with applicability · State · Tier basis · Code
floor only · **Regulatory stratum only** (`yes`) · Falsification condition · an honest-banner
fallback when a determination has no sources.

**Does not render:** the value (no column exists for it) · any `●`/`◐`/`○` marker · the
`[BEST-PRACTICE-PENDING]` token · the `GAP-901` link · any governing source.

**The net effect on the page:** a determination that says *corridor clear width for people with
mobility needs is stated on a code-only basis, flagged regulatory-stratum, and here is what would
overturn it* — carrying **no number, no evidence band, and a statement that it has no governing
sources**, which is false.

---

## The handoff table — what each boundary passes, and what it drops

| boundary | key passed | integrity | what stops here |
|---|---|---|---|
| 1 → 2 | `slug` | FK | — |
| 2 → 3 | `slug` | FK | the other twelve populations (scope is singular) |
| 3 → 4 | `exec_id` | FK | — |
| 4 ↔ 5 | `ref_id` | FK, **but order-inverted and enforced post-commit** | — |
| 5 → 6 | `ref_id` | FK | — |
| 6 → connections | `connections_produced` | **JSON string, no FK** | the mining→connection link |
| 5 → 7 | `ref_id` | FK | — |
| **7 → 9** | *nothing* | **no consumer** | **every value, paradigm, device class, contested flag and locator** |
| 8 → 9 | regex over prose | **no FK** | malformed populations, silently |
| 9 → 12 | `cell_id` | FK | **`governing_refs` — written to JSON, read from the junction** |
| 9 → 12 | — | — | **`value_min`/`value_max`/`value_unit` — never written, never rendered** |
| 12 → reader | `item_code` + `population_code` | UNIQUE | the marker band, the gap link, the sources |

**Three of the twelve boundaries pass nothing usable**, and they are consecutive: the value
leaves the pipeline at 7, the population leg is a regex at 8, and the number is never written
at 9. Everything downstream of phase 7 is reasoning about *how well evidenced* a cell is,
detached from *what the evidence said*.
