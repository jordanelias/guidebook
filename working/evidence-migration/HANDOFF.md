# HANDOFF — evidence migration & rehabilitation program

*Written 2026-07-18 for a fresh context. Self-contained: a cold session should be able to resume from this
document + the two it points to (`pipeline-audit.md`, `/root/.claude/plans/delegated-pondering-pine.md`).*

*Updated 2026-07-19, seven batches across four sessions (batches 1-3 in the original session; batches 4-5
in a follow-on merged as PR #19; batch 6 in a further follow-on merged as PR #20; batch 7 in a further
follow-on after #20 merged) — see §0 below for what changed. Sections 1-9 are the 2026-07-18 state as
originally written; treat §0 as the current addendum.*

---

## 0. 2026-07-19 addendum — non-English research recovery (batches 1-7)

Picked up `research-handoff-non-english.md` and ran its recovery pipeline across seven batches; batch 5
was a dedicated **adversarial review** of the first four, batch 6 and batch 7 further follow-ons after
each prior PR merged. Full detail: `equity-dashboard.md`, `non-english-coverage-matrix.json`,
`global-south-finding.md`, `slug-language-tracking-matrix.md` (a live slug×language tracking table —
check this first before spending more research effort on any given slug/language). Seven migrations
applied (`data_20260719034512` through `data_20260719190934`, suffixed `...recovery.sql` /
`...recovery-batch{2..7}.sql`) — `data_migrations` now 206 rows; `PRAGMA foreign_key_check`/
`integrity_check` clean after all seven.

- **Batch 7**: closed out the 2 Indonesian leads batch 6 left untouched, plus 2 small unrelated loose
  ends. `WebFetch` failed its control-URL test a **4th consecutive session** — same WebSearch-only
  standard applied again. Permen PUPR 14/2017 ingested (REF-00770, tier 6/`code`, "Berlaku"/in force) —
  Indonesia's first jurisdiction in this corpus. Kepmen PU 468/1998 confirmed genuinely
  accessibility-scoped but formally revoked by Permen PU 30/PRT/M/2006 — correctly excluded. **All 9
  original Global-South leads are now resolved** (5 ingested, 4 correctly excluded). Separately: the
  Italian companion "Linee guida n. 1" date on REF-00746 corrected to 31 marzo 1994 (Legge 724/1994 art. 3
  cross-ref now confirmed); Portugal's IGAS 2023 ERPI referencial checked and found to contain no
  dementia-specific design content, corroborating (not overturning) the existing genuine-absence finding.
- **Batch 6**: `WebFetch` failed its control-URL test a 3rd consecutive session — rather than keep
  waiting, applied batch 5's validated `WebSearch`-corroboration standard to the 9 flagged Global-South
  leads. **Resolved 7 of 9**: 4 new jurisdictions ingested (Saudi Arabia's SBC 201, Egypt's Code 601,
  UAE/Dubai's Universal Design Code, Bangladesh's 2013 Disability Rights Act with an honest weak-
  enforcement caveat), 3 correctly excluded after closer inspection (Indonesia's SNI 03-1735-2000 turned
  out to be a fire-safety standard, not accessibility — a real scope-matching catch; BUAG confirmed a
  secondary explainer, not a primary source; a Hindi PDF lead couldn't be re-located and its relationship
  to an already-ingested source is unresolved, so it stayed un-ingested rather than risk a double-count).
  2 leads (Indonesian Kepmen/Permen) were left open batch 6, resolved batch 7 above.

**Batches 3-5, briefly (batches 1-2 detailed below unchanged):**
- **Batch 3**: fixed 2 more `lang_detected` mislabels missed by batch 1's narrower filter — including
  `REF-00572`, the *exact* example the original handoff cited as its motivating case. Added 1 new source
  (Chile's Ley 21.545 for sensory-room-user-control, honestly scoped — it's a general procedural duty, not
  an explicit sensory-room mandate as a naive read might suggest); investigated and rejected a Brazilian
  bill (PL 3098/24) as not-yet-enacted law.
- **Batch 4**: closed `luminance-contrast-and-pattern` (discovered to have rich search notes but **zero**
  `source_slug_links` at all — 0/0 → 13/13, 100% non-English) and discovered 4 "Tier-2" slugs
  (`mental-health-built-environment`, `deaf-spatial-design`, `cognitive-wayfinding-design`,
  `accessible-circulation-geometry`) have PRE-REMEDIATION-stub search notes with **zero named
  instruments** — a fundamentally different, harder problem than notes-extraction recovery. Did genuine
  fresh primary research for 2 of the 4 (2 jurisdictions each), including one **Co-1** addition (a
  Deaf-led Japanese research lab) as a deliberate counterweight to this corpus's documented Co-1
  thinness/US-UK skew.
- **Batch 5 — adversarial review, run at the user's explicit request.** 4 independent agents, blind to the
  ingesting agent's reasoning and instructed to try to REFUTE rather than confirm, checked DB integrity,
  re-verified a sample of 8 new sources via fresh WebSearch, and re-derived every documentation number
  from the live DB. **Found and fixed**: 1 factual error (Japan's MHLW ordinance unit-count cap was wrong),
  6 tier/`evidence_type` doctrine violations against `governance/tier-system.md` (including one that
  silently defeated the batch's own Co-1 goal), 1 `lang_detected` over-correction (reverted), 1 misleading
  audit-trail note (data value unchanged), and 2 documentation undercounts. **Structural integrity was
  clean throughout**, and 7 of 8 sampled sources were confirmed accurate — the review earned its keep by
  finding real, fixable problems without discrediting the underlying work. This is the same discipline
  §8 lesson 2 below describes, now applied reflexively to this session's own output.

**What happened, in priority order of what it changes about §2/§5 below:**

1. **A systematic `lang_detected` mislabel bug, much bigger than the one example the prior handoff cited**
   (batch 1). 59 rows corrected — national standards tagged `en` (English-gloss-derived) or
   cross-contaminated between non-English languages (Chinese hanzi misread as Japanese by `unicode_block`
   detection; short-string `langdetect` noise). 5 borderline cases deliberately left uncorrected (see
   coverage-matrix). Most of the resulting non-English-count jump is *visibility*, not new gathering — the
   sources were already there, mistagged.
2. **Tier-0 registry backlog (6 refs) mostly resolved as stale-duplicate, not a real hole** (batch 1). Only
   2 of 6 were genuinely missing (REF-00221 JP deafblind, REF-00139 SG wayfinding code — both ingested).
   The other 4 are registry entries for standards already migrated under different `ref_id`s — confirmed by
   title/standard-number match, not guessed.
3. **The Tier-1 ingestion-funnel bias is now directly demonstrated at the slug level, not just
   corpus-wide, and mostly fixed for the 3 richest slugs.** Checked `source_slug_links` for
   deaf-classroom-reverberation-time, stair-ramp-threshold-biomechanics-accessibility, and
   wayfinding-dementia-spatial-design: all three had **0/27 non-English links** despite the search having
   named 11-14 languages of instruments per slug. Current state: deaf-classroom-reverberation-time 9/12
   non-EN (batch 1, untouched in batch 2), stair-ramp-threshold-biomechanics-accessibility 11/26 non-EN
   (batch 1 + batch 2's NL ingest + ES citation correction), **wayfinding-dementia-spatial-design 13/22
   non-EN (batch 1's partial pass completed in batch 2 — the highest non-English share of any slug
   touched)**. Portugal was independently re-checked in batch 2 (5 more search queries) and its genuine
   absence held.
4. **Anti-fabrication gate held under pressure, twice.** Batch 1: NF S31-080:2006 (France) was verified to
   NOT actually cover classrooms (real scope is offices/tertiary) and was substituted with the correct
   citation (arrêté du 25 avril 2003). Batch 2: the CTE DB SUA (Spain) ramp-gradient table named in search
   notes turned out to conflate two different documents (a new-construction table and a separate
   existing-building tolerance table) — the existing DB row was relinked with the *corrected* figures and
   section citation rather than the wrong one.
5. **The Global-South zero-result question is answered per-language with evidence, and the "why can't we
   verify the recoveries" question is now precisely diagnosed rather than just repeated.** 4 of 5 languages
   (Indonesian, Hindi, Bengali, Arabic) are query-construction failures; only Swahili is genuine absence.
   Batch 2 made a **second, independent** attempt to directly read (not just WebSearch-corroborate) the 9
   flagged candidate sources — again 0/9 succeeded, but this time control-URL tests (`example.com`,
   `en.wikipedia.org`) confirmed the cause is a **session-wide `WebFetch` tooling outage**, not target-site
   blocking. None of the 9 are ingested. **Do not attempt a third WebSearch-only pass** — see
   `global-south-finding.md`'s batch 2 update.
6. **Applied jurisdiction-hygiene item 1** (batch 1; the previously-proposed, unapplied
   `0001-jurisdiction-hygiene.sql`): INTL → INT normalized (5 rows). Item 3 (19 null jurisdictions)
   intentionally still untouched.

**Honest limit (S3, restated):** two batches cover Tier-0 + the 3 richest Tier-1 slugs (2 fully, 1 now
complete after batch 2). Tier-2 (luminance-contrast-and-pattern 74 hits, sensory-room-user-control 42, and
4 more ~20-hit slugs) is untouched; the 9 Global-South recoveries need a session with functional `WebFetch`
before they can be ingested; two loose ends from batch 2 (the Italian "Linee guida" companion document's
exact date, and Portugal's unread IGAS 2023 ERPI reference) are flagged, not chased. Next steps are
enumerated in `equity-dashboard.md` §"Next batch."

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
| **ingestion (bias funnel)** | **narrowing** | 14 langs returned hits + 5 new Global-South jurisdictions (SA/EG/AE/BD/ID); corpus now **514 EN : 161 non-EN** (2026-07-19, 7 batches: +74 non-EN net, partly a lang_detected hygiene fix, partly new real-retrieval ingests — see §0) |
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
5. **Fix flagged data errors.** ✅ **DONE** (migration `data_20260718071505_…evidence-migration-issue-resolution.sql`):
   the Devos/REF-00571 mislink is re-pointed to REF-00735; the ANSI-2010 dups (REF-00326/335/604) are
   consolidated onto canonical REF-00563 (FKs re-pointed, dups marked `DUPLICATE-OF`, reversible — not
   deleted). Remaining: apply the proposed `db/migrations/0001-jurisdiction-hygiene.sql` (still un-applied).

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
