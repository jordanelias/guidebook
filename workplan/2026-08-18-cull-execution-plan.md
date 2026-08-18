# 2026-08-18 — Cull execution plan

**Status:** PROPOSAL. Nothing here is executed. Every phase is owner-gated; §7 lists what only the
owner may decide.

**Provenance.** Six exhaustive read-only sweeps (Fable 5) over all 2,133 tracked files, merged by
Opus 5 into a 20-claim digest, then adversarially critiqued by a cold Opus 5 agent that had not
authored the digest. Model-substitution debt is recorded in
`workplan/2026-08-18-model-substitution-log.md` — the critique was Fable's task and **Fable is owed a
re-examination of every `JUDGMENT`-marked verdict.**

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
