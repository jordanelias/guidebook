# HANDOFF — evidence migration & rehabilitation program

*Written 2026-07-18 for a fresh context. Self-contained: a cold session should be able to resume from this
document + the two it points to (`pipeline-audit.md`, `/root/.claude/plans/delegated-pondering-pine.md`).*

---

## 1. What the project is (in one paragraph)

The Guidebook is a **radically transparent gatherer, not an authority** — it helps people ask better
questions about accessible/inclusive design, held to CRPD + Kawa (ethics) and PRISMA (rigour). Every
provision needs **two layers** — a performance **TARGET** and the design **TECHNIQUE** to achieve it — each
**evidence-graded** on a **seven-tier hierarchy** (T1 primary research and **Co-1 lived experience** are
co-primary; T2 synthesis/standards and Co-2 OT CPGs; T3 lower-control; **T4–6 = the regulatory stratum,
"convergence-not-evidence," walled off from best-practice anchoring**). Values are produced in **three
modes** — Universal (top-down floor), Population (evidence range, median default), Person (OT resolving the
person's position *within* the Population range) — and presented through **multimodal lenses** for four
audiences. English carries **no** evidential weight. Grading authority = the canonical DB
(`data/guidebook.db`); the website is a **non-canonical render** (shape, never grade).

## 2. Pipeline state at a glance (see `pipeline-audit.md` for the full survey)

**Shape: wide-top, narrow-bottom, hollow-shell.** Doctrine + gathering are ~complete; the
extraction→grading→modes midstream is **pilot-only (~7% of items)**; the render is 87 pages over 7 graded
items. The English skew is manufactured in **ingestion**, not search.

| link | state | one-number |
|---|---|---|
| doctrine | complete, highest rigour | 25+ DR records; S1–S8 added this session |
| language search | done | `search_languages` 1539 = 19 langs × 81 slugs |
| **ingestion (bias funnel)** | **the leak** | 14 langs returned hits; corpus still **551 EN : 89 non-EN** |
| citation-mine / supersession | ~7% | 7 / 6 slugs |
| **extraction / grading** | **the throat** | extractions **1 slug**; cells **7 / 93 items** |
| connections (post-grading) | 273 over ungraded items | generative loop; owe re-validation once graded |
| modes | Person ~0 | design_scale person **0**; `pmp_delta` 2/93 |
| lenses | spec 100%, applied ~7% | `weighting_profile` 5 rows / 4 audiences |
| website | shell 93%, backed 7% | `site/specs` **87** pages |
| governance | rigorous; attestation stale | `data_migrations` 196; CI non-blocking-fail |

**Focus (confirmed): evidence curation (widen the grading throat) · data migration (flag reconciliation +
ingest non-English backlog + fix flagged errors) · bias management (the ingestion funnel + Global-South
zero-results + Co-1 skew).**

## 3. What this session did

- **Authored + hardened the migration plan** (`/root/.claude/plans/delegated-pondering-pine.md`), approved,
  through many agonist→antagonist passes. It carries S1–S8 (values from evidence+precedents, converge≠evidence,
  three modes, top-down/bottom-up, DAR), the Part V·5 CRPD/Kawa/A10 ethics gate, the transparency model
  (all jurisdictions/standards/precedents · admit extrapolation · admit thin base), and a **Stage −1
  substrate inventory** (added after the pilot — see lesson 1 below).
- **L0 registry reconciliation** (`registry-reconciliation.md`): the vague "37 stranded refs" → **1 live
  hole (REF-00181/f-07)**, **~35 registered-but-un-migrated** (several non-English), **~11 cruft**. Plus a
  proposed (un-applied) jurisdiction-hygiene migration.
- **Pilot: A-18 (RT60)** through the pipeline with a **separate guilty-until-proven verifier**, which
  **caught real errors** in the first draft → corrected. See `pilot-A18-rt60/` and lesson 1.
- **Full pipeline audit** (`pipeline-audit.md`) — this session's closing analysis.
- **PRs:** #13 merged (first-draft pilot + L0). **#14 OPEN** (the corrections + this audit + handoff).

## 4. Corrected key findings — READ BEFORE TRUSTING OLD FRAMING

The migration plan's Part I.b and the early pilot framing contain claims this session **disproved**:

1. **"grading ≠ rehabilitation / A-18 needs everything" was overstated.** A-18 already has a deep, correct
   substrate (4 population-coded cells, 8 code+evidence extractions with `echo_of` provenance, 13 PMP
   derivation walks, convergence assessments). Its real debt: flags not flipped, **Co-1 genuinely absent**,
   and two DB-flagged data errors.
2. **"code-floor values un-migrated" — FALSE.** They live in `source_value_extractions` / `spec_value_probes`
   / `jurisdictional_values`. The first draft checked only `evidence_sources.bpc_note`.
3. **"jurisdictions_searched 0/82 = no search done" — FALSE.** `search_languages` (1539) + `search_coverage`
   (3807) show the search ran; the flag is decorative.
4. **The English skew is an INGESTION artifact, not a search failure** — search surfaced 14 languages of
   results; curation kept English.
5. **`bpc_metadata` flags are unreliable in both directions** — never trust them without checking the
   substrate tables.

## 5. DB substrate map (where the truth actually lives)

`data/guidebook.db` — use **`python3` with the `sqlite3` module** (there is **no** `sqlite3` CLI). All
writes go through **migration-based writes** (`governance/migration-based-writes-adopted-2026-05-11.md`;
ledger `data_migrations`, 196 rows) — never ad-hoc UPDATE.

| layer | tables | coverage |
|---|---|---|
| sources | `evidence_sources` (640; 635 VERIFIED), `evidence_source_authors` (1244), `source_slug_links` (689) | broad |
| slugs/items/pops | `bpc_metadata`/`slugs` (82), `items` (93; `bpc_source_slug` maps to slug), `populations` (22), `item_population_links` (366), `item_population_elaborations` (7/4 items) | broad, flags unreliable |
| **gathering** | `search_languages` (1539), `search_coverage` (3807; 3152 NOT-RUN), `citation_mining` (107/7 slugs), `supersession_check` (134/6) | wide (lang), partial (juris) |
| **grading** | `source_value_extractions` (8/1 slug), `spec_value_probes` (31/3 slugs), `convergence_assessment` (10), `evidence_cell_state` (11/7 items), `jurisdictional_values` (109/20 items), `evidence_population_match` (28) | **pilot-only** |
| presentation | `weighting_profile` (5/4 audiences) | spec complete |
| connections (post-grading, generative) | `connections` (273), `connection_targets` (507) | built pre-grading — re-validate + let them surface new specs |
| cross-cutting | `gaps` (297; 37 OPEN), `terms` (30)/`term_aliases` (880)/`term_item_links` (50) | active, all stages |
| provenance | `data_migrations` (196), `pipeline_runs` (15), `item_audit_runs` (87), `url_verification_runs` (9) | rigorous |

**Key joins:** slug→items via `items.bpc_source_slug`; item→grading via `evidence_cell_state.item_code`;
cell→convergence via `evidence_cell_state.convergence_id`; slug→values via `source_value_extractions.slug`
and `spec_value_probes.slug/item_code`. `evidence_cell_state.population_code` (NOT `population`) holds
DEAF/ALL/DEM/AUT.

## 6. Concrete next steps (in priority order)

1. **Substrate inventory across all 82 slugs (cheap, do first).** For each slug, count rows in
   `search_languages`, `citation_mining`, `source_value_extractions`, `spec_value_probes`, and cell-states
   (via items). Produce a per-slug readiness table: *gathered? processed? extracted? graded?* This
   right-sizes the true debt and drives batch ordering. (Partly done in `pipeline-audit.md`; make it
   per-slug.)
2. **Flag reconciliation migration.** Flip `bpc_metadata` flags to match the substrate (e.g.,
   `jurisdictions_searched`/language-search where `search_languages` rows exist) so state is legible.
3. **Widen the grading throat.** Take the next batch of slugs that already have gathering+citation substrate
   (the 6–7 citation-mined slugs: mobility-built-environment, mental-health-built-environment,
   stair-ramp-threshold-biomechanics-accessibility, cognitive-wayfinding-design, plus circadian-lighting &
   school-environment-autism which already have PMP walks) through extraction→grading with the separate
   verifier. **Validate the verifier with seeded plants first** (plan Part VII; task #4).
4. **Ingestion funnel repair (bias).** Reconcile `search_languages` non-EN hits (1153) against
   `evidence_sources` non-EN (89); ingest the gap; investigate the 5 zero-result Global-South languages;
   correct `lang_detected` mislabels.
5. **Fix flagged data errors.** REF-00571 (Kotloski 2020) is mis-cited as Devos 2019 in
   `item_population_elaborations` elab_id=6 (real Devos = REF-00735, unlinked); dedup the four ANSI-2010
   records (REF-00326/335/563/604); apply `db/migrations/0001-jurisdiction-hygiene.sql`.

## 7. Open loose ends

- **PR #14** open (corrections + this audit/handoff). CI: only the non-blocking `adherence_log_audit`
  (attestation shakedown) fails — a baseline 35-commit-stale re-attestation on `decisions_*`/`sessions_*`,
  **not caused by our content**; #13 merged through the identical failure. A **~1h self check-in is
  scheduled** (send_later) to re-check #14.
- **37 OPEN gaps** in `gaps`.
- **task #4** (validate gates / seeded plants) still pending — the gate before scaling.
- The **Global-South zero-result** question (search reachability vs genuine absence) is unresolved.

## 8. Hard-won lessons / gotchas (do not relearn these)

1. **Inventory the schema before declaring a gap.** The pilot's first draft called values "un-migrated" and
   `population_code` "null" because it queried the wrong column / wrong table. The DB is richer than any one
   table suggests. *Always check the substrate tables (section 5) before claiming something is missing.*
2. **The writer never certifies its own grounding.** Run a **separate** guilty-until-proven verifier agent
   (general-purpose, with DB + web access) on every load-bearing claim; it caught three real errors this
   session. Seed it the caveats you suspect (e.g., occupied-vs-unoccupied RT).
3. **Background workflows die silently on session suspension.** Use foreground small batches + checkpoints;
   resume via `resumeFromRunId`. Prefer synchronous `Agent` calls for verification.
4. **Branch discipline:** the working branch is `claude/project-status-next-steps-wgatjq`. When its PR merges,
   **restart from latest `main`** (don't stack on merged history); a rebase/force-with-lease is fine when it
   holds only merged history. Done twice this session (after #12, after #13).
5. **`python3` + sqlite3 module only** (no CLI). **Migration-based writes only.** Nothing promoted to
   `stated` without verifier confirmation.
6. **Don't overclaim numbers.** State attrition/ratios as directional when the underlying counts double-count
   (e.g., `search_languages.results_count` across slugs). The transparency ethos forbids the confident-but-wrong.

## 9. Critical files

- Plan: `/root/.claude/plans/delegated-pondering-pine.md`
- This session's deliverable: `working/evidence-migration/` (README, pipeline-audit.md, registry-reconciliation.md,
  pilot-A18-rt60/, db/migrations/, this HANDOFF)
- Doctrine: `references/project-standards.md` (7-tier L17; best-practice≠code L20; ●/◐/○ L26; Co-1 L35; three
  modes + DAR L14; top-down/bottom-up L11/L23; 14-lang/24-juris L121/L127; Kawa L405; solo-authorship L484;
  meta-methodological carve-out L520; A10 nine vectors L539)
- Governance: `governance/tier-system.md`, `governance/adversarial-use-framework.md` +
  `data/adversarial_use/catalog.yaml`, `governance/migration-based-writes-adopted-2026-05-11.md`
- Render (non-canonical, shape only): `site/specs/e-08.html` (the 4-door / 12-facet exemplar)
