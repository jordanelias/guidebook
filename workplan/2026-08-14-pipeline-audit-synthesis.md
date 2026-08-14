# 2026-08-14 — Six-agent pipeline audit: throughlines, lessons, and the culling list

**What this is.** Four read-only analyses of the apparatus (pipeline walkability, code rigour,
read/write surface, provenance), four independent adversarial reviews of those analyses, and two
contradiction audits (governing layer, executable layer). Ten agent-passes, all read-only, all
against `main @ 6c690b2` with the corpus empty.

**Status of the inputs.** The four analyses are **superseded by their reviews**. Every review
re-derived the numbers rather than trusting them, and each broke at least one load-bearing claim.
Where this document states a fact, it states the *review's* verdict, not the analysis's. Reviews and
audits are in the session scratchpad; their substance is carried here.

**One correction to the premise this work was commissioned under.** The brief said there are no live
item codes. That is right about content and wrong about the frame: `specifications` is 0 rows, but
`items` holds 93 `active` rows, including `E-08 — Corridor Clear Width (≥1200 mm Minimum on All
Primary Routes)`. The 2026-08-12 retirement removed the E-08 *exemplar*, not the item. See §5.

---

## 1. What survived every attack

Exactly one finding across all four analyses survived adversarial review unqualified, and two
independent agents reached it by different routes:

> **A determination cannot reach the words that support it. There is no schema edge from
> `specifications` to the claim or extract that licenses its value.**

- Inbound FKs to `specifications`: exactly one (`specification_source_links.specification_id`).
  Inbound to `source_value_extractions`: exactly one (`extraction_population_links`), which does not
  touch specifications. No JSON column on either side names the other's key. **0 of 18 views cross
  the joint.**
- Production already improvises the join it lacks: `pilot_renderings.py:301-306` joins on
  `(ref_id, item_code)` — which returns 0 rows whenever `item_code` is NULL (a documented, intentional
  staging state) and never constrains population, so a populated join can attach another population's
  extraction.
- `governing_refs` points at *sources*. "Which words support this number" is currently
  **unrepresentable**, not merely unrendered.

Everything else in the provenance analysis — doctrine stamping, hash coverage, the vetting page — is
*unbuilt on existing substrate*. This one is a design gap. It is also precisely what the owner's
backend-vetting ruling requires, and it costs one DDL migration today against zero rows.

## 2. Throughlines

### 2.1 The characteristic defect is partial correction, not error

Three of the governance audit's three BLOCKING findings have the identical shape: **a decision was
ratified, one location was amended, and co-located rules kept asserting the repealed position.**

- **Option A** (weak-band anchoring, ratified 2026-07-21): the ledger amended one of three
  co-located rules. `project-standards.md:17` and `:26` still state the repealed absolute — and the
  executing DR asserts "Option A now holds across … its governing sources." Two live ledger rules now
  give opposite instructions on the same act, in a file bootstrap-loaded into every session.
- **Person Mode** (ratified 2026-07-13/14): "OT assessment resolves position **within range**"
  survives in locked ledger rules and in the *mandated handoff-flag template* — text the ratified
  doctrine defines as wrong. DR-2026-07-14 named these exact lines for a second pass that never ran.
- **Tier-3 threshold** (ratified 2026-07-12): the SHA-anchored doctrine file's own state-machine
  table still admits Tier-3-alone to `stated`. Every sibling doc was corrected; the anchor was not.

The same shape recurs outside governance: `CLAUDE.md` §4 describes the pre-baseline migration layout;
its §1 says `main` is "protected by CI" while §0 and §7 say it is not; `retired-vocabulary.yaml`
excuses one script's `/tmp` default by naming a workflow that never runs it. `CLAUDE.md` §0 opens by
narrating this failure mode about itself. The repo knows the shape; it has no mechanism for it.

**`CLAUDE.md` §0 rule 5 already demands a caller sweep for renaming any identifier, path, or column.
It does not demand one for ratifying a rule.** That asymmetry is the finding.

### 2.2 Four analyses, four false-absence claims — in the same direction

| Analysis | Claimed absent | Actually |
|---|---|---|
| A | "Nothing reconciles the dual stores" | Blocking `test_db_integrity` §H holds two of three pairs bidirectionally |
| B | "`main` is not branch-protected, so blocking is decorative" | `main` **is** protected (GitHub API) |
| C | "A live canonical writer with no invoker" | Uninvoked yes; its default target is `/tmp/guidebook.db`, not canonical |
| D | "R13 is write-time-or-never" | A retrospective whole-corpus check exists, with a blocking git-witnessed ratchet |

Each error came from stopping at the layer the agent was assigned — DDL-only, registry-only,
AST-only, hash-only. **Failure to search is indistinguishable from a finding.** This is the repo's own
§10 warning ("a gate reporting zero may have examined zero") reproduced in the auditors rather than
the audits. Two of the four were stale facts copied out of `CLAUDE.md` into present-tense
conclusions — guardrail §9-1 failing at exactly the place it was written for.

### 2.3 Every integrity instrument checks identity; none checks content

Four instruments, one shape:

- `derivation_sha` covers exactly four fields — `item_code`, `population_code`, sorted
  `governing_refs`, `rule_version`. **Reproduced on a scratch copy:** altering a determination's
  values by 50% *and* its unit mm→cm left `test_db_integrity` at **70/70** with K01 ✓ and
  `validate_evidence_state` PASS.
- `test_db_integrity` L01 compares **6 of 22** decision columns.
- L02 compares **record counts only** for jurisdictional values; `validate_schema --cross-check`
  compares the **identity triple** only.
- **Nothing anywhere reads `value_min` / `value_max` / `value_unit`** — not K01, not the state
  validator, not any view predicate, not the vetting surface. A `stated` determination with no value
  at all passes every gate.

Fair framing, per the reviews: K01 is documented as a *derivation* attestation, not a value-integrity
check; it does protect `governing_refs`, the most forgeable field; the advisory deep-reproducibility
check would catch an out-of-migration tamper; and the repo recorded essentially this result on
2026-08-01. It is a **coverage gap across four instruments**, not one broken instrument — which is
why it belongs here as a throughline rather than as four findings.

### 2.4 The parity checks with narrow envelopes are the ones with live divergence

Two divergences exist **right now**, and nothing detects either:

- **`jurisdictional_values.evidence_tier` — 109 of 109 rows disagree.** The 2026-08-12 retirement
  cleared every claimed value; the YAML nulled `evidence_tier`, but the column is
  `NOT NULL DEFAULT 6`, so all 109 DB rows still assert Tier 6. Every YAML header claims "Mirrors
  data/guidebook.db." L02 compares counts (109 = 109 → pass); cross-check compares identity → pass.
- **`decisions.delegation_rationale` — 3 rows disagree** (D-0158/59/60: populated in the DB by
  migration, key absent from the hand-edited YAML). L01's envelope is 6 of 22 columns; both holders
  run green.

Meanwhile the dual stores that *are* fully held — `governing_refs`↔links, the admissions triple —
agree, vacuously, being empty. **The reconciliation machinery is good where it exists; the live
divergences are exactly where the envelope is narrow.**

### 2.5 The apparatus is measured against a corpus that cannot falsify it

- 65 active checks (28 blocking, 34 advisory, 3 informational) + 16 quarantined; `--selftest` PASS;
  `--all` = 57 green, 8 advisory failures, 0 blocking failures.
- **13 of 65 active checks pass while examining zero records — 5 of them blocking.** The review
  adjudicated all 13: **every one is a legitimately empty corpus, none is a broken scoping
  predicate.** Five print explicit `EXAMINED: 0` / `NOTHING-IN-SCOPE` banners. The post-incident
  instrumentation is working.
- **The residual finding is narrower and real:** `run_checks.py` has no NOTHING-IN-SCOPE status. All
  13 render as `[PASS]`, indistinguishable from earned green, and `min_items` — the registry-level
  floor that would catch vacuity — is declared on 6 of 65.
- The reproducibility gate's six `CORE_INVARIANTS` tables: five are empty.
- 32 of 65 checks carry `basis: unattributed` — surfaced by the selftest as a tracked ratchet, not
  ignorance. Sharper and unremarked by the analysis: **`synthesis/opus-routing`, a declared hard
  floor, is claimed by no check at all.**

So "watching, not filling" is description, not indictment: the reset was deliberate and the writer
plan was ruled on 2026-08-13. But it does mean **nothing here has been tested against data**, in
either direction.

### 2.6 There is a third write path nobody modelled

The scheduled workflows write the canonical DB and then `git add data/guidebook.db` and push to
`main`. **`url_verification_runs` is not in `EXEMPT_TABLES`** (only `evidence_source_authors` and
`pipeline_runs`, per DR-2026-05-28, which states that adding one requires a new DR). So the one stage
with wired writers is wired *around* migrations-only, into a table with no DR cover.

That said — and this is the strongest positive result in the whole sweep — **a full rebuild from
migration history is currently exact.** Identical DDL text for all 67 tables, 18 views, 77 indexes;
equal row counts on all 67 tables, not just the six the blocking gate checks; identical content
hashes on 66 of 67, the sole difference being the by-design `applied_at`/`notes` ledger stamp. The
`AFTER_DATA` ordering mechanism is internally consistent, and `build_plan()` is a single ordering
authority for both replay paths. **The discipline holds today because the tables are empty. It will
not survive the first verify-urls run against a populated corpus.**

## 3. Lessons

1. **Ratifying a rule needs a caller sweep, with the same discipline as renaming a column.** Extend
   `CLAUDE.md` §0 rule 5 from identifiers to doctrine. All three BLOCKING governance findings, and
   one DR that overstated its own completion, are instances of the missing sweep.
2. **Never act on a single agent's absence claim.** Four of four analyses carried one; three of four
   would have driven wrong work — new schema that already exists at blocking level, deleting
   load-bearing tooling, or standing down on "blocking is decorative."
3. **A passing check must report its subject count, and the runner must surface it.** The per-check
   instrumentation exists and works; the runner flattens it. This is a `run_checks.py` change plus
   `min_items` declarations, not new checks.
4. **Define "unreachable" before culling on it.** The 44-file / 15.4k-line dead-code census is
   accurate as *"not CI-reachable"* — and includes `emit_data_migration.py`, the only sanctioned
   write path, plus `db.py` and the documented generators. A cull driven by that number deletes the
   write path.
5. **Empty is the cheapest moment for every structural fix and the worst moment for judging whether
   the apparatus works.** Both halves matter: do the schema work now; do not read green as proof.
6. **When two stores are kept, the comparison's envelope is the guarantee** — not the existence of a
   comparison. Both live divergences sit outside an envelope that passes.

## 4. Culling and consolidation

All items are proposals. File moves, retirements, and schema changes are owner-gated (§9-4; D-SCHEMA
is Change-Order gated).

### Tier 1 — actively false, one-line fixes

| Item | Why |
|---|---|
| `scripts/audit/readonly_db_open_audit.py` | Prints `40/40 read-only consumers open read-only`. **False**: its lower-case-local blind spot misses 6 scripts, 5 of them blocking checks, holding rw handles on the canonical DB. Fix the matcher, then the 6 opens. |
| `CLAUDE.md` §1 vs §0/§7 | §1 says "protected by CI"; §0/§7 say not branch-protected. **Both are now wrong** — `main` *is* protected. One fact, three statements. |
| `CLAUDE.md` §4/§6 | Describes the pre-057 migration layout and points at files now under `_archived/`. |
| `CLAUDE.md` §10 | Names a blocking check `session_pointer_resolvable` with zero hits in code, registry, or workflows (already on the books as R-22). The dispatcher provides half the described behaviour; the drift half does not exist. |
| `retired-vocabulary.yaml:306` | Excuses `verify_resolved_dois.py`'s `/tmp` default with "resolve-dois.yml sets the real path" — that workflow never runs the script. |
| `DecisionStatus` | Pydantic accepts `RETIRED`; the table CHECK accepts `WITHDRAWN`. Each rejects the other's member. Zero rows use either. |
| Conflict `status` | File layer and DB layer share 2 of 5 values. Zero rows. |
| `item_code` grammar | `^[A-K]-\d{2}$` in two graph extractors vs canonical `^[A-K]-\d{2}[a-z]?$`. `A-10b` exists today and matches only the canonical form. |

### Tier 2 — widen the parity envelopes (the two live divergences)

- **`decisions`**: extend L01 from 6 columns to full-field (it already loads both stores), or retire
  the YAML leg. The caller sweep is small and fully enumerated, and the corpus will never be this
  small again.
- **`jurisdictional_values`**: extend L02 / cross-check to field level, and adjudicate the direction —
  either the YAML headers stop claiming to mirror the DB on `evidence_tier`, or the column relaxes.

### Tier 3 — structural, cheap only while empty (owner-gated)

1. **The determination→claim edge** (§1). The single highest-value change in this document.
2. **Extend the derivation payload** over `state`, values, and unit — or add a second content hash.
   Zero rows to restamp today.
3. **Stamp the doctrine SHA on the row.** It appears nowhere in the database.
4. **Ref column + FK on `jurisdictional_values`** — migration 053's own header already conceded "the
   `ref_id` FK that table has never had." Nullable at birth; the parent is deliberately empty.
5. **A verbatim-extract field on `jurisdictional_values`**, and **make `claim_text` unconditional**
   (protocol currently requires it only for qualitative/definitional claims — so a *quantitative*
   determination's source words are optional, which collides head-on with the backend-vetting ruling).
6. **Unify the 16-column locator scheme** across the value-bearing tables (`source_value_extractions`,
   `reasoning_doc_citations`, `jurisdictional_values`, and `spec_value_probes`, which has neither
   locators nor extract). Hand-duplicating 16 columns per table invites exactly the drift above; this
   is also the uniformity ruling in structural form.
7. **Give `evidence_sources.tier` a floor.** It is bare `INTEGER` — no CHECK, no `ENUM_GUARDS` entry,
   not covered by the B-series vocabulary checks. `tier = 7` passes everything, on the tier the whole
   anchoring doctrine runs on.
8. **Resolve `url_verification_runs`**: a DR-backed exemption, or route it through the sink.

### Tier 4 — cull (owner-gated)

> **CORRECTED 2026-08-14 — this list was too aggressive.** The retirement planning pass re-verified
> every candidate with `git grep` and rescued five: the **`economics_entries` family** and
> **`search_candidates`** are read by *blocking* gates (`test_db_integrity` C06 and the
> definition-of-done rules R12/R7) — a table a gate refuses to pass without is not dead;
> **`access_needs`** and **`access_need_icf`** are reset-preserved frame carrying a live FK from
> `access_need_axis_map`, which nothing proposed culling; **`weighting_profile`** is cited by
> ratified doctrine; and **`source_locators`** is the reset's deliberate recovery stash, to be wired
> rather than retired. Three further corrections: `scripts/db/**` is **3** files, not 13;
> `validate_db.py` is **repaired**, not broken; and nine candidates called "no content" do hold rows.
> The error was mine — the reviews flagged gate-readership as the dead-vs-load-bearing criterion and
> this list did not apply it. The verified sequencing is in
> `workplan/2026-08-14-remediation-workplan.md` §6.

**Tables** — safe now, after the correction above: `db_meta`, `population_reclass` (its retirement
already sanctioned by a ratified DR), and the `v_source_reach` view. Blocked on a named prerequisite,
not free: `rooms`/`room_items`, the case-study family, the frozen search grids, `access_duration`,
`access_stakes`. On hold with a blocker: `situations` (DG-NON), `external_root_registry`,
`life_stage_modifiers`. Migrations are forward-only; re-adding when a renderer exists is cheap, and
carrying genuinely dead tables costs census confusion every audit cycle.
Finish the `search_coverage` / `search_languages` freeze with a `DROP TABLE` so the retirement is
structural rather than behavioural. **Do not build writers for those two** — it would un-freeze a
retirement.

**Scripts:** `scripts/db/**` (3 files, targets a database that does not exist); `scripts/migrate/**`
(keep `migrate_decisions.py` while the dual store lives); `scripts/convert/**` (13 files, 2,669 lines,
no legacy status and absent from the shared `EXCLUDE_PARTS` convention); `init_db.py`;
`migrate_evidence_sources_v2.py`; `validate_db.py` (quarantined; repaired but unselected);
`test_generate_parts_4_2.py` (exits 0 having asserted nothing — a test that cannot fail is worse than
no test); `verify_resolved_dois.py` (wire it into `resolve-dois.yml` or archive it — do not leave it);
`generate/room_page.py` + `population_page.py` (crash-by-construction against six phantom table names,
and undriven — fix and wire, or archive; the present middle state is the worst of the three).

**Consolidate:** `v_source_reach` into `v_source_reach_all` (the honest one); shallow
`migration_reproducibility` into `--deep` once deep is promoted; `validate_commits.py` into
`check_commit_msg.py`; the three ~12,000-line probe logs down to the newest.

**Repair rather than cull:** `register_integrity_check` reports a **missed mutation in its own
selftest**; `test_graph_audit` crashes on the empty `connections` table.

### Do NOT cull, despite appearing in the dead-code census

`emit_data_migration.py` (the only sanctioned write path), `db.py`, `generate_parts.py`,
`schemas/*.py` (all dynamically imported by a registered check), `item_audit_pipeline.py` and
`audit_consolidator.py` (skill-invoked; their canonical writes are a write-path governance question,
not a dead-code one).

## 5. Flagged for the owner, not acted on

**28 of the 93 active item names carry quantified values.** `Acoustic Ceiling Panels (NRC ≥0.85)`,
`Circadian Lighting (≥150 EML Minimum at Eye Level in Daytime Spaces)`, `Sensory Room / Quiet Room
Provision (≥8 m², one per floor or per 500 m² GFA)`, `Corridor Clear Width (≥1200 mm Minimum on All
Primary Routes)`, and 24 more.

The clean-room reset emptied `specifications` and retired the E-08 exemplar; commit `6f512b9`
quarantined trial artefacts specifically "so no pre-existing item seeds content research." That
quarantine covered the artefacts. It did not reach the item names — which are the frame every future
determination is written into, and which currently state the answers the research is meant to derive.

This is a DG-NON-adjacent judgment about the frame, so it is recorded here rather than acted on.

---

*Read-only audit throughout; the canonical database was opened `mode=ro` and the tamper reproduction
ran on a scratch copy. No repository file was modified by any agent. This synthesis is the single
committed artifact.*
