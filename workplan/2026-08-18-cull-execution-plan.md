# 2026-08-18 — Cull execution plan

**Status:** PROPOSAL. Nothing here is executed. Every phase is owner-gated; §7 lists what only the
owner may decide.

**Provenance.** Six exhaustive read-only sweeps (Fable 5) over all 2,133 tracked files, merged by
Opus 5 into a 20-claim digest, then adversarially critiqued by a cold Opus 5 agent that had not
authored the digest. Model-substitution debt is recorded in
`workplan/2026-08-18-model-substitution-log.md`.

> **DEBT DISCHARGED 2026-08-18 — Fable 5 re-examination complete. See §14.**
> **Phase 4a must not be executed as written.** It culls `scripts/audit_consolidator.py`, which an
> **active skill invokes** — `skills/item-audit-pipeline_SKILL.md:252` runs
> `python3 scripts/audit_consolidator.py` as Step 8, "always runs last". The reachability analysis
> could not see it, because a caller written in skill prose is invisible to a call-graph by
> construction. Verified independently. Eleven further findings, four of them overturning claims
> this plan makes, are recorded in §14.

**The goal this plan is measured against**, in the owner's words: *minimize code infrastructure so we
can focus on proper content generation from research; as little code as possible without sacrificing
data integrity.*

---

## 0. Read this before anything else

### 0.1 The merged digest was defective. Execute from the sweeps, not from it.

I compressed six sweeps into a 20-claim digest. The critique's verdict on that compression is blunt
and correct: it is *"a lossy and in places distorting compression of a better document."* Four defects
were introduced **by the compression, not by the sweeps**, and all four are mine:

| Defect | Reality |
|---|---|
| Named `db_handle_contract` as one of five data-integrity floor members | **The check does not exist.** `git grep` → zero hits. One-fifth of the asserted floor was a phantom |
| Named `website/` as a 3,537-line cull target | **The path does not exist.** `ls -d website` → no such file; `git ls-files website` → empty |
| "63 of 70 retired-vocabulary occurrences" in the pre-reset record | **35 of 70.** Four of the eleven named files hold zero |
| "86 plans → 8, by proof-by-construction" | **The eight are never named.** The source census says *one* is load-bearing. Unverifiable as written |

Two further numbers were wrong in the digest and are now settled by direct measurement:

- **DDL constraint counts.** Digest said 81 / 137 / 5. Critique said 81 / 123 / 7. **Measured: 80
  `REFERENCES`, 123 `CHECK` (regex `\bCHECK\s*\(`; only 45 with the literal spelling `CHECK(`), 7
  `UNIQUE`.** Three agents produced three answers because the count is spelling-sensitive. **The
  counts are not load-bearing and should not be cited again** — the mechanism finding below is.
- **Empty tables.** "43 of 66" → **42 of 65** (66 including `sqlite_sequence`).

**Operative instruction: where this plan and the digest differ, this plan governs; where this plan and
`workplan/2026-08-18-structural-census-and-cull-list.md` differ, the census governs on anything it
covers.** The census is better hedged, correctly refuses to cull dormant checks, and contains none of
the four phantoms above.

### 0.2 The plan's own premise has inverted: every named red gate is now green

Measured this session:

| Gate | Registry / doc says | Actual |
|---|---|---|
| `test_db_integrity` | "RED on main (63/69 checks pass as of 2026-08-04)" | **RESULTS: 72/72 passed**, exit 0 |
| `migration_reproducibility --deep` | "RED… `evidence_sources` diverges on 277 rows" | **VERDICT: PASS**, 63 identical, 2 exempt |
| `validate_population` | "first real run surfaces 5 findings" | **PASS, 0 findings, 425 rows** |
| `adjudication_integrity` (quarantined) | "RED — 274 tier inconsistencies" | **PASS**, 0 inconsistencies |
| `code_currency_audit` (quarantined) | "RED" | **0 issues**, exit 0 |
| `CLAUDE.md:344` | "two blocking gates are red on `main` today" | **none found** |

The apparatus is not obstructing anyone. It is **silent** — and it is silent because the corpus is
empty. `run_checks.py --selftest` reports *"checks with a real floor: 31 of 65"*: **34 of 65 checks
cannot currently be falsified by any data.** Culling them saves nothing today and costs exactly when
content generation restarts, which is the goal.

### 0.3 The honest limit of this whole exercise

This program removes roughly **101,000 lines of attention cost**. It adds **zero rows** to
`evidence_sources`. It does not re-enter the pre-reset stash
(`_archived/data/corpus-pre-reset-2026-08-06.db`: gaps 313, connections 273, evidence_sources 863).
`scripts/audit/table_connectivity.py` reports **`FULLY-EVIDENCED WALKS: 0 of 80 ACTIVE topics`** before
and after.

**The ratio improves from 345:1 to roughly 265:1 and nothing has been researched or written.** No claim
in the digest addressed the recovery path, and that omission is this plan's largest defect against the
stated goal. **The recovery plan should be written before Phase 5, not after** — re-entering the stash
changes which checks have subjects, and therefore changes the cull list.

---

## 1. The mechanism finding that reshapes everything

The digest claimed five blocking Python checks are replaceable by DDL constraints *"because every legal
write passes `migrate_db.py` with `PRAGMA foreign_keys=ON`."*

**That mechanism is false.** `scripts/migrate_db.py:192` runs `PRAGMA foreign_keys = OFF` before
`executescript`, and `:325` does the same in the rebuild path. Foreign-key integrity is enforced
instead by a **post-hoc `PRAGMA foreign_key_check` set-difference** — which has three holes:

1. **Grandfathering** (`:188`) — violations already present are permanently exempt.
2. **A `BOOTSTRAP` escape hatch** (`:202`, `:337`) — a migration whose first 500 bytes contain
   `BOOTSTRAP` downgrades new violations to a warning. Latent: no current migration uses it.
3. **The schema path performs no FK check at all.** `scripts/migrations/057_baseline_2026-08-12.sql`
   is a *schema* migration containing **5,072 `INSERT INTO` statements** and setting
   `PRAGMA foreign_keys = OFF` at its line 62. **The bulk of the database's data entered through a
   path with zero foreign-key enforcement.**

Proven rather than argued, in a scratch DB: with `foreign_keys` at SQLite's default `0`, an FK-orphan
`INSERT` is **accepted**; a `CHECK` violation is **rejected**; a `UNIQUE` violation is **rejected**.

**Consequence — `CHECK` and `UNIQUE` substitutions are sound; FK substitutions are not.**

### 1.1 The real hole in the data-integrity floor

`git grep -l foreign_key_check` over live code returns five files. **None of them is a blocking check:**

| File | Status |
|---|---|
| `scripts/migrate_db.py` | not a check |
| `scripts/migrations/057_baseline_2026-08-12.sql` | a migration |
| `scripts/audit/population_integrity_audit.py` | **advisory** |
| `scripts/tests/test_evidence_cell_state_2_3.py` | **advisory** |
| `scripts/tests/probe_pipeline.py` | **unregistered** |

And `grep -c foreign_key_check scripts/tests/test_db_integrity.py` → **0**. The floor check does
semantic orphan checks at `:358` and `:513` but never runs the pragma.

**Nothing blocking observes referential integrity on the committed database.** It is clean today —
that is a fact about the current file, not a guaranteed property.

**The remedy is a net code reduction:** a ten-line blocking check running `PRAGMA foreign_key_check`
replaces ~283 lines of hand-rolled join-checking in `validate_items` + `validate_axes`. That is the
shape this whole exercise is looking for — **delete a duplicate, don't add a guard** — and it is the
one place where adding code is correct.

---

## 2. Phase 0 — Correct the record (mechanically safe, no cull)

**Prerequisite:** none. Every later phase reasons from these facts; four sweeps reasoned from stale
ones. **Acceptance test written before the work** — capture the pre-state of every command cited.

| # | Action | Path |
|---|---|---|
| 0.1 | Rewrite `test_db_integrity`'s `note:` — "RED (63/69)" is false; it is 72/72 | `governance/check-registry.yaml` |
| 0.2 | Rewrite `migration_reproducibility_deep`'s `note:` — the 277-row divergence dissolved with the reset; EXAMINED is 65, not 67 | same |
| 0.3 | Rewrite `validate_population`'s `note:` — the 5 findings are gone; PASS on 425 rows | same |
| 0.4 | Correct `CLAUDE.md:344` — "two blocking gates are red on `main` today"; none are | `CLAUDE.md` |
| 0.5 | Correct six quarantine `reason:` fields (§2.1), each stamped with the date and the command that re-derived it | `governance/check-registry.yaml` |
| 0.6 | Add `supersession-audit` to the active-skills block | `references/skill-registry.md` |
| 0.7 | Add five ids to `EXTRA_RULE_IDS` — **urgent, see below** | `scripts/audit/adherence_log_audit.py:84` |
| 0.8 | Fix `governance/functional-taxonomy.md:9` — it cites `working/taxonomy/staged_schema_functional_axes.sql`; the whole directory does not exist | `governance/functional-taxonomy.md` |

**0.7 is a live latent failure, not tidiness.** `attestations/decisions_DR-2026-08-06-clean-room-
evidence-reset.json` cites `decision-protocol`, `evidence-architecture`, `tier-system`,
`migration-discipline`, `retire-not-delete` — none registered. `attestation_schema` is **blocking**,
and the audit scopes to attestations in the changeset. **The next commit that touches that file turns a
blocking gate red.** Exactly one of 86 attestations is affected; the fix is one list edit.

### 2.1 The six false quarantine reasons

| Check | Registry says | Measured |
|---|---|---|
| `adjudication_integrity` | RED, 274 inconsistencies | **PASS**, 0 |
| `code_currency_audit` | RED | **0 issues** |
| `pre_rehab_banner_audit` | RED, 6 slugs | exit 1, cohort 70 files / 68 slugs |
| `validate_audit_runs` | "Green (87 runs)" | **PASS (0 runs)** |
| `validate_temporal` | generator `scripts/convert/version_retrofit.py` "still exists" | `scripts/convert/` **archived 2026-08-15** |
| `full_db_metadata_verification` | network-bound ~298s | **UNVERIFIED** (not executed) |

**One correction to the digest's own reasoning:** it said `validate_audit_runs` "passes against a table
that does not exist." **`item_audit_runs` exists and is empty**; `scripts/validate_audit_runs.py:47`
handles genuine absence with an explicit `SKIP`. The digest confused *empty* with *absent* — the exact
conflation `CLAUDE.md` §10 warns about.

**Acceptance:** `adherence_log_audit.py --check schema` PASS; `run_checks.py --selftest` PASS; every
corrected note re-derivable by the command it cites.
**Reversal:** `git revert` — text only, no path moves.

---

## 3. Phase 1 — Search-surface reduction (the best row in the plan)

**Prerequisite:** Phase 0. **Owner-gated only because `.ignore` is** (`CLAUDE.md` §10; DR-2026-08-06).

```diff
 # --- retired-but-preserved -------------------------------------------------
 _archived/
 workplan/_superseded/
+
+# --- deprecated-in-place: self-declared superseded, awaiting archive move ---
+workplan/deprecated/
+skills/deprecated/
```

Bare `dir/` form is correct — `.ignore` already uses it for `workplan/_superseded/` and `audits/`, and
the file's own syntax note (verified) says bare `dir/` cannot be re-included but `dir/**` can. Neither
new entry needs a negation.

**Budget: 28 files / 7,480 lines** off the agent search surface — `workplan/deprecated/` 16 files /
6,324 lines, `skills/deprecated/` 12 files / 1,156 lines. Exact, measured twice.

**Zero files moved. Zero code affected** — `workplan_naming_audit.py` globs `workplan/*.md` at top
level only. **Reversal: delete two lines.**

**Acceptance, before:** `rg --files workplan/deprecated skills/deprecated | wc -l` → 28.
**After:** ripgrep → 0, `git grep` → 28 (proving nothing was deleted); `workplan_naming_audit.py`
exit 0.

---

## 4. Phase 2 — Dead references, zero dependents

**Prerequisite:** Phase 0. Archive to `_archived/<origin path>` exactly.

| # | Path | Lines | Stub |
|---|---|---|---|
| 2.1 | `references/claim-reference-join.json` + `.md` | 16,526 | no |
| 2.2 | `references/global-reference-registry.json` + `.md` | 10,224 | **yes** (`.md`) — patch one prose line in `governance/conceptual-model.md` |
| 2.3 | `references/specification-database.json` | 3,755 | no — zero hits anywhere |
| 2.4 | `references/bibliography-v11-draft.md` | 1,789 | no |
| 2.5 | `references/citation-mining-register.md` | 319 | **yes** — it still says "CHECK this register BEFORE mining" |
| 2.6 | `references/coverage-matrix.md` | 120 | no |

**The digest's `website/` row is struck — the path does not exist.**

**Budget: 8 files / 32,733 lines.** The four largest sizes verified exact.

**Prerequisite check that Phase 2 must run first:** 21 attestation `evidence_path` fields point into
`references/`. These were enumerated but never cross-referenced against this cull list. **Do that
before moving anything.**

**Acceptance, before:** per path, `git grep -l -F <basename> -- scripts skills governance tools .github
schemas`; `validate_cross_refs.py` exit 0. **After:** re-run both; RV count unchanged at 70.

---

## 5. Phase 3 — The rooms stratum (one commit, three files)

**Prerequisite:** Phase 0. **All three actions land together** — this resolves a cross-stratum
contradiction where one sweep archived the output and another held the generator.

| # | Action | Lines |
|---|---|---|
| 3.1 | `site/rooms/` → `_archived/site/rooms/` | 1,969 |
| 3.2 | `scripts/generate/room_page.py` → `_archived/scripts/generate/` | 282 |
| 3.3 | `schemas/room.py` → `_archived/schemas/` (zero live importers, unmirrored) | 112 |

**Verified:** `room_page.py r_ba` → `sqlite3.OperationalError: no such table: room` at `:26`. Live
tables are `rooms`/`room_items`; `room_item_population`, `specification`, `room_dar_provision`,
`room_conflict` are genuinely absent. Zero inbound `href`s. `build_site.py:6–11` states in its own
docstring that it does not drive `room_page.py`, so `site_pages_fresh` is unaffected
(`FRESH: 93`, exit 0).

**Correction to the digest:** archiving does **not** take retired vocabulary to zero. It goes
**70 → 68**. But `site/rooms/r_ba.html:118` carries the only remaining occurrences of RV-025 and
RV-026, the **only two `[doctrine]`-class entries still failing** — so *doctrine-class* goes to zero.
That transition is the acceptance criterion; the "to zero" phrasing invites the wrong reading.

**Budget: 19 files / 2,363 lines.**

---

## 6. Phase 4 — Unreachable executables

**Prerequisite:** Phase 0.

### 6.1 Why sweep A's "114 of 132 are keeps" was an artefact

The shared protocol's reachability test was `git grep -l <basename>`.
`audits/2026-08-12c-pipeline-probe-findings.json` is **23,975 lines and mentions 107 of 110 live
executables by name.** The test returns "referenced" for 97% of scripts regardless of whether anything
calls them. **A test that almost always says yes cannot distinguish keep from cull**, and 114/132 is
what it returns by construction.

A second-order trap worth recording: that file lives under `audits/`, which the root `.ignore` hides.
**ripgrep would not see it; `git grep` does.** The instruction to use `git grep` for absence claims is
correct for safety and is simultaneously what poisoned this particular test. **Future sweeps must
exclude `audits/`, `sessions/` and `attestations/` from a *reachability* grep while including them in
an *absence* grep.**

Replacing it with a real call-graph closure from 63 genuine entry points — active registry `cmd`s,
workflows, `.claude/settings.json`, `preflight.sh`, `regenerate_derived.sh`, closed over imports and
subprocess mentions — gives **87 reachable / 23 unreachable, 6,358 lines**. Sweep A proposed 601.
**It was roughly 10× too timid on its own stratum.**

The exotic-caller inventory, though, is complete: `scripts/audit/graph/*` via bare `sys.path` imports
and `research_batch_dod.py` via the settings.json Stop hook are the only unusual channels, and both
were found. **The method failed in the opposite direction from the one expected — it over-attributed
reachability, not under-attributed it.**

### 6.2 What to cull, and what to leave

> **BLOCKED — Fable 5 pass, A1 (HIGH).** `audit_consolidator.py` below is **not unreachable**:
> `skills/item-audit-pipeline_SKILL.md:252` invokes it directly and no skill edit is scheduled. Remove
> it from this set, or schedule the skill edit first. **Re-audit the rest of 4a for prose callers
> before executing** — the whole set was selected by a method blind to this channel.

**4a — cull (14 non-quarantined unreachable files, ~4,648 lines):** `audit_consolidator.py` ·
`generate_alias_chart.py` · `item_audit_pipeline.py` · `probes/citation_mining_pipeline.py` ·
`tests/probe_pipeline.py` · `tests/test_adjudication_integrity.py` · `verify_resolved_dois.py` ·
`bootstrap.sh` · `schemas/question.py` · `schemas/specification.py` · the six zero-importer unmirrored
schema modules. `migrate/migrate_decisions.py` + `_legacy_guard.py` gate on owner decision D2;
`tests/walk_harness.py` holds pending D4.

**4b — do NOT cull the nine quarantine-registered files.** They are unreachable, but
`references/tooling-register.md` §6.5 makes quarantine-with-reason terminal, and re-litigating nine
entries costs more owner attention than ~2,000 lines is worth. **Phase 0.5 already repairs their false
reasons, which is the actual defect.**

**Acceptance, before:** capture the call-graph closure → 87 reachable. **After:** re-run → **unchanged
at 87**; `run_checks.py --selftest` PASS; `python3 -c "import schemas"` clean.

---

## 7. Phase 5 — Workplan and working stratum (blocked on owner decision D1)

**Cannot be specified until D1 is answered.** The digest claimed "86 → 8" and never named the eight;
the source census says **one** plan is load-bearing. Count at HEAD is **87**, not 86.

**Method to re-derive the keep-set:** take `workplan/2026-08-17-consolidated-action-plan.md` §0's
supersession list, verify each named predecessor is covered, and treat anything uncovered as a keep.

**Three hard constraints, each in the same commit as its move:**

1. **Nine attestation-pinned files go to `_archived/workplan/<same filename>` and MUST NOT be stubbed.**
   `adherence_log_audit.py:337` already accepts the mirrored `_archived/` path. But `:322` runs
   heading-anchor resolution **only when the origin path still exists** — so a redirect stub satisfies
   `.exists()` and then fails the anchor lookup. **For this file class, a stub is strictly worse than a
   clean archive, and `CLAUDE.md` §9 guardrail 2 is wrong.** No current `evidence_path` carries an
   anchor, so this is latent — but the plan must say so.
2. **`scripts/db.py:274, 297, 552` requires a stub** at
   `workplan/search-coverage-completion-workplan.md` — a runtime print, so a stub file is right here.
3. **The `GRANDFATHERED` trim is cosmetic, not gating.** `workplan_naming_audit.py:150` fails only on
   `offenders`; stale entries merely print. Do not block on it.

**Budget: up to 123 files / ~53,000 lines, pending D1.**

---

## 8. Phase 6 — Prose weight (new; replaces the digest's registry-merge proposal)

The digest's headline registry action was "merge 28 entries into 9, zero predicates lost." **That is
refuted.** `level`, `kinds` and `session_pointer` are predicates; only 14 entries share a script across
5 groups, and **every group differs on at least one** — `adherence_log_audit.py` alone spans three
distinct levels. Merging the attestation four forces one level: promote and `main` goes red on an
advisory backlog; demote and two blocking gates are silently disarmed. **Maximum lossless consolidation
is about one entry.**

It also optimises the wrong dimension. `governance/check-registry.yaml` is 1,599 lines for 81 entries:
**50,775 characters of `note`/`reason`/`basis` prose against 8,880 of structure — 85.1% prose,
~634 lines.** Deleting 44 entries recovers the 15%.

**Do this instead:**

| # | Action |
|---|---|
| 6.1 | Truncate every `note:` to ≤2 lines — what the check asserts, and its level rationale. Move the archaeology verbatim to `_archived/governance/check-registry-notes-2026-08.md`. **~634 prose lines → ~130.** No `id`, `cmd`, `kinds`, `level`, `battery`, `min_items` or `no_floor` touched |
| 6.2 | Reduce `references/tooling-register.md` (627 ln) to a stub, after transcribing §6.7's required-check recommendation into the registry header |
| 6.3 | Strip `CLAUDE.md`'s self-correction narration into `decisions/`; keep the current statement only |

**Acceptance — the mechanical proof the digest asserted and could not offer:** hash the registry's
structural fields with `note`/`reason` excluded, before and after. **The digest must be byte-identical.**

**Budget: ~1,100 lines off the two most-loaded files in the repo, with no enforcement predicate changed.**

**The honest risk, stated because I am proposing this and no sweep did:** those notes exist because
this project was burned four times by vacuous passes. The structural-hash test protects predicates but
**not institutional memory.** Archiving the prose verbatim rather than deleting it is the mitigation,
and it is why 6.1 says *move*, not *delete*.

---

## 9. What NOT to do

1. **Do not merge registry entries.** "Zero predicates lost" is false (§8).
2. **Do not retire `validate_items`.** Two of its five predicates have no constraint, existing or
   proposed: V1 (`item_code` matching `^[A-K]-\d{2}[a-z]?$` — the column is a bare `TEXT PRIMARY KEY`)
   and V4 (`name` non-empty — `NOT NULL` permits `''`). And `scripts/validate_items.py:99–104` carries
   an explicit rebuttal of this exact method — *"A declared constraint is not an observed one"* — with
   a fault-injection record at `:41–52` showing a previous attempt was caught. **Doing it again would
   be the second commission of a recorded mistake.**
3. **Do not retire `source_slug_links_duplicates` before the `UNIQUE` migration is applied.** The gap
   between "proposed" and "in the DDL" is a window with no protection.
4. **Do not touch the dormant checks.** 34 of 65 cannot be falsified by any data. The digest culls two
   by name (`source_slug_links_duplicates`, `validate_evidence_state`) in **direct contradiction of the
   source census §4c, which lists both under "do not cull."**
5. **Do not redirect-stub attestation-pinned files** (§7 constraint 1).
6. **Do not present this as progress toward content generation** (§0.3).

---

## 10. Owner decisions

| # | Decision | Recommendation | Cost of the alternative |
|---|---|---|---|
| **D1** | Which workplans survive? Blocks Phase 5, the largest budget line | **The census's answer: 1 active plan + 9 attestation-pinned records stay live; 77 move.** The digest's "8" is unnamed and unverifiable | If `2026-08-17`'s supersession is incomplete, an obligation is lost — **fully mitigated by archiving rather than deleting** |
| **D2** | Decision-store triple: `decisions/*.md` + 5,558-line YAML + DB (163 rows) | **Retire the YAML.** `CLAUDE.md` §2 makes the DB canonical; `test_db_integrity` L01 is a check whose sole function is keeping a duplicate alive | 4 caller edits + a DR. Keeping it: two stores that can permanently disagree |
| **D3** | Promote `migration_reproducibility_deep` to blocking? | **Yes — but only in the commit after a DR widening the DR-2026-05-28 exemptions.** It passes today; it is the only check that can see a value-level edit | Promote without the DR and the next weekly `resolve-dois.yml` run red-Xs `main` on a divergence the project considers legitimate |
| **D4** | `probe_pipeline.py` (1,718 ln) + `walk_harness.py` (272 ln) | **Archive the first; hold the second** pending the writer plan. The census calls `walk_harness` live-cited; the call graph says unreachable — the one claim not mechanically settled | Archiving both: re-writing the harness if a probe pass is wanted |
| **D5** | Does `schemas/*.py` mirror SQLite or the YAML entity layer? | **Rule "SQLite", keep `MODEL_TABLE_MAP` at its 17 governed pairs (do not widen toward 57), archive the 8 zero-importer unmirrored modules (751 ln).** Then `validate_pydantic_schemas` can go blocking | Leaving it open: the only schema-drift detector stays advisory indefinitely |
| **D6** | Approve the `.ignore` edit (Phase 1)? | **Approve.** 7,480 lines, zero code impact, two-line reversal | — |
| **D7** | **Add the blocking `PRAGMA foreign_key_check` gate?** (§1.1) | **Yes.** Ten lines, and it is what makes any FK-based retirement safe. Currently nothing blocking observes referential integrity | Without it the floor has a hole, and Phase 4's FK-adjacent retirements must not proceed |
| **D8** | Branch-protection required-check set | **Now unblocked.** `CLAUDE.md` §7's warning — don't require the DB-integrity job until its backlog clears — **is obsolete: it is 72/72** | — |

---

## 11. Minimum viable infrastructure

The "as little code as possible" answer: **9 checks, 6 scripts, the populated frame plus the recovery
stash, 5 documents.** Everything else is dormant-with-a-trigger or discretionary.

**Checks (9):** `migration_reproducibility` · `migration_reproducibility_deep` (promote, D3) ·
`test_db_integrity` · `validate_pydantic_schemas --strict` · `db_path_env_audit` ·
`readonly_db_open_audit` · `attestation_presence` + `attestation_schema` ·
**a new `PRAGMA foreign_key_check` gate (D7)** · `run_checks.py --selftest`.

**Scripts (6):** `emit_data_migration.py` · `migrate_db.py` · `db.py` · `run_checks.py` ·
`adherence_log_audit.py` · `retired_vocabulary_audit.py`.

**Tables:** the populated frame (`items` 93, `populations` 23, `axes` 17 + 232 mapping rows, `slugs`
106, `terms`/`term_aliases` 2,382, `jurisdictional_values` 109, `decisions` 163, `data_migrations`),
**`source_locators` (835 — the reset recovery stash)**, and the empty synthesis core, which must
persist because recovery depends on it.

**Documents (5):** `mission-and-epistemics.md` · `tier-system.md` · `evidence-architecture.md` ·
`references/project-standards.md` · `check-registry.yaml` (structure only). Plus `decisions/` and
`attestations/` as append-only history.

**One thing to note about the floor:** `source_locators` holds 835 rows and has **no reader and no
writer in live code**. Keeping it is right — it is the recovery stash. Calling it *protected* is not;
nothing would detect its corruption.

---

## 12. Corrected budget

| Phase | Files | Lines | Confidence |
|---|---|---|---|
| 0 — correct the record | 0 | +~40 net | verified |
| 1 — `.ignore` | 28 | **7,480** (search surface) | exact |
| 2 — dead references | 8 | **32,733** | exact |
| 3 — rooms stratum | 19 | **2,363** | exact |
| 4a — unreachable executables | 20 | **~4,648** | measured |
| 5 — workplan/working | ≤123 | **≤53,000** | count exact, scope pending D1 |
| 6 — prose weight | 3 | **~1,100** | measured |
| **Total** | **~201** | **~101,300** | |

Live surface falls from ~430,000 to ~330,000 lines. The primary deliverable stays at **471 lines in 3
files**. The synthesis core stays at **0 rows**. `table_connectivity.py` still reports **0 of 80**.

---

## 13. Outstanding — what nobody has verified

- `full_db_metadata_verification` — not executed (network-bound, ~298s). The sixth quarantine reason is
  **unverified**.
- `resolve_dois.py` / `verify_urls.py` — not executed (network). D3's time-bomb is reasoned, not observed.
- **D1's keep-set** — the largest gap. Phase 5 cannot be specified without it.
- The ~21 dormant skills — classification accepted, not audited file by file.
- The 21 `references/` attestation-pinned paths — counted, not cross-referenced against Phase 2's list.
- The writer/reader table census — regex-based, not AST-based. Directionally right, numerically soft.
- **The recovery path from the pre-reset stash — unaddressed by every sweep and by this plan.**

---

## 14. Fable 5 adversarial pass — 2026-08-18

**Authority:** owner ruling, *"Fable 5 available; return suspended work for its use."* Discharges §4
items 1–3 of `workplan/2026-08-18-model-substitution-log.md` — ledger item 9, the whole substitution
debt. Read-only. Interrupted once by a transient API error and resumed from its own transcript.

### 14.1 Findings

| # | Severity | Verdict | Finding |
|---|---|---|---|
| **A1** | **HIGH** | **OVERTURNED** | §6.1's "exotic-caller inventory is complete" is false. `skills/item-audit-pipeline_SKILL.md:252` invokes `python3 scripts/audit_consolidator.py` as Step 8, "always runs last"; Phase 4a culls it with no skill edit scheduled. **A caller written in skill prose is invisible to a call-graph by construction** — so the defect is the method, not one missed file. |
| **A2** | MED-HIGH | **OVERTURNED** | §2 item 0.7's "the next commit touching that file turns a blocking gate red" is wrong on enforcement level. The five unregistered rule ids are real, but rule resolution runs under `attestation_evidence` (**advisory**); the blocking `attestation_schema` runs jsonschema only, and the file passes it cleanly. Fix still worth doing; the urgency was invented. |
| **A3** | MEDIUM | AMEND | §1.1's "ten-line FK gate replaces ~283 lines of `validate_items` + `validate_axes`" contradicts **this plan's own §9.2**. `validate_axes` is nearly fully replaceable; `validate_items` V1 (item_code regex — the column is bare `TEXT PRIMARY KEY`) and V4 (`name NOT NULL` permits `''`) are not. An executor following §1.1 verbatim commits the mistake §9.2 forbids. |
| **A4** | MEDIUM | **OVERTURNED as a universal** | §7 constraint 1's "no current evidence_path carries an anchor" — **38 anchored paths exist** across 86 attestations. None point into `workplan/`, so the narrow conclusion for the 9 pinned files survives. But "CLAUDE.md §9 guardrail 2 is wrong" overreaches: the guardrail is *inapplicable to this file class*, not wrong. |
| **A5** | MEDIUM | AMEND | §6.2's 4b counts are wrong (quarantine is 16 entries / 15 live scripts / 3,383 lines, not "nine files / ~2,000"), and §6.5's terminality ground **already dissolved** — `validate_db.py` was archived 2026-08-15 and its quarantine `cmd` now points into `_archived/`. ~3k lines is ~8–9% of the live executable surface: material against the owner's goal. |
| **A6** | MEDIUM | AMEND | §0.1's precedence rule ("census governs where it covers") is **silently overridden twice** — Phase 1 hides `workplan/deprecated/` in place where census 4a.3 says move it; 4b keeps `validate_commits`/`validate_audit_runs` where census 4a.10/4a.12 cull them. The executor faces contradictory instructions. |
| **A7** | MED-LOW | AMEND | The Phase 1 `.ignore` edit breaks that file's own header invariant — neither `workplan/deprecated/` nor `skills/deprecated/` is on `retired-vocabulary.yaml`'s `exempt_paths`. Needs a paired addition or an explicit invariant amendment. All Phase 1 budget figures verified exact. |
| **A8** | LOW | AMEND | §8's "50,775 chars, 85.1% prose" is not reproducible as stated — `note`+`reason`+`basis` = 44,666 chars (54.4%); 50,775 requires adding `no_floor`, which §8 does not say. Direction correct, figure wrong. |
| **A9** | LOW | — | §0.1's *corrected* DDL counts (80/123/7) re-ran as **80/128/9** — a fourth answer from a fourth agent. Corroborates this plan's own instruction never to cite these counts, and shows the correction was itself method-underspecified. |
| **A10** | LOW | AMEND | Phase-4 partition prose is sloppy: "14 non-quarantined unreachable files" enumerates 14–16 depending on reading, and ~4,648 lines requires including files the 4a/4b text holds separately. Headline roughly right. |

**Verified clean, no defect found:** the §1 FK mechanism end to end (FK OFF at `migrate_db.py:191/:325`, grandfathering set-difference, BOOTSTRAP hatch, 057's 5,072 INSERTs, schema path never FK-checked) · §0.2's re-run gates (`test_db_integrity` 72/72, deep repro PASS, `validate_population` 425/0, selftest 31-of-65 floor) · Phase 2 budgets (32,733) · Phase 3 (19 files / 2,363) · the pre-reset stash (313/273/863) · connectivity 0 of 80 · live surface ~432k lines.

**New work the plan listed as undone:** zero of the 21 `references/`-pinned attestation paths touch the six Phase-2 targets. That prerequisite is now discharged.

### 14.2 Discharge of the §4 debt

**Item 1 — the JUDGMENT verdicts. AMEND, with a compliance defect noted.** §3 of the substitution log
required the substitute to produce a **PART 3** marking every verdict MECHANICAL or JUDGMENT. **No
PART 3 exists anywhere in the repository** — grepping for the markings finds only the log that demands
them. The substitute did not produce the artifact its own terms required, and nobody noticed for two
days. Fable reconstructed the judgment-shaped verdicts from the plan and ruled on each: **upheld**
§0.2, §0.3, the §1 consequence, Phase 3, §9.2–9.4, D2, D3, D7; **overturned** 0.7's urgency, §6.1's
completeness, §7's universal-anchor claim; **amended** §0.1 precedence, §1.1 remedy scope, the Phase 1
invariant, 4b, §8's figures.

**Item 2 — applicability. AMEND, and this is the answer to the owner's actual question.** The cull is
*not* furniture-rearranging: `workplan/` and the search surface are exactly where sessions get hurt.
But measured against *"minimize code infrastructure"* —

- **only ~5,000 of the plan's ~101,300 lines are code** — about **14%** of the 35,444-line executable
  surface;
- **the plan retires zero active registered checks**;
- **no phase routes from the 65-check reality to §11's own 9-check / 6-script minimum.**

§0.3's "recovery plan before Phase 5" survives re-test as **the single highest-value item in the
plan**. The residual timidity did not go away when the too-timid finding was refuted — **it relocated
to the active stratum**, which is the one the owner's goal is about.

**Item 3 — the too-timid finding. UPHOLD both the refutation and the correction, independently.** The
poisoning is real: **108 of 112 live basenames appear in the 23,974-line audit file**, re-measured.
Fable then built its own reachability closure from registry `cmd`s, workflows, settings hooks and
preflight, excluding all frozen strata: **88 reachable / 24 unreachable of 112 (6,490 lines)** against
the substitute's 87/23/6,358. **Same answer by a method that does not share the defect.** Sweep A's
original 601-line proposal was ~10× under.

### 14.3 What the pass examined that the substitute did not

The **skills/ prose-caller channel** — which is where A1 came from; the actual enforcement level of
CHECK 3 versus the blocking schema gate, including validating the attestation against the JSON schema;
a full anchored-`evidence_path` scan (38 hits); the Phase-2 × attestation cross-reference the plan
itself listed as undone; `exempt_paths` against the proposed `.ignore` edit; and a from-scratch
reachability closure rather than inheriting 87/23.

---

## 15. The route from 65 to the minimum — appended 2026-08-19

**Why this section exists.** §11 declares a minimum viable infrastructure — 9 checks, 6 scripts,
5 documents — and §§2–8 contain no action that reaches it. The 2026-08-18 adversarial pass named
the gap (§14.1, objection 3) and did not close it. This section closes it, and is appended here
rather than filed as a new plan because `references/project-standards.md` RULE 2026-08-19 requires
extending existing work instead of restating it, and because `DR-2026-08-19` §2.2.1 would forbid
a new `workplan/` file.

**Method.** Five read-only audit passes on 2026-08-19. One **ran all 65 active checks live**; one
inventoried all 107 executables with caller analysis; one audited the non-code compliance regime;
one recovered this plan's own execution status; one checked the new findings against prior art.
Every check below was classified by a single test: **if this were deleted tomorrow, what wrong
thing could reach the guidebook?**

### 15.1 The classification that supplies the route

| Class | Active | Quarantine | Total | Share |
|---|---:|---:|---:|---:|
| PROTECTS-CONTENT | 7 | 2 | 9 | 11% |
| PROTECTS-DATA | 13 | 0 | 13 | 16% |
| CODE-ABOUT-CODE | 26 | 2 | 28 | 35% |
| CEREMONIAL | 3 | 0 | 3 | 4% |
| VACUOUS | 16 | 12 | 28 | 35% |

**59 of 81 (73%) protect nothing, or protect only the apparatus from itself.** 32 of 65 active
entries declare `basis: unattributed` — the registry's own field for "authority not established."

### 15.2 The route — 81 entries to ~35

- **DELETE (13).** `validate_temporal` (reads a directory that has never existed) · `validate_item`
  · `validate_conflicts` · `schema_reference_drift_audit` (coverage owned by `graph_audit`; its own
  registry entry proposed retirement on 2026-08-01) · `validate_commits` (registry concedes
  `check_commit_msg.py` "is the wired one") · `validate_audit_runs` (0 runs; its own wiring
  condition unmet for 17+ days) · `check_phase_a_complete` · `contamination_sampler` (writes files;
  a category error the entry admits) · `jurisdictional_divergence` (registry: "Belongs in a report,
  not a gate") · `table_connectivity` · `citation_mining_backlog_t3` · `workplan_naming` ·
  `full_db_metadata_verification` (298s of network against 0 rows).
- **DEMOTE or SUSPEND-EMPTY-SUBJECT (7).** The runner's own "BLOCKING and vacuous" five —
  `source_slug_links_duplicates`, `citation_mining_session`, `validate_evidence_state`,
  `validate_verification_consistency`, `check_rendered_docs` — plus `decision_capture` and
  `doctrine_recheck`. Auto-repromote when `EXAMINED > 0`. Better: give `run_checks.py` a
  first-class `SUSPENDED-EMPTY-SUBJECT` state, so a gate cannot report assurance it did not perform.
- **MERGE (5 merges, −7 entries).** attestation ×4→2 · `validate_schema`+`_cross_check`→1 ·
  `readonly_db_open_audit`+`db_path_env_audit`→1 (same AST walk, same `EXCLUDE_PARTS`) ·
  `migration_reproducibility`+`_deep`→1, **running deep as the blocking form** (this also
  discharges D3 and closes R-17b) · `citation_mining_backlog` t2+t3→1.
- **KEEP (~20).** The three syntax gates, `validate_bpc`, `validate_cross_refs`,
  `migration_reproducibility` (merged), `test_db_integrity`, `alias_provenance_audit`,
  `validate_schema` (merged), `validate_items`, `validate_population`, `validate_jurisdiction`,
  `validate_axes`, `graph_audit`, `audit_adversarial_use`, `evidentiary_audit_fresh`,
  `site_pages_fresh`, `research_dod_selftest`, and **`validate_reasoning`**.

**`validate_reasoning` is the finding this whole exercise turns on.** It is advisory. It is one of
only two checks currently red on real content. Run today it reports **15 errors on
`references/bpc-reasoning/room-acoustic-performance.md`** — the repository's single real
deliverable and the restart plan's first slug — missing every required section A through F, with a
status value (`PILOT`) outside its own permitted vocabulary. It exits 0.

**Five blocking gates examine nothing while the only real content fails silently.** That sentence
is the state of the apparatus, and no cull is needed to see it.

### 15.3 The executable route — 35,442 LOC to ~21,000

Measured: **9,898 LOC (28%) is code-about-code** and **10,595 LOC (30%) operates on empty tables**;
the sets are disjoint, so **58% of the executable surface polices the apparatus or polices nothing.**

- **Archive outright (~5,000 LOC, no caller and no subject):** `tests/probe_pipeline.py` (1,718) +
  `walk_harness.py` (272, closing D4) · `item_audit_pipeline.py` (496) · `verify_resolved_dois.py`
  (287) · `generate_search_queries.py` (309) · `probes/citation_mining_pipeline.py` (254) ·
  `check_phase_a_complete.py` (234) · `migrate/migrate_decisions.py` + `_legacy_guard.py` (214,
  after D2) · `generate_alias_chart.py` (95) · `validate_commits.py` (247) · `validate_item.py`
  (239) + `validate_conflict.py` (220).
- **Freeze until `evidence_sources > 0` (~7,500 LOC):** the research-protocol five behind
  `research_batch_dod`, the evidence-metadata trio behind `full_db_metadata_verification`, the two
  verification test suites, the evidence-cell demo layer. Keep `resolve_dois`/`verify_urls` as the
  restart kit; disable their cron workflows meanwhile.
- **Merge (~2,000 LOC):** the two AST hygiene auditors → one; three HTML dashboards → one; the four
  selftest wrappers → `run_checks --selftest`.
- **Two corrections to Phase 4a, which remains BLOCKED as written.** `audit_consolidator.py` is
  invoked by `skills/item-audit-pipeline_SKILL.md:252` — prose callers are invisible to a call
  graph by construction, so the defect is the method. And **`generate_parts.py` (463 LOC) is an
  orphan by call graph that assembles the actual deliverable** — it must be registered, never culled.
  Note also that the only referencing file for the two largest dead scripts is
  `governance/context-map.yaml`: the sole caller of the dead code is the generated map of the code.

### 15.4 The compliance route

- **Abolish.** The doctrine token and its apparatus (`check_doctrine_token.py`, the commit-msg
  doctrine step, `doctrine-deltas.json`, adherence checks 2 and 7, the dead `RE_ATTESTATION_WINDOW`):
  push-only, merge-exempt, PR-skipped, so it binds only the path the workflow forbids; every
  recorded firing was a false positive. A 7-hex checksum evidences copy-paste, not comprehension.
  Also abolish the dual decision store (drift is zero *today*, so retirement is free), the frozen
  working-session counter and the "any doctrinal-rule revision" recheck trigger, the
  `next_action`-pivot→D-OP rule, and the 13 never-invoked skills.
- **Suspend until content exists.** The attestation requirement on `decisions/` and `sessions/`.
  **84 of 87 attestations attest to governance artifacts; exactly 1 covers real content.** Keep the
  counterclaim only for `references/bpc-reasoning/` and `references/connection-reasoning/`, the one
  place it could earn its cost. Gate the Stop hook's FAIL print on `EXAMINED > 0`.
- **Keep.** R1–R15 and `research_batch_dod.py` — all 15 rules have real enforcers, hardened twice
  after being caught passing on substring matches. Migrations-only writes and the reproducibility
  rebuild. The DG-NON list and DR files as single-store read-once records.

### 15.5 Reconciliation with this plan as it stood

**Confirms:** Phase 2, Phase 3, Phase 6.2, D2, D5, and the census rows on `validate_commits`,
`validate_audit_runs`, `schema_reference_drift_audit`, `probe_pipeline.py` — all independently
re-derived from live state.

**Resolves three of the recorded contradictions.** (7→) `workplan/deprecated/` — **move**, per
census 4a.3: hiding in place breaks the `.ignore` invariant and leaves the files citable.
(2→) `validate_commits` / `validate_audit_runs` — **cull**, per census: quarantine is not terminal,
as the `validate_db.py` archiving of 2026-08-15 already established. (8→) §1.1 vs §9.2 — **keep
`validate_items`, add the FK gate anyway**; the gate covers referential integrity, V1/V4 cover
constraints the DDL does not express. They are not substitutes.

**Adds what no prior pass covered:** the compliance regime (§15.4) and the 87 attestations, which
every earlier cull document listed as must-not-cut without measuring what they attest to.

**Concedes what §0.3 already said, and it still governs:** *"This program removes roughly 101,000
lines of attention cost. It adds zero rows to `evidence_sources`."* Nothing in §15 changes that.
The route exists so that the apparatus stops growing, not because shrinking it produces research.

### 15.6 Sequence

1. **Phase 0 of this plan** — 8 record corrections, no owner gate, ~40 lines. Planned twice
   (2026-08-16 Wave 0, 2026-08-17 Wave 0) and skipped twice; still undone. Add `check-registry.yaml:174`,
   whose unquoted flow-mapping commas have been producing junk keys since R-12 was filed on 2026-08-11.
2. **The first research batch** — unchanged, per the restart plan and `DR-2026-08-19` §3. It is not
   downstream of any of this.
3. **§15.2 and §15.3**, which need only that the batch has established which checks have subjects.
4. **§15.4**, owner-gated throughout.
5. **Phase 5**, still blocked on D1 and still sequenced behind the batch.

**Nothing in §15 is a prerequisite for research.** If only one item on this page is ever executed,
it should be item 2.
