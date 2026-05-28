# DR-2026-05-28-b — `source_value_extractions` schema layer

**Status:** PROPOSED — adopted-in-effect by application of migration 018 this session; ratification by owner via review of this DR + surface confirmation.
**Authored:** 2026-05-28 (`session_2026-05-28-vetting-surface-and-extraction-layer`)
**Doctrine SHA at authorship:** `61c7f95`
**Companion to:** the spec-curation vetting surface (`spec-curation-vetting-surface.html`, this session).
**Relates to:** standing rule #10 (evidence verification gate); `reasoning_doc_citations` (the existing verification layer); `source_slug_links` (the bare-link layer).

---

## Context

The vetting surface generated in this session exposed a structural gap in the data model. Per-topic, the project records:

1. **`source_slug_links`** — "this source is relevant to this topic" (689 rows; the spread).
2. **`reasoning_doc_citations`** — "I re-read this source and confirm `value_match` = EXACT for parameter P, population Q, jurisdiction J" (7 rows, 1 topic; the synthesis-gate verification layer per rule #10 sub-rules 2/3).

Between these two there is no schema slot for the most-frequent unit of mining work: **what value does each linked source actually assert for the parameter, before full re-read verification?** A skim that captures "Source A says 0.6 s for primary classrooms" should be recordable as durable evidence — not lost in session prose — even when it has not yet gone through the rule #10 re-read.

Without that layer, the surface can show *which* sources are at hand and *whether their bibliography is valid*, but not the **spread of values** across those sources for any topic the synthesis hasn't already touched. That makes 67 of 68 topics functionally opaque to vetting, even when 20–33 sources sit linked to them.

The owner's spec for the vetting surface explicitly named this: *"I need to be able to see the spread of information you have at your disposal for each topic, what values you are taking from sources, what you are selecting for each topic, what you are selecting for each population."* The first two clauses are the missing layer.

---

## Decision

Add one table, `source_value_extractions`, between `source_slug_links` and `reasoning_doc_citations` in the verification chain. Schema migration `018_source_value_extractions.sql`; `user_version` 17 → 18.

### Table shape

```
source_value_extractions
  extraction_id          INTEGER PK
  ref_id                 TEXT NOT NULL          FK evidence_sources(ref_id)
  slug                   TEXT NOT NULL          (matches source_slug_links.slug — soft tie)
  parameter              TEXT NOT NULL          e.g. "RT60", "door clear width"
  parameter_canonical    TEXT                   normalized for join (lowercase, hyphenated)
  population_code        TEXT                   FK populations(population_code), nullable
  population_label       TEXT                   free-text qualifier
  jurisdiction           TEXT                   "UK", "US", "Multi", or NULL for clinical
  claim_type             TEXT NOT NULL CHECK    'numerical'|'range'|'qualitative'|'framework'|'absent'
  claimed_value          TEXT                   as stated; NULL when claim_type='absent'
  claimed_unit           TEXT
  claim_text             TEXT                   exact phrasing if relevant
  source_section         TEXT                   "Table 6, p.33", "§4.2"
  extraction_method      TEXT NOT NULL CHECK    'skim'|'full-read'|'re-read'|'auto-mined'
  extraction_status      TEXT NOT NULL CHECK    'preliminary'|'reviewed'|'verified'|'contradicted'|'absent-confirmed'
  promoted_to_rdc_id     TEXT                   FK reasoning_doc_citations(citation_id), nullable
  notes                  TEXT
  created_at, created_by_session, updated_at, updated_by_session
```

Indexes: `(slug, parameter_canonical)` for the per-topic surface pivot; `(ref_id)` for the per-source pivot.

### Verification chain (the role each layer plays)

| Layer | What it records | Status at mining |
|---|---|---|
| `source_slug_links` | this source is relevant to this topic | created at source-tier-assignment |
| **`source_value_extractions`** *(new)* | this source asserts value X for parameter P, population Q, jurisdiction J | **per-mining-act** |
| `reasoning_doc_citations` | re-read confirms `value_match` = EXACT / WITHIN-TOLERANCE | per-cell synthesis verification (rule #10) |
| `spec_value_probes` | the PMP walk that selected the curated value | per-item value-selection (rule #8) |
| `items.pmp_*` | the final curated spec value | per-item end-state |

A row in `source_value_extractions` with `extraction_status='verified'` and a non-null `promoted_to_rdc_id` is the bridge: the extraction graduated to the synthesis layer and the reasoning-doc cell points back.

### Append-friendly, not unique-constrained

Mirrors `supersession_check` (DR-2026-05-24) and `gap_mining` (DR-2026-05-26): multiple extractions per `(ref_id, slug, parameter, population, jurisdiction)` are allowed across time (preliminary → reviewed → verified). The operative row is the most recent `verified`, else the most recent. Application code (`scripts/db.py`, the vetting surface) implements this rule; the schema does not enforce uniqueness, preserving the audit trail of how an extraction evolved.

### Interlocks with existing rules

- **Rule #10 sub-rules 2/3 unchanged.** Synthesis claims still require a `reasoning_doc_citations` row with `value_match ∈ {EXACT, WITHIN-TOLERANCE}`. An extraction with `extraction_status='verified'` does **not** itself clear the synthesis gate — it must promote to `reasoning_doc_citations`, which then carries the gate-passing match verdict. This preserves the existing gate.
- **Rule #8 (PMP) unchanged.** Numerical spec selection still requires `spec_value_probes`. The new table feeds the *evidence pool* the PMP walk evaluates, but does not replace the walk's step record.
- **Rule #7 (adversarial research) unchanged.** Per-study population-match logging (`evidence_population_match`) is still required for synthesis-supporting evidence. A `source_value_extractions` row with `population_code` set is not a substitute.

### What this does *not* do (deliberately deferred)

- **No backfill this session.** 689 existing source-links remain without extractions. Backfilling is the actual mining work; the schema landing is the prerequisite. The vetting surface will continue to show un-mined topics honestly, with the new layer surfacing as `0 extractions` until populated.
- **No `db.py` CLI helpers this session.** The migration alone is sufficient. CLI subcommands (`add-extraction`, `list-extractions-for-topic`, `promote-extraction-to-rdc`) ship with the first mining session that needs them.
- **No PI rule change.** This is data-model armature, not a new standing rule. Per architecture v2.3 `<migration_and_growth>`, schema-only changes do not require a PI version bump.
- **No audit script this session.** Level-2 enforcement (e.g., orphan `promoted_to_rdc_id`, status transitions) is deferrable; rule #10 audits already catch downstream failures. An `extractions_audit.py` ships when the table has content to police.

---

## Mission test (abbreviated)

Verifiable (#7): every extraction carries `ref_id`, `source_section`, and `extraction_method` — what was looked at, where, and how — making each claim replayable from the cited source. Acknowledges non-uniformity (#2): the row shape preserves jurisdiction and population at the extraction level, so cross-jurisdictional spread becomes queryable from the moment evidence is captured rather than being inferable only after synthesis. Aligned with audience priority (#8): designers and disabled-people audiences read the curated synthesis, which is now traceable back through extractions to the exact source section — not just to "this source supports the claim."

---

## Deliverables

**This session:**
1. This DR.
2. `scripts/migrations/018_source_value_extractions.sql` (applied; `user_version` 17→18; table empty).
3. `schemas/source_value_extraction.py` (Pydantic mirror).
4. Vetting surface regenerated to surface the new layer (currently empty for all 68 topics).
5. Attestation.

**Next mining session:**
- `db.py` CLI helpers.
- First topic populated end-to-end as the pilot (most plausibly `room-acoustic-performance`, which already has `reasoning_doc_citations` rows — back-populating the extraction layer from those is mechanical and yields a worked example).
