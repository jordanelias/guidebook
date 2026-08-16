# 2026-08-14 — Remediation workplan for the six-agent audit

**Companion to** `workplan/2026-08-14-pipeline-audit-synthesis.md`. The synthesis said what is wrong;
this says what to do, in what order, and what only the owner can decide.

**Provenance.** Four read-only planning passes — governance, schema/provenance, executable-layer,
retirement — each re-verifying the synthesis's claims rather than inheriting them, each prototyping
its migrations against a scratch copy of the database. Three of the four corrected the synthesis. The
corrections are in §8.

**Nothing here has been executed.** Every migration, file move, and doctrine edit below is a proposal.
Schema changes are D-SCHEMA (Change-Order gated); file moves and retirements are owner-gated;
DG-NON items are marked and are not pre-decided.

---

## 0. Time-critical: one item has a deadline of 2026-08-15 06:00 UTC

`verify-urls.yml` fires on cron `0 06 1,15 * *` — **the next run is tomorrow morning**.
`scripts/verify_urls.py` inserts a `url_verification_runs` row *even when the candidate pool is zero*,
and the workflow then commits `data/guidebook.db` to `main`.

`url_verification_runs` is **not** in `EXEMPT_TABLES` (`scripts/audit/migration_reproducibility.py:65`
— only `evidence_source_authors` and `pipeline_runs`, per DR-2026-05-28, which states that adding one
requires a new DR). So that run ends the currently-exact rebuild reproducibility reported in the
synthesis, and turns `--deep` red for a reason unrelated to any data problem.

**The fix is ten lines** — an early return when `pool_size == 0`, printing a `NOTHING-IN-SCOPE`
verdict and writing no row (prototyped; `test_url_verifier` unaffected at 25/25, `--deep` still PASS).
It needs no workflow edit, because the workflow's own no-change guard already skips the commit when
the database is byte-identical; the guard only fails today because the script writes a row for
nothing.

This is a bridge, not the resolution. The durable answer is owner decision **#5**.

---

## 1. How the four tracks interlock

> ## ⚠ The allocation below is STALE — corrected 2026-08-16, do not use it as written
>
> Slots **058, 059 and 060 were consumed by other work** after this plan was written, and are on
> `main` now: `058_status_vocabulary_ratification.sql`, `059_tier1_retirements.sql`,
> `060_restore_superseded_status.sql`. A session following the table below would collide on the first
> migration it wrote. `workplan/2026-08-15-instrument-status-backfill-plan.md` §6 already noted
> "058–060 are used" without correcting the table it was reading from — so the stale allocation
> survived the one pass that spotted it.
>
> **Re-allocation, to be confirmed when the Group 3 batch is ratified (owner decision #4):** the six
> prototyped schema migrations shift **058→061, 059→062, 060→063, 061→064, 062→065, 063→066**; the
> ratification trigger, the Tier-1 retirement and the Tier-2 retirements follow at **067, 068, 069**.
> The prototypes were tested at their old numbers; renumbering is mechanical (the filename and the
> `user_version` target), but it has **not** been re-prototyped at the new numbers, and the row-level
> content is unchanged. Note that the retirement track's 065 is *already partly executed* —
> `059_tier1_retirements.sql` on `main` is the Tier-1 batch that this table listed at 065 — so that
> row needs re-deriving against what actually shipped, not just renumbering.

**Migration numbering — reconciled.** The schema and retirement plans both claimed 058 and 059.
Allocation, chosen so the six prototyped schema migrations keep their tested numbers:

| Slot | Contents | Track |
|---|---|---|
| 058 | `constraint_floor` — evidence-source CHECKs, tier floor, partial UNIQUE on doi | Schema |
| 059 | `jurisdictional_values_provenance` — ref FK, claim_text, tier CHECK, drop `spec_id` | Schema |
| 060 | `claim_capture_uniformity` — unconditional `claim_text`, locator set on probes | Schema |
| 061 | `determination_provenance` — `doctrine_sha`, `outcome_sha` (ADD COLUMN only) | Schema |
| 062 | `specification_claim_links` — **the determination→claim edge** | Schema |
| 063 | `source_excerpts` — the screenshot/extract table | Schema |
| 064 | ratification trigger (writer plan Phase 0's last piece) | Writer plan |
| 065 | retire dead tables — Tier 1 | Retirement |
| 066 | retire conditional tables — Tier 2, per-package as gates clear | Retirement |

No table is touched by both tracks, so the ordering above is a convention, not a dependency.

**Cross-track dependencies:**

- Executable commit 9 (`RANGE_GUARDS` + range checks at the write path) is *complementary to*, not a
  substitute for, the table CHECK in migration 058. Both, or the tripwire has nothing behind it.
- Retirement package 2.E (`migrate_decisions.py` + its guard) is blocked on owner decision **#2**.
- Retirement consolidation 6.2 (shallow reproducibility folded into `--deep`) is blocked on promoting
  `--deep` to blocking, which is blocked on decision **#5**.
- The schema track's `claim_text`-unconditional rule edit
  (`skills/reasoning-doc-citations_SKILL.md:52,194`) is a governance-doc change and rides the
  governance track's conformance sweep.
- The schema additions are inert until the writer plan's sink writes them: `assess_cell.py` must
  stamp `doctrine_sha`/`outcome_sha` and emit claim-link rows, and `db.py` needs
  `insert_specification_claim_link` and `insert_source_excerpt`.

**The one genuine disagreement between planners** is decision **#1** below. It is surfaced, not
resolved.

---

## 2. Track A — executable-layer correctness (9 commits)

Ordered; all prototyped against a scratch copy.

1. **The zero-subject scheduled write** (§0 above). Urgent.
2. **Repair two broken self-tests, admit suffixed item codes.** `graph_audit.py:277` raises
   `TypeError` on the empty `connections` table (`fetchone()[0]` on None).
   `register_integrity_check` misses a mutation in its own selftest — root cause: with
   `specifications` at 0 rows the DB→doc direction can never fire, so the fix injects a ghost
   determination into a temp copy (12/12 FIRED after). And the two graph extractors use
   `^[A-K]-\d{2}$` while `A-10b` exists today.
3. **The read-only audit's false certificate.** `readonly_db_open_audit.py` prints
   `40/40 read-only consumers open read-only`. Widening the matcher finds **nine read-write connects
   across eight reader files** — the six review-B named, plus `generate_parts.py:435` and
   `tools/regenerate_vetting_surface.py:41`, whose docstring says "Read-only" while it opens rw. None
   legitimately needs rw.
4. **`NOTHING-IN-SCOPE` in the runner** — the centrepiece; see §3 below.
5. **Extend the `EXAMINED:` contract** to the remaining zero-subject checks.
6. **Declare the floor** — `min_items` or an explicit `no_floor` on all 65 checks, with a new
   selftest assertion (C8) forcing every *future* check to declare its vacuity regime. That
   assertion is the structural half; without it this is a one-time sweep that decays.
7. **Widen L01 to full-field** and reconcile the three drifting decision rows. Prototyped: detects
   exactly D-0158/59/60 on exactly `delegation_rationale`, zero false positives across the other 157.
8. **Stale prose in executable files**, including `preflight.sh:33-36` asserting `test_db_integrity`
   is red on main when it now passes 70/70. Also fixes `context_map_fresh`, already advisory-red at
   HEAD because the synthesis commit skipped regeneration.
9. **A floor under `evidence_sources.tier`** at the write path — a new `RANGE_GUARDS` table
   (`ENUM_GUARDS` cannot see unquoted integer literals) plus B07/B08 range checks.

### 3. The vacuity-reporting design

The defect is narrower than the synthesis stated, and therefore fixable. The 13 zero-subject checks
are *correct*; five already print `EXAMINED: 0` / `NOTHING-IN-SCOPE` banners. **`run_checks.py`
renders all of them as a plain `[PASS]`.**

The mechanism is a **parsed line**, extending the `EXAMINED:` convention the checks already use —
not an exit code (the 0/1 space is spoken for), not a structured sidecar (65 scripts would need
rewriting). Prototyped: `--selftest` stays PASS and `--all` renders

```
RESULT: PASS — 51 check(s) green, 5 nothing-in-scope, …
```

with the five already-instrumented checks flipping immediately and **zero script changes** for them.

Why this does not become ceremony: a reviewer seeing `NOTHING-IN-SCOPE` on a *blocking* check knows
the gate did not run, and `min_items` converts "should have had subjects" into a failure rather than
a green. This is the repo's named recurring failure mode, produced four times before; the fix has to
be structural, and C8 is the structural part.

---

## 4. Track B — governance sweeps (9 commits, A→I)

The three blocking findings are all *incomplete sweeps of ratified decisions*. Two determinations
shaped the plan, both verified rather than assumed:

- **Amend-in-place on the append-only ledger is licensed.** Four ledger rules already carry dated
  in-place reconciliation clauses citing their DRs, so B1/B2 use that established form rather than an
  append-and-supersede workaround.
- **The re-attestation cascade is materiality-scoped, not the flat five-commit window.**
  `RE_ATTESTATION_WINDOW = 5` is a dead constant; the audit reads `governance/doctrine-deltas.json`.
  Both `CLAUDE.md` §8 and PI rule #11 still describe the retired model, and both get corrected.

**Commit A is the doctrine batch — one SHA rotation.** The Tier-3 row at
`mission-and-epistemics.md:115`, the two-marker bullet at `:136`, and the stale status stanza at
`:190`, shipped together with an atomic `doctrine-deltas.json` entry carrying an **empty materiality
set** — because each edit conforms the anchor to a position already ratified into an earlier state.
The discharged re-attestation obligation is therefore **zero of 82 attestations**, verified by
`adherence_log_audit --check window` printing nothing.

Commits B–C carry the ledger amendments and the full conformance sweep across `tier-system.md:97`,
`armature_v4.md`, three skills and five reference files, with a zero-hit acceptance grep. D–F run in
parallel (cosmetics; `CLAUDE.md` structural claims; skill-registry completeness). G adds forward
notes to the DRs that overstated their own sweeps and performs the merge-ratification flips —
explicitly *not* flipping the DG-NON one, since merge does not manufacture a DG-NON decision.

### Commit H — the mechanism that would have caught all three

`CLAUDE.md` §0 rule 5 requires a caller sweep for renaming an identifier. It requires nothing for
*repealing a rule*. That asymmetry is why B1, B2 and B3 exist.

The fix extends the **existing** retired-vocabulary apparatus rather than adding a register:

- `decision-protocol.md` gains §3.5 — a superseding DR must carry a **Ratification Sweep** section.
- Mechanically-matchable *repealed formulations* are registered alongside retired vocabulary. Three
  are seeded, and each demonstrably matches the text that survived B1/B2/B3.
- `ratification_sweep_audit.py` enforces the coupling, registered **advisory** per the promotion
  discipline, with `EXAMINED:`/`NOTHING-IN-SCOPE` banners and a mutation-tested selftest.
- Its `min_items: 1` is permanently satisfiable — its own enabling DR is always in scope — so it
  cannot become another gate that passes on zero subjects.

Its D-0161 register entry lands as a **YAML append paired with a data migration**, writing the same
fields to both stores. Writing only the YAML is precisely the omission that produced the live
`delegation_rationale` divergence.

---

## 5. Track C — schema and provenance (6 migrations, all prototyped)

All six applied cleanly to a scratch copy under `foreign_keys=ON` with zero new FK violations, all 18
views executing, and a full rebuild through the repo's own replay path returning **identical on all
173 DDL objects, all row counts, and per-table content hashes** (sole diff: the by-design ledger
stamp). On the migrated rebuild: `test_db_integrity` 70/70, `validate_evidence_state` PASS,
`validate_schema` 20/20.

**The four design calls, with the reasoning that decided them:**

1. **The determination→claim edge (062)** — a polymorphic junction `specification_claim_links`, with
   real FKs to extractions, citations *and* jurisdictional values, exactly one non-NULL, plus a
   `role`. An extraction-only junction was rejected because it fails the uniformity ruling: a
   determination anchored on a citation, or on an Option-A code-consensus value, would get no edge at
   all. Overloading `specification_source_links` was rejected because that table already carries the
   H01/H02 parity and `derivation_sha` contracts, and the cardinality is wrong.
2. **Hash coverage (061)** — a **second** hash, `outcome_sha`, over state, values, unit, tier basis,
   design scale and the two stratum flags, chained to `derivation_sha`. Not an extension of the
   existing payload: K01 is documented as a derivation/identity attestation, and silently repurposing
   it would trade one honest instrument for one dishonest one. Prototyped against review-D's exact
   tamper (values moved, mm→cm): the new check catches it, K01 still passes — which is correct for
   both.
3. **Locators (060)** — per-table duplication with a mechanical parity check (`min_items: 68`), not a
   shared `locators` table. A shared table forces a two-insert id handoff, the exact hazard the writer
   plan already flagged.
4. **Screenshots (063)** — a `source_excerpts` table with the image file gitignored and the SHA-256,
   caption, page and crop committed. Verifiable evidence without binaries in git.

Also settled: `jurisdictional_values.spec_id` is NULL in all 109 rows and is a TEXT column that could
never FK an INTEGER primary key, so 059 drops it rather than repairing its false comment.

**A trap worth recording.** The first prototype *failed*: SQLite auto-rewrites dependent views on
`ALTER TABLE RENAME` under `legacy_alter_table=0`. The fix follows house precedent from migration 039
— drop and recreate the views verbatim, never rename the old table.

**End to end:** the plan proves on a synthetic fixture that after 058–063 a single edge-walk returns,
for each determination, its words, its pinpoint locator, and its screenshot path — uniformly across
the research, citation and regulatory strata. That is rulings (i), (ii) and (iii) in queryable form.

---

## 6. Track D — retirement

**The reachability definition matters more than the list.** A cull driven by "not CI-reachable" would
delete `emit_data_migration.py` — the only sanctioned write path — along with `db.py`,
`generate_parts.py`, the dynamically imported `schemas/*.py`, and the skill-invoked audit pipeline.
The plan uses a six-test union instead: registry/CI, **gate-readership**, contract or doctrine
citation, operator CLI paths, transitive imports, and scheduled jobs. All caller sweeps use
`git grep`, never ripgrep, because the root `.ignore` hides seven directories and would make an
unsafe deletion look safe.

**Tier 1 — safe now (10 packages):** `db_meta` + `init_db.py` + the `db.py init` subcommand;
`population_reclass` (retirement already sanctioned by a ratified DR); the `v_source_reach` view;
`scripts/db/**` (3 files, not the 13 I wrote in the synthesis); `scripts/migrate/**` minus the
decisions importer and its guard; `scripts/convert/**` (13 files, 2,669 lines); the one-time evidence
migration; `validate_db.py` and its subcommand and registry entry; the assert-nothing test; and the
duplicate probe logs. Each carries its full sweep, `_archived/` destination mirroring the origin path,
retirement-record text, registry consequences and reversal cost.

**Tier 2 — safe after a named prerequisite (7 packages),** each blocked on a specific decision or
patch: the room stratum, the case-study family (needs the R12 contract amendment first, since
`research_contract_sync` is blocking), the frozen search grids (three real readers to patch, plus a
DR superseding the "frozen, preserved" clause), two access-vocabulary tables, the decisions importer,
the reproducibility consolidation, and `verify_resolved_dois.py`.

**HOLD (5):** `situations` (DG-NON, a ratification-record-named Co-1 entity — recommend keep),
`external_root_registry` (three views, one contract-cited), `life_stage_modifiers` (doctrine-cited),
`population_page.py` (working but undriven — a wiring question, not a retirement), and the newest
probe log (cited by the live writer plan).

Migrations 065 and 066 were prototyped: rebuild reproduces exactly, `test_db_integrity` 70/70,
`validate_evidence_state` PASS, shallow and `--deep` reproducibility both PASS.

**A trap found in passing:** `migration_reproducibility.py:89-97` fingerprints the repository's
migrations directory while its rebuild honours `GUIDEBOOK_MIGRATIONS_DIR` — a stale-cache mismatch
that produces a **spurious FAIL** on a blocking gate.

---

## 7. Owner decisions

Deduplicated across the four plans. Nothing below is pre-decided.

**#1 — `jurisdictional_values.evidence_tier`. The two planners disagree; you arbitrate.**
109 of 109 rows diverge (YAML `null`, DB `6`, because the column is `NOT NULL DEFAULT 6`).
- *Relax the column to nullable and null the 109* — reads the 2026-08-12 retirement's "all claimed
  values are cleared" as reaching `evidence_tier`, and makes the YAML mirror claim true again.
- *Keep `NOT NULL DEFAULT 6` plus a 1–6 CHECK* — reads Tier 6 as true by definition for statutory
  values, and the YAML gains a documented exception instead.
Not deciding has a cost: the divergence becomes a standing advisory red, which trains people to
ignore the check.

**#2 — Retire `data/decisions/decision_register.yaml`?** The caller sweep is complete and every
caller's replacement is specified. Either answer is stable; the unstable thing is today's unratified
middle, where a "dual store pending sign-off" is held by a six-of-twenty-two-column envelope.

**#3 — Two enum vocabularies, zero rows each.** Decision status: `RETIRED` (recommended — matches the
documented lifecycle and the existing counters; the DB CHECK changes) or `WITHDRAWN`. Conflict status:
ratify the DB set (recommended) or declare the file-layer set a distinct concept, which then needs a
distinct name.

**#4 — Ratify migrations 058–063** (D-SCHEMA ×6, Change-Order), with sub-decisions on the claim-link
`role` vocabulary (enum birth is its own D-SCHEMA decision), the excerpt media-type vocabulary, and
whether the new integrity checks land blocking-at-birth on a zero-subject corpus or advisory-first.

**#5 — The third write path.** Route the scheduled jobs through the migration sink (extends the
2026-08-13 uniform-sink ruling), or ratify a widened exemption in a new DR — which institutionalises
the third path and needs column-level exemption machinery that does not exist, against the
centralization maxim. **Decide before 2026-08-15 06:00 UTC, or land §0's guard.**

**#6 — Jurisdiction scope (DG-NON).** 46 in the multilingual skill and PI rule #9, with blocking
completion gates; 24(+2) canonical in jurisdiction-philosophy; 27 in the schema enum, so 19 of the 46
cannot be encoded at all. The skill's own checkpoint counts `/24`. Options: 46 as search matrix with
24(+2) as the coverage requirement; narrow to canonical; or ratify 46 as coverage, which is a
Change-Order enum extension and the largest research commitment. Sub-item: the canonical prose says
24 countries while its own table lists 25.

**#7 — "cross-population" (partially reverses an owner-adopted decision).** The ledger retires the
term and then uses it in three live rules and a live skill name. License it as the conflict-domain
term of art (cheapest); enforce the retirement fully (a governed skill rename with
attestation-identifier continuity); or document the status quo.

**#8 — Retirement approvals:** the Tier-1 batch; the room stratum (register as frame, or reset — the
question is already queued); the R12 case-study contract amendment; superseding the search grids'
"frozen, preserved" clause; the two access tables; and `verify_resolved_dois.py` (wire, recommended,
or archive).

**#9 — PI v10.15.** The diff list is assembled; one item is conditional on #6. One paste.

**#10 — The required-check set.** `main` **is** branch-protected — I verified it against the API
(`"protected": true`), resolving a question one planner could not settle from inside the container and
correcting `CLAUDE.md` §0 and §7, which say the opposite. Since blocking checks now genuinely gate
merges, confirm the required set matches `references/tooling-register.md` §6.7 — in particular that
the DB-integrity job is *not* required until its backlog clears.

**New Decision Records:** ratification-sweep gate (D-OP/DG-REVIEW, register-captured);
jurisdiction scope (D-DOCT/DG-NON, PROPOSED only); cross-population vocabulary (D-METH, upgraded to
explicit owner review); the enum ratification (D-SCHEMA); the scheduled-writer path (D-OP); and — only
if #2 is yes — the register retirement.

---

## 8. Corrections to the 2026-08-14 synthesis

The planners re-verified the synthesis and broke parts of it. Recorded rather than quietly amended:

- **The cull list was too aggressive.** Five candidates are load-bearing: the `economics_entries`
  family and `search_candidates` are read by *blocking* gates (a table a gate refuses to pass without
  is not dead); `access_needs`/`access_need_icf` carry a live FK from a table nobody proposed culling;
  `weighting_profile` is cited by ratified doctrine; `source_locators` is the reset's deliberate
  recovery stash. The synthesis's Tier 4 has been corrected in place.
- **`scripts/db/**` is 3 files, not 13.** `validate_db.py` is repaired, not broken. Nine candidates
  described as having no content do hold rows.
- **`main` is branch-protected** (§7 #10), which the synthesis reported correctly and `CLAUDE.md`
  still contradicts.
- **The re-attestation model** in `CLAUDE.md` §8 is retired; materiality, not a commit window.
- **Two more read-write handles** than review-B found, including one in a file whose docstring claims
  read-only.

---

## 9. Deliberately not planned

The writer plan's Phase 1–3 (the sink itself) — it is already ruled on and sequenced. Content
research of any kind. The 28 item names carrying quantified values, flagged in the synthesis §5 and
still awaiting an owner ruling, since the item roster is frame. Promotion of any new check to blocking
before its false-positive rate is known.
