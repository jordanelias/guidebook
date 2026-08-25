# F5 — Design: splitting `MOB` into `AMB` (ambulatory) and `WHEEL` (wheelchair users)

**Read-only remediation design. Nothing here has been executed.**
Author: F5 (Fable 5, read-only), session_2026-08-25-pipeline-smoke-test-mobility.
Date: 2026-08-25. DB measured at `PRAGMA user_version` = 64, populations = 23 rows.

**Owner ruling being designed for (2026-08-25, DG-NON, settled):**
> "As to 'mobility', separate out into 'ambulatory' and 'wheelchair user' to start."

"To start" is read as: first cut, further splits may follow (part-time wheelchair users,
balance). Everything below is designed so a further split is an additive row plus the same
fan-out pattern — nothing keys on there being exactly two members.

**Pipeline placement.** `populations` and its crossing maps are SUBSTRATE, not a stage
(CLAUDE.md, THE PIPELINE). Measured today, **no stage table holds a MOB row** — research,
evidence-collection, judgment, synthesis and render tables are all at 0 MOB (see §2). The
split is a substrate act plus the repointing of two substrate crossing maps and one legacy
scaffold (`item_population_links`). That is why it is executable now, before the mobility
batch, at low cost — and why it should land BEFORE that batch frames a single search.

---

## 1. THE CODES

### 1.1 Proposed rows

| column | AMB | WHEEL |
|---|---|---|
| `population_code` | `AMB` | `WHEEL` |
| `display_name` | `ambulatory disabled people` | `wheelchair users` |
| `category` | `mobility` | `mobility` |
| `description` | Walking-based mobility disability: gait, stamina, stairs, distance, gradients; includes walking-aid users (canes, crutches, walkers, prosthetics). Split from MOB with WHEEL per owner ruling 2026-08-25. UK/AU standards term: "ambulant disabled people". | People who use wheelchairs (manual or power), full- or part-time; turning, clearance and transfer geometry, seated reach. The person, not the device (see terms TERM-016 vs TERM-079). Split from MOB with AMB per owner ruling 2026-08-25. |
| `parent_code` | `NULL` | `NULL` |
| `is_compound` | `0` | `0` |
| `status` | `active` | `active` |

### 1.2 Naming justification, against the live 23 rows

- **Owner's own words.** "Ambulatory" and "wheelchair user" are the owner's wording; the
  ruling is a naming act and the names are kept. "Wheelchair users" is also already this
  repo's person-term: `terms` row TERM-016 scope note reads *"TERM-016 is the person
  (wheelchair user); this is the equipment"* — and MOB's own `display_name` already said
  "wheelchair users". Community-preferred, identity-affirming, consistent with the
  post-2026-07-23 convention (BLIND "identity-first", BAR "fat people", LPA "little people").
- **Code style.** The DR-2026-07-23 set favours short readable words over acronyms
  (BLIND, BRAIN, MOVE, TALL, DEAFBLIND). `AMB` matches the historic sub-code `MOB/AMB` and
  the demand code `AX-AMB`'s note "Alias source: MOB ambulant share (canonical MOB/AMB)".
  `WHEEL` is legible at a glance. Rejected: `WC` (collides with water-closet in this
  domain — G-04), `WCU` (opaque acronym), `WHM` (names the mechanism `AX-WHM`, not the
  community — populations are communities, demand codes are mechanisms; keep the layers
  apart per the icf_demands RULE, references/project-standards.md:1097-1136).
- **Flat, no parent.** DR-2026-07-23: "no parent codes, no containment". `parent_code`
  stays NULL for both; MOB is not resurrected as a parent.
- **`category`** — `'mobility'` is in the `populations.category` CHECK
  (verified via `dbcore.check_values(conn,'populations','category')` =
  {cognitive, developmental, general, mental_health, mobility, neurological, pain_fatigue, sensory}).

### 1.3 What happens to `MOB`: **superseded and DELETED**, not retained

- **It cannot be retained as an umbrella code.** The permitted-umbrella test
  (references/project-standards.md:563-566, ratified 2026-07-23) requires (c) *"no opposed
  demand between members"*. The record already finds the opposite: *"`AX-AMB` (ambulant
  movement) and `AX-WHM` (wheeled movement) are not orthogonal — they are alternatives,
  simultaneous for part-time wheelchair users, and on ramp gradient their demands are
  **opposed**"* (references/project-standards.md:1120-1127, reaffirmed at :1151-1154).
  MOB fails clause (c); the design-equivalence exception cannot apply. Work-from-axes
  (project-standards.md:557-560) allows umbrellas only as *additive cross-cutting tags,
  never replacement codes* — and MOB has been the replacement code for two communities,
  which is precisely the erasure the rule's own provenance names ("'physically
  disabled/wheelchair users' erased the ambulatory ... disabled").
- **Not a deprecated tombstone row either.** `populations.status` does offer
  `'deprecated'` (check_values: {active, deprecated}), but `scripts/validate_population.py`
  P1 checks enum ↔ table parity **both ways with no status filter**
  (validate_population.py:141-148), so a kept row forces `MOB` to stay in
  `schemas/enums.py PopulationCode` indefinitely. The ratified execution precedent is
  DR-2026-07-23 ("Execution" section): **"INSERT new → repoint every code-bearing column →
  DELETE retired"** — VIS/UPL/DBL/NEU/OFS rows were deleted, not deprecated. Follow it.
- **Retirement memory** lives where the precedent put it: `RETIRED_CROSSWALK` in
  `scripts/validate_population.py:79` (add `"MOB"`), the DR/rule record, and this design.
  No co-occurrence tag is needed now: a person who both walks and wheels is `AMB+WHEEL`
  under the `+` intra-individual notation (project-standards.md:96-97). If the owner later
  names a distinct community code (e.g. part-time/ambulatory wheelchair users), it is added
  flat — the "to start" extension path.

---

## 2. THE DATA RESOLUTION — measured counts and per-row disposition

Every population-bearing column was enumerated from the live schema and counted
(read-only, 2026-08-25). Word-boundary `\bMOB\b` was also scanned across **every text
column of every table**.

| table.column | total rows | MOB rows | disposition |
|---|---|---|---|
| `populations.population_code` | 23 | 1 | DELETE (last), after all repoints — §1.3 |
| `item_population_links.population_code` | 372 | **31** | **fan out to both**, then delete MOB rows — §2.1 |
| `population_axis_map.population_code` | 53 | **2** | **1:1 replace** (AMB→AX-AMB, WHEEL→AX-WHM) — §2.2 |
| `evidence_population_match.target_population` / `.study_population` | 25 | **0** | nothing to resolve — §2.3 rule recorded for the future |
| `item_population_elaborations.population_code` | 0 | 0 | nothing; future writes use AMB/WHEEL |
| `probe_population_links.population_code` | 0 | 0 | nothing |
| `extraction_population_links.population_code` | 0 | 0 | nothing |
| `citation_population_links.population_code` | 0 | 0 | nothing |
| `case_study_populations.population_code` | 0 | 0 | nothing |
| `economics_entry_populations.population_code` | 0 | 0 | nothing |
| `specifications.population_code` | 0 | 0 | nothing (0-row object = unproven, not clean — verified by query, §6) |
| `spec_value_probes.population` | 0 | 0 | nothing |
| `source_value_extractions.population_code/.population_label` | 0 | 0 | nothing |
| `bpc_metadata.population` | 0 | 0 | nothing (registry note claiming 42 MULTI rows is stale; table is empty today) |
| `reasoning_doc_citations.population` | 0 | 0 | nothing |
| `term_item_links.population` | 147 | 0 (all NULL) | nothing |

Other `\bMOB\b` text hits (not population-code columns):

| where | rows | disposition |
|---|---|---|
| `term_aliases.alias` = 'MOB' (TERM-079 "mobility aid", alias_type DOMAIN) | 1 | **keep** — maps the legacy token for slug-token resolution; historical shorthand is its stated job |
| `axes.notes` ("Alias source: MOB …") on AX-AMB, AX-WHM, AX-REA | 3 | append a supersession note to AX-AMB/AX-WHM in the migration (AX-BAL's `\|\|` append pattern); AX-REA's "canonical MOB/UPL" is pre-2026-07-23 history, leave |
| `population_axis_map.note` rowid 1 | 1 | replaced with its row (§2.2) |
| `decisions.summary/.rationale` rowid 124 | 1 | frozen decision history — never edited |
| `source_locators.title/.jurisdiction` rowids 226, 306 | 3 | clue store — **exempt permanently** (owner ruling 2026-08-24, "the clue store exists to be copied out of") |

### 2.1 `item_population_links` — 31 MOB rows → fan out to both members (62 rows)

Measured: 31 rows = **28 with `subtype=''` + 3 with `subtype='with-upper-limb-involvement'`**
(E-12, G-08, G-09), across 28 distinct items
(A-10b, B-12, C-04, D-03, D-11, E-01–E-08, E-12, F-05, F-06, F-08, G-03–G-09, H-01, H-04,
I-01, I-04). All 31: `applicability='applies'`, `rationale_ref=NULL`, created 2026-05-11 by
`session_2026-05-11-items-population-normalization` (pre-taxonomy scaffold from the retired
`applicable_groups` CSV).

**Rule: every MOB row becomes one AMB row AND one WHEEL row, `subtype`/`applicability`/
`rationale_ref` carried verbatim; the MOB rows are then deleted.**
Count produced: 372 − 31 + 62 = **403** rows; 62 new.

Why fan-out is justified *for this table*:
- MOB's own description is the union ("walking, balance, or wheeled mobility"), so
  assigning each row to only one member is a per-item judgment nobody has made; making it
  silently would erase one community from each item — the exact failure work-from-axes
  records ("erased the ambulatory ... disabled"). The umbrella-split analogue of the
  ratified test's clause (b): **preserve the union, never dedupe it away**.
- What the fan-out ASSERTS: member-level `applies` at the same grade the umbrella row
  carried. This is a mechanical carry, not a synthesis finding. Per the owner ruling of
  2026-08-24 (§2.4, project-standards.md:935-968) applicability is an **output of
  synthesis**; these edges are scaffold either way, and the taxonomy-execution session
  already recorded the intent: *"31 item links re-derived per mechanism at harvest"*
  (baseline 057:5070, the retired `population_reclass` row). The migration header must say
  the fan-out is mechanical and pending re-derivation.
- What is LOST: nothing — no row is dropped, and the deleted MOB rows survive in baseline
  057 and git history.
- **Flagged for review, not guessed:** the 3 `with-upper-limb-involvement` subtype rows
  (→ 6 after fan-out). Upper-limb involvement is the AX-REA / LMB axis; under the flat
  taxonomy that subtype may be better expressed as `+LMB` co-occurrence. Leave the subtype
  verbatim in this migration; queue the question for synthesis (it is a judgment, and per
  §2.4 not owed now).

*Alternative considered and NOT recommended (flagged in §8):* delete the 31 rows with no
replacement, on the strict §2.4 reading that zero pre-synthesis links is the correct state.
Rejected here because DR-2026-07-23's conservation principle ("No synthesis work
discarded") governed the last re-key, the links feed live render surfaces (§4), and
deleting content rows is a bigger content decision than this ruling made.

### 2.2 `population_axis_map` — 2 MOB rows → 1:1 replacement, NOT a fan-out

Measured: exactly 2 rows, both `role='ALIAS'`:
`(MOB, AX-AMB, 'ambulant share (MOB/AMB)')` and `(MOB, AX-WHM, 'wheeled share')`.
**The split is already encoded here** — MOB was an alias over two demand mechanisms.

**Rule:** `(AMB, AX-AMB, ALIAS)` + `(WHEEL, AX-WHM, ALIAS)` inserted; the two MOB rows
deleted. Count: 53 − 2 + 2 = **53**. Nothing lost, nothing asserted beyond a rename of the
alias halves: each new population is the community face of exactly the mechanism its half
of MOB already aliased. `ALIAS` matches the live convention (BLIND→AX-VIS-*, LMB→AX-REA,
PAIN→AX-PAI, DEAF→AX-AUD all ALIAS). Candidate SECONDARY rows (e.g. WHEEL→AX-REA seated
reach, AMB→AX-BAL) are **not** written — per §2.4 they are outputs of evidence, and the
MOB rows never asserted them (§8).

### 2.3 `evidence_population_match` — 25 rows, ZERO MOB. Nothing to resolve.

Measured: `target_population` distribution AUT 7, COM 3, DEM 7, NDV 8; no `\bMOB\b` in
`target_population` OR `study_population` (both scanned; `study_population` is free prose
by design — validate_population.py deliberately excludes it). Count produced by the split:
**0 changed rows; no grade invalidated.**

**Rule recorded for the future:** a match grade is a judgment-stage fact about one
(source, target population) pair. Had a MOB grade existed it would be resolved by
**re-grading per member against the study population** — the study's population-of-study is
a fact about the study and a PARTIAL against the union is not automatically PARTIAL against
each member. Fan-out is never permitted in this table. Note: `target_population` has **no
FK and no CHECK** (`check_values` = NONE), so nothing but the `db.py add-population-match`
writer stops a retired code being written here post-split — that writer validates against
`populations`, which is one more reason MOB must not remain as an active row.

---

## 3. THE MIGRATION

### 3.1 Shape: one DATA migration; no schema migration; no `user_version` bump

- No DDL is needed: new `populations` rows, junction repoints and deletes are all data.
  So: **no `scripts/migrations/0NN_*.sql`, no `PRAGMA user_version` change, no Pydantic
  schema-shape change** (the enum VALUE list changes — §4 — but no model shape).
- Authored as SQL and emitted via
  `python3 scripts/emit_data_migration.py --session <executing-session>.md --summary "split MOB into AMB + WHEEL (owner ruling 2026-08-25)" --input split.sql`
  → `scripts/migrations/data_{YYYYMMDDHHMMSS}_{session-slug}.sql`, applied by
  `python3 scripts/migrate_db.py`. The emitter wraps BEGIN…COMMIT and will WARN (not
  refuse) on the UPDATE/DELETE statements — expected, review and proceed.
- This is exactly DR-2026-07-23's shape: the last population re-key was "authored as a
  **data** migration so it runs in the data phase (after all data loads) and stays
  rebuild-reproducible".
- `db.py` has **no subcommand** for `populations`, `item_population_links` or
  `population_axis_map` (verified against the full `add_parser` list). Per CLAUDE.md §4
  that is a CLI coverage gap in general; for a one-shot owner-ruled taxonomy act the
  sanctioned path is the data migration itself (precedent: DR-2026-07-23 and
  `data_20260825215123_2026-08-25-rulings-incorporation-and-pipeline-sweep.sql`).
  Rehearse on a scratch copy first (`cp data/guidebook.db $SCRATCH`;
  `GUIDEBOOK_DB_PATH` inline on every call); canonical DB sha must not move until
  `migrate_db.py` applies the committed migration.

### 3.2 Append-only replay constraints — checked

- `grep -n "'MOB'" scripts/migrations/*.sql` → **only** `057_baseline_2026-08-12.sql`
  (populations :2369; the 31 item links :1933-2258; term_aliases :4418; the dropped
  `population_reclass` :5070; population_axis_map :5502-5503) and one incidental prose
  comment in `data_20260823223839`. Consequence: our DELETEs replay **after** the baseline
  INSERTs they compensate — reproducible. The trap (a DROP/DELETE replaying before its
  target's INSERT) does not arise. The baseline itself is immutable; do not touch it.
- **No `datetime('now')` anywhere in the migration** — `migrate_db.py --rebuild` is
  byte-parity-compared (the `migration_reproducibility` gate); every timestamp and
  session literal must be a fixed string.
- FK behaviour: 11 columns FK to `populations(population_code)`, **all `ON DELETE NO
  ACTION`** — nothing cascades; a naive delete cannot destroy evidence rows. (The only
  CASCADE in the vicinity is `item_population_links.item_code → items`.) `PRAGMA
  foreign_keys` defaults OFF (measured 0) and `migrate_db.py` explicitly applies bodies
  with FK OFF then restores ON (migrate_db.py:150-162,202) — so ordering is for
  legibility and for integrity gates, not for the engine.
- `population_code` is under **no CHECK constraint anywhere**
  (`dbcore.check_values` on `populations`, `item_population_links`,
  `population_axis_map`, `specifications`, `evidence_population_match` → all NONE).
  The vocabularies that DO constrain us and are satisfied: `category` (§1.2), `status`,
  `applicability` (carried verbatim from valid rows), `role` ('ALIAS' valid).

### 3.3 The SQL (body for `emit_data_migration.py --input`)

```sql
-- Split MOB -> AMB + WHEEL. Owner ruling 2026-08-25 (DG-NON, settled):
--   "As to 'mobility', separate out into 'ambulatory' and 'wheelchair user' to start."
-- MOB fails the permitted-umbrella test clause (c) -- AX-AMB and AX-WHM demands are
-- opposed on ramp gradient (project-standards.md:1120-1127) -- so it is retired, not
-- kept as an umbrella. Execution shape per DR-2026-07-23: INSERT new -> repoint ->
-- DELETE retired. Fan-out of item links is MECHANICAL CARRY of the umbrella's union,
-- pending synthesis re-derivation (owner ruling 2026-08-24 §2.4: applicability is an
-- output of synthesis). All timestamps are literals: this file must replay byte-identically.

-- 1. The two member populations.
INSERT INTO populations (population_code, display_name, category, description,
                         parent_code, is_compound, status, created_at, updated_at)
VALUES
  ('AMB', 'ambulatory disabled people', 'mobility',
   'Walking-based mobility disability: gait, stamina, stairs, distance, gradients; includes walking-aid users (canes, crutches, walkers, prosthetics). Split from MOB with WHEEL, owner ruling 2026-08-25. UK/AU standards term: "ambulant disabled people".',
   NULL, 0, 'active', '2026-08-25T00:00:00Z', '2026-08-25T00:00:00Z'),
  ('WHEEL', 'wheelchair users', 'mobility',
   'People who use wheelchairs (manual or power), full- or part-time; turning, clearance and transfer geometry, seated reach. The person, not the device (TERM-016 vs TERM-079). Split from MOB with AMB, owner ruling 2026-08-25.',
   NULL, 0, 'active', '2026-08-25T00:00:00Z', '2026-08-25T00:00:00Z');

-- 2. Fan the 31 MOB item links out to both members, verbatim (subtype, applicability,
--    rationale_ref carried; ORDER BY rowid pins insertion order for byte-parity).
INSERT INTO item_population_links (item_code, population_code, subtype, applicability,
                                   rationale_ref, created_at, created_by_session)
SELECT item_code, 'AMB', subtype, applicability, rationale_ref,
       '2026-08-25T00:00:00Z', 'REPLACE-WITH-EXECUTING-SESSION-STEM'
  FROM item_population_links WHERE population_code = 'MOB' ORDER BY rowid;

INSERT INTO item_population_links (item_code, population_code, subtype, applicability,
                                   rationale_ref, created_at, created_by_session)
SELECT item_code, 'WHEEL', subtype, applicability, rationale_ref,
       '2026-08-25T00:00:00Z', 'REPLACE-WITH-EXECUTING-SESSION-STEM'
  FROM item_population_links WHERE population_code = 'MOB' ORDER BY rowid;

DELETE FROM item_population_links WHERE population_code = 'MOB';

-- 3. Demand map: 1:1 replacement of the two ALIAS halves (not a fan-out).
INSERT INTO population_axis_map (population_code, axis_code, role, note,
                                 created_at, created_by_session)
VALUES
  ('AMB',   'AX-AMB', 'ALIAS', 'population face of AX-AMB Ambulant movement; was MOB ambulant share',
   '2026-08-25T00:00:00Z', 'REPLACE-WITH-EXECUTING-SESSION-STEM'),
  ('WHEEL', 'AX-WHM', 'ALIAS', 'population face of AX-WHM Wheeled movement & transfer; was MOB wheeled share',
   '2026-08-25T00:00:00Z', 'REPLACE-WITH-EXECUTING-SESSION-STEM');

DELETE FROM population_axis_map WHERE population_code = 'MOB';

-- 4. Provenance append on the two demand rows (AX-BAL's '||' append pattern).
UPDATE axes SET notes = notes || ' || SPLIT 2026-08-25: population face is now AMB (was MOB ambulant share).'
 WHERE axis_code = 'AX-AMB';
UPDATE axes SET notes = notes || ' || SPLIT 2026-08-25: population face is now WHEEL (was MOB wheeled share).'
 WHERE axis_code = 'AX-WHM';

-- 5. Retire the umbrella LAST, once nothing references it.
DELETE FROM populations WHERE population_code = 'MOB';
```

Post-conditions: populations 23→24; item_population_links 372→403 (62 new, 31 deleted);
population_axis_map 53→53; zero MOB in any population-code column.

---

## 4. THE CALLER SWEEP (CLAUDE.md §0.4 — a view is a caller, and so is a skill)

Sweep method: word-boundary `\bMOB\b` via `grep -r` (NOT ripgrep — `.ignore` hides
`sessions/`, `_archived/`, `references/search-log/`, `workplan/_superseded/`), all file
types, plus a `sqlite_master` walk and a per-text-column DB scan (§2).

**MUST change in the same commit as the migration:**

| caller | what |
|---|---|
| `schemas/enums.py:35` (`MOB = "MOB"` in `PopulationCode`) | replace with `AMB = "AMB"` and `WHEEL = "WHEEL"` in the "Moving and handling" block; else `validate_population` P1 goes red both directions |
| `scripts/validate_population.py:79` (`RETIRED_CROSSWALK`) | add `"MOB": "AMB (ambulatory) / WHEEL (wheelchair users) — split per owner ruling 2026-08-25; assign per member"` so any straggler gets a P3 message naming the fix |
| `site/populations/mob.html` | generated page named for the code — `git rm`; generate `amb.html` + `wheel.html` via `python3 scripts/generate/population_page.py AMB` / `WHEEL` (build_site.py drives `site/specs/` only; population pages are per-code) |
| `tools/spec-curation-vetting-surface.html` (31 `MOB` tokens) and `tools/pipeline-completeness-dashboard.html` (1) | regenerate via `bash scripts/regenerate_derived.sh` — their `--check` gates mirror CI (`pipeline_completeness_fresh` is BLOCKING) |

**Checks that fire, and when (registry levels verified in `governance/check-registry.yaml`):**

| check | level | behaviour across the split |
|---|---|---|
| `test_db_integrity` | **blocking** | A03 (`item_population_links → populations`) fails on any orphan; passes iff repoint precedes the populations DELETE. A05 unaffected (no MOB matches). |
| `validate_axes` | **blocking** | walks all 53 `population_axis_map` rows; fails on a dangling `MOB` population_code; passes with the §2.2 replacement. EXAMINED stays 232. |
| `pipeline_completeness_fresh` | **blocking** | goes red if dashboards are not regenerated in the same commit. |
| `validate_population` | advisory | P1 parity (needs enums.py same commit), P2/P3 catch stragglers. |
| `validate_items` | advisory | V5 junction FK re-check; fine after repoint. |
| `population_integrity_audit` | advisory | its three junctions are 0 rows; unaffected. |
| `check_rendered_docs` | blocking | EXAMINED: 0 under `--all` (specs/ is reference-only since 2026-08-06); unaffected. |
| `retired_vocabulary` | advisory | see §8 — a `MOB` entry likely fails admission test 4 (flood from frozen content); record in the file's `deferred:` with reasoning rather than adding. |

**DB views:** none of the 18 views names `MOB` literally. Five touch `population_code`
(`v_value_independence`, `v_source_reach_all`, `v_item_extractions`, `v_item_provenance`)
or carry `specifications.*` (`v_divergence`) — all read tables that are 0-row today, so
"no output change" is unproven-by-emptiness; §6 proves it by query instead. **No view is
deleted or altered**; the four protected cross-stage pointers are untouched.

**Cosmetic, same commit or immediately after (comments/docstrings, not behaviour):**
`schemas/population.py:32-33` (example strings "MOB", "MOB/AMB"),
`scripts/generate/population_page.py:25` (usage example `MOB`).

**Live doctrine surfaces owed an update (prose, not code):**
- `references/project-standards.md` — append the RULE block recording this ruling
  (append-only ledger; the split is otherwise a ruling with no operative surface — the
  exact defect the 2026-08-25 RULES entry documents).
- `governance/population-taxonomy.md` supersession banner (:15) — its "canonical 23 codes"
  list includes `MOB`; the banner itself is now stale and must gain the split note.
- `governance/functional-taxonomy.md:123,283-284,298,370` — historic crosswalk tables
  naming MOB; annotate, don't rewrite (they describe the 2026-07-21 state truthfully).

**Skills carrying `\bMOB\b` — live callers, pre-existing debt:**
`skills/cross-population-conflict-mapper_SKILL.md` (8 hits),
`functional-deficit-auditor` (3), `table-formatter` (3), `voice-style` (2),
`sensory-coherence-checker`, `item-specification-writer`, `supersession-audit`,
`guidebook-auditor`, `connection-discovery`, `relational-integrity-checker` (1 each).
Verified: these also still carry `VIS`/`OFS`/`NEU`/`DBL` (e.g. conflict-mapper: 12 such
hits) — they were never swept after DR-2026-07-23, whose DR explicitly deferred the
derived-markdown sweep as non-gating. The MOB hits join that same follow-up bucket —
**but flag it louder now**: a mobility batch that loads these skills verbatim will be
handed retired codes at the exact moment MOB retires (§7).

**Explicitly NOT swept (frozen records / history, per precedent and `.ignore` policy):**
`scripts/migrations/057_baseline*.sql`, `sessions/**`, `decisions/**`,
`workplan/` history + `_superseded/` + `deprecated/`, `references/bpc/**`, `references/fdr/**`,
`references/conflict-matrices/**`, `references/toc.md`, `references/claim-reference-join.json`,
change-orders, `_archived/**`, DB rows: `decisions` rowid 124, `source_locators` 226/306
(clue store, exempt), `term_aliases` TERM-079. 228 markdown files carry `\bMOB\b` in total —
the overwhelming majority are these frozen classes.

---

## 5. THE ICF/DEMAND MAPPING (codes WITH names — the twice-broken rule)

The demand layer is physically still `axes`/`population_axis_map` — the `icf_demands`
rename is D-SCHEMA, owner-gated, and **must not be attempted piecemeal here**
(project-standards.md:1129-1135). These rows use the current physical names and survive
the rename mechanically.

**AMB → `AX-AMB` "Ambulant movement", role ALIAS** (weight: the population's face
mechanism, per the ALIAS convention). ICF anchors carried by the demand row:
- b770 **Gait pattern functions**; b730 **Muscle power functions**
- d450 **Walking**; d455 **Moving around**; d460 **Moving around in different locations**

**WHEEL → `AX-WHM` "Wheeled movement & transfer", role ALIAS.** ICF anchors:
- b730 **Muscle power functions**; b710 **Mobility of joint functions**
- d465 **Moving around using equipment**; d420 **Transferring oneself**;
  d410 **Changing basic body position**

The mapping is a **weighted vector, not a bucket**: nothing above says AMB has no wheeled
demand or WHEEL no ambulant demand — a part-time wheelchair user carries both
simultaneously (project-standards.md:1121-1123), expressed as `AMB+WHEEL` on the person and,
when evidence supports it, as additional SECONDARY rows on either code. Candidate
SECONDARY rows deliberately not asserted now (outputs of synthesis, §2.4): WHEEL→AX-REA
(Reach & manipulation — seated reach envelope is in AX-REA's own mechanism text),
AMB→AX-BAL (Balance & postural demand), AMB→AX-STA (Sustained-exertion demand — standing/
distance). Research framing note: the full cross-product rule means the mobility batch
frames against ALL populations/access-needs/ICF codes anyway; these mappings never gate
what gets searched.

---

## 6. VERIFICATION PLAN (commands, in order)

```bash
bash .claude/hooks/ensure-deps.sh          # pydantic first, or 5 governance gates lie

# 0. Rehearse on scratch (canonical sha must not move):
SCRATCH=/tmp/claude-0/.../scratchpad/split-rehearsal.db
cp data/guidebook.db "$SCRATCH"
GUIDEBOOK_DB_PATH="$SCRATCH" python3 - # apply split.sql body, then run the queries below

# 1. Emit + apply for real:
python3 scripts/emit_data_migration.py --session <session>.md \
  --summary "split MOB into AMB + WHEEL (owner ruling 2026-08-25)" --input split.sql
python3 scripts/migrate_db.py
python3 scripts/migrate_db.py --rebuild "$PWD/scratchpad/.../rebuilt.db"   # byte-parity vs committed

# 2. Conservation + orphan queries (all must hold):
python3 - <<'EOF'
import sqlite3
c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
q = lambda s: c.execute(s).fetchone()[0]
assert q("SELECT COUNT(*) FROM populations") == 24
assert q("SELECT COUNT(*) FROM populations WHERE population_code IN ('AMB','WHEEL')") == 2
assert q("SELECT COUNT(*) FROM populations WHERE population_code='MOB'") == 0
assert q("SELECT COUNT(*) FROM item_population_links") == 403
assert q("SELECT COUNT(*) FROM item_population_links WHERE population_code='AMB'") == 31
assert q("SELECT COUNT(*) FROM item_population_links WHERE population_code='WHEEL'") == 31
# pairwise parity: every AMB link has its WHEEL twin (item, subtype, applicability)
assert q("""SELECT COUNT(*) FROM item_population_links a WHERE a.population_code='AMB'
            AND NOT EXISTS (SELECT 1 FROM item_population_links w
              WHERE w.population_code='WHEEL' AND w.item_code=a.item_code
                AND w.subtype=a.subtype AND w.applicability=a.applicability)""") == 0
# no orphaned population reference anywhere:
for t,col in [("item_population_links","population_code"),("population_axis_map","population_code"),
              ("item_population_elaborations","population_code"),("specifications","population_code"),
              ("citation_population_links","population_code"),("probe_population_links","population_code"),
              ("extraction_population_links","population_code"),("case_study_populations","population_code"),
              ("economics_entry_populations","population_code"),("source_value_extractions","population_code")]:
    assert q(f"SELECT COUNT(*) FROM {t} WHERE {col} IS NOT NULL AND {col} NOT IN (SELECT population_code FROM populations)") == 0, t
assert q("SELECT COUNT(*) FROM population_axis_map") == 53
assert q("SELECT COUNT(*) FROM evidence_population_match") == 25    # untouched
print("ALL PASS")
EOF

# 3. Regenerate render surfaces, then gates:
python3 scripts/generate/population_page.py AMB
python3 scripts/generate/population_page.py WHEEL
git rm site/populations/mob.html
bash scripts/regenerate_derived.sh          # includes the tools' own --check gates

# 4. The check battery — BOTH invocations (the selftest is where a rename fails):
python3 scripts/run_checks.py --changed-from origin/main --explain
python3 scripts/run_checks.py --selftest
python3 scripts/validate_population.py --verbose   # P1 parity + P3 stragglers directly
python3 scripts/validate_axes.py
python3 scripts/tests/test_db_integrity.py         # A03 in particular
grep -rn --include='*.py' --include='*.yaml' -E '\bMOB\b' scripts schemas governance tools \
  | grep -v RETIRED_CROSSWALK    # expect: nothing
```

Also owed at execution: attestation if the commit touches `decisions/` or `sessions/`
(CLAUDE.md rule 2); commit format `{skill}: {action} [YYYY-MM-DD HH:MM]`; scratchpad
committed at the natural break, not session end.

---

## 7. WHAT THIS BREAKS — honest list

1. **No evidence grade is invalidated.** 0 of 25 `evidence_population_match` rows touch
   MOB (measured, incl. substring scan). Targets are AUT/COM/DEM/NDV only.
2. **`v_divergence` output: unchanged** — it joins `specifications` (0 rows) to
   `convergence_assessment` and names no population; returns 0 rows before and after.
   Same for the other four population-touching views (0-row sources); §6 verifies by
   query rather than trusting emptiness.
3. **Rendered surfaces DO hardcode MOB** and go stale the moment the migration lands:
   `site/populations/mob.html` (whole page), `tools/spec-curation-vetting-surface.html`
   (31 tokens), `tools/pipeline-completeness-dashboard.html` (1). Not regenerating in the
   same commit turns `pipeline_completeness_fresh` (blocking) red. `mob.html` must be
   deleted by hand — no generator removes a page for a code that no longer exists.
4. **`schemas/enums.py` and the migration must land together** or `validate_population`
   P1 fires in one direction or the other (advisory, but it is the split's own check).
5. **The 62 fan-out links assert member-level applicability mechanically.** They are
   scaffold pending synthesis re-derivation (§2.1) — anyone reading them as findings is
   over-reading, and the migration header says so. The 6 `with-upper-limb-involvement`
   rows are the weakest and are flagged.
6. **Live skills still teach the retired taxonomy** (§4): a mobility batch loading
   `cross-population-conflict-mapper` et al. gets MOB/VIS/OFS examples verbatim.
   Pre-existing DR-2026-07-23 debt, but this split raises its cost precisely when a
   mobility batch is imminent.
7. **Frozen prose disagrees with the DB forever** (228 md files carry `\bMOB\b`), as it
   already does for VIS/NEU/OFS. Mitigated by `RETIRED_CROSSWALK` + the project's
   established "history is not swept" posture; a `retired_vocabulary` entry is the
   tripwire option (§8).
8. **The slug `mobility-built-environment` (ACTIVE, `serves_axes` NULL) now spans two
   populations.** Slug names are frozen path identifiers (never renamed), but the
   "each slug covers exactly one population" RULE (2026-03-18) now bites: the pending
   mobility batch needs a framing decision (§8). Under work-from-axes the slug can
   legitimately serve the two demand codes (AX-AMB + AX-WHM) instead.
9. **`AMB`/`WHEEL` were verified unused** as population codes anywhere in the DB (0 rows)
   — no collision. `AMB` does collide as a *substring* inside `AX-AMB` in prose greps;
   sweep patterns must stay word-boundary.

---

## 8. NEEDS AN OWNER DECISION (everything else above is executable without one)

1. **Ratify the two codes and display names** (`AMB` "ambulatory disabled people",
   `WHEEL` "wheelchair users") — DG-NON naming act; this design proposes, the owner
   disposes. Alternatives rejected in §1.2 if the owner prefers different tokens.
2. **Fan-out vs delete for the 31 item links** (§2.1). Recommended: fan out (conservation
   precedent). The strict §2.4 alternative — delete all 31 as pre-synthesis presupposition
   — is defensible and cheaper, but discards recorded scaffold and empties two members'
   item lists on the render surface. One-word decision: "fan" or "drop".
3. **The 3 `with-upper-limb-involvement` subtype rows** (→6 after fan-out): keep subtype,
   or re-express as `+LMB` co-occurrence at synthesis time. Recommended: defer to synthesis
   (no decision needed now unless the owner wants the subtype gone in this migration).
4. **Candidate SECONDARY demand rows** (WHEEL→AX-REA, AMB→AX-BAL, AMB→AX-STA): assert now
   or wait for evidence per §2.4. Recommended: wait.
5. **Slug framing for the mobility batch** (§7.8): one slug serving AX-AMB+AX-WHM, or two
   population slugs. Touches the 2026-03-18 one-slug-one-population RULE.
6. **`retired_vocabulary` entry for `MOB`**: recommended to record under `deferred:` with
   reasoning (fails admission test 4 — word-boundary MOB floods frozen content and the
   live hits are already caught by validate_population P3). Adding it as live is the
   owner's call.
7. **Future member codes** ("to start"): part-time/ambulatory wheelchair users as their own
   community code, or `AMB+WHEEL` co-occurrence only. Nothing in this design forecloses
   either; flagged so the extension path is on the record.
