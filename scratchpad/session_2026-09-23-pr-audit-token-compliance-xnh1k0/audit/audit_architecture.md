# Data-architecture compliance audit — PRs #116–#157 (2026-08-23 → 2026-09-20)

**VERDICT: MOSTLY COMPLIANT ON THE MECHANICS, NOT ON THE DESIGN.** The write path held: every PR that changed the DB blob shipped a migration, and no committed migration was edited. The schema, however, was built and then rebuilt in the same weeks. About a quarter of the period's schema migrations correct an earlier migration from the same period. Five migrations built `icf_code` against the coined `axes` table after the owner had ruled it out. Two new copies of facts from earlier stages were created and are still live. Outside the PRs, a scheduled bot commit rewrote evidence rows that no migration reproduces.

Scope: the merge commits from `git log origin/main --merges --first-parent --since=2026-08-23`. #117 is the root commit (`git log -1 --format=%P d6ef7e9` prints nothing), so it has no diff and is excluded. Every number below is followed by the command that produced it; re-run the command rather than trusting the number. Base ref is `ce33ef6^1` (the parent of #116); end ref is `1d49a62` (#157).

Owner instruction received mid-audit: run no check suites. Before it arrived I had run two things, both read-only against the repo: `scripts/audit/validate_pydantic_schemas.py` (one advisory script), and `migrate_db.py --rebuild` into the scratchpad. Neither wrote to a repo file. Nothing was run after the instruction.

---

## Findings, worst first

### F1 — MAJOR — no PR (bot commit `c4c8463`, 2026-09-21) — Rule 3: the live DB cannot be reproduced from migrations
- The scheduled `source-verification` commit did more than add a `pipeline_runs` row. It rewrote `evidence_sources` REF-01006: 9 bibliographic fields changed, including `author_count_is_complete` 0→1, `issn`, `journal_abbrev` and `pub_month`. It also deleted and re-inserted the 6 `evidence_source_authors` rows for that source.
  - Commands: `S=<scratch> python3 scratchpad/dbdiff.py c4c8463^ c4c8463`, plus the per-column diff (method: `set(select *)` compared parent vs commit).
- A fresh rebuild disagrees with the live DB on exactly those rows: `evidence_sources live-only 1`, `evidence_source_authors live-only 6`.
  - Command: `migrate_db.py --rebuild $S/rebuilt.db`, then a row-set diff against `data/guidebook.db`.
- The blocking `migration_reproducibility` gate compares row counts only, so it cannot see this; the row counts did not change.
- This is a known leak that was never fixed. `governance/check-registry.yaml:353-360` (the note on `migration_reproducibility_deep`) already records that "resolve_dois.py writes Crossref enrichment straight into" `evidence_sources`. CLAUDE.md rule 3 describes the bot as exempt through `pipeline_runs` only, and this commit shows that description is wrong.
- The rewrite also changed `author_count_is_complete`. That is the field §5(c) exists to protect, and this change carries no retrieval-log artefact.
- Merit of the check: `migration_reproducibility_deep` would catch this, but it is advisory and already red, so it is ignored. The blocking count-only gate cannot detect UPDATE-shaped drift at all.

### F2 — MAJOR — PRs #125, #131, #134, #136 — Owner ruling 2026-08-18 ("axes" is a bad coined term): `icf_code` built on bare axis codes five times, then reversed
- `icf_code … REFERENCES axes(axis_code)` appears in migrations 065:111, 071:103, 073:316, 074:73 and 076:121.
  - Command: `grep -n 'REFERENCES axes' scripts/migrations/0{65..79}_*.sql`.
- As a result, a column named `icf_code` resolved to an `AX-` code on four tables until 081 (#136, 2026-09-13) re-pointed all four at `base_icf`. 081's header states this: "Four columns literally named `icf_code` … carried a real FK into `axes(axis_code)`".
- The reversal cost a rebuild of 6 tables. On a from-scratch rebuild it also produces `WARNING (advisory): 158 FK violations after 081_icf_registry.sql`. That happens because migrations 065–084 carry no `AFTER_DATA` marker, so the rebuild order differs from the order the live DB was actually built in.
  - Commands: `grep -l AFTER_DATA scripts/migrations/0[6-9]*.sql`; the rebuild output.

### F3 — MAJOR — PR #136 (migration 080) — Rule 5: two new tables copy facts from earlier stages
- `specifications.functional_basis` is a JSON copy of `population_icf_links` rows: icf_code, mechanism, mapping_confidence and provenance, word for word. That is a base-stage crosswalk copied into the specification stage instead of pointed to by `link_id`.
  - Command: `select functional_basis from specifications where specification_id=8`.
- `determination_gates.trigger_tier` and `trigger_evidence_type` (080:143-144, both NOT NULL) sit beside `trigger_ref_id REFERENCES evidence_sources`. They are copies of evidence-stage facts, and the tier is also derivable by `derive_tier()`, so they break rule 8 as well.
  - The doctrine behind the columns (DR-2026-07-13, "gate rows carry the tier") explains the need but does not license a copy. The FK is already there to point with.

### F4 — MAJOR — PRs #125, #126, #136 — Owner ruling 2026-08-26 (the determination is keyed on the parameter; no new writer keys anything on `item_code`): a new table keyed on `item_code`
- 065 (#125, 2026-09-01) created `item_taxonomy_links(item_code, …, applicability, strength_band, mechanism_note)`. Those are judgment-shaped facts, keyed on the render aggregate.
- The hand-written data migration `data_20260901183203` inserted 10 rows keyed on `item_code`.
- The next PR (#126) emptied `items`. That left the new table UNWRITABLE: it held 540 rows at #125 and 0 at #126.
  - Command: row counts at `708948a` vs `1a6e24d`.
- 081 (#136) then rebuilt the table while keeping `item_code`. That preserves a dead table instead of deleting it, against §8.
- The table is still UNWRITABLE today (§4 derivation snippet: `UNWRITABLE item_taxonomy_links.item_code -> empty table`).

### F5 — MAJOR — PRs #131, #134, #136, #137 — Rule 4: the 063→064 failure repeated; renames and drops shipped with incomplete caller sweeps
- 071 dropped `specifications.item_code` and `population_code` and broke 3 views, including `v_item_provenance`, the same view 063 missed. 072 (same PR #131) repaired them.
  - 072's header records that `run_checks.py --all` was "PASS, 50 green, 0 blocking, over three broken objects".
- 073's own header says it is "owed sweep" of 071 ("WHAT 071 LEFT HALF-DONE").
- 085 (#142) renamed or dropped 23 columns. It left `schemas/bpc_metadata.py:78` with `@field_validator("last_updated")` on a field that is now `updated_at`, and **the module no longer imports**: `python3 -c "import schemas.bpc_metadata"` raises PydanticUserError.
  - Commit `1dbd092` edited line 32 and missed line 78.
  - `scripts/db.py:90` `_BPC_META_COLS` still whitelists the dropped `last_updated`.
- Prose callers were not swept. `governance/check-registry.yaml:802` still says EXAMINED sums `item_axis_links … (232 today)`, but 065 dropped that table (rule 7a, third shape).
- Merit of the checks: `schema_reference_audit` resolves names only; it did not catch 071. No registered check SELECTs from every view. The only probe that does, `scripts/audit/rename_insurance.py:74`, is unregistered (`grep rename_insurance governance/check-registry.yaml` returns nothing). So a 071-class break would still pass today.

### F6 — MAJOR — PR #136 (`data_20260913040739`) — Rule 3 and §4: a bulk hand-written DELETE across 17 tables freed identifiers, forcing compensations
- The owner-ruled "clear circulation corpus" deleted rows from 17 tables, including `base_parameters` and `specifications`.
  - Command: `grep -oiE '^\s*DELETE FROM\s+"?[a-z_]+' <file> | sort -u`.
- It lowered the `ref_id` high-water mark from REF-00982 to REF-00970 and reset rowid identifiers. That required migration 076 (AUTOINCREMENT on both keys, rebuilding `base_parameters` and `specifications` again) and `data_20260913050221` (tombstone rows in `source_locators`).
- It also emptied `base_parameters` a second time, so `specifications` went back into the §4 "NOT NULL FK into an emptied table" state.
  - Command: counts at `0bad045` show `base_parameters 0` and `specifications 0`.
- The same shape happened on 2026-09-01 (#126): that retraction needed 5 compensating data migrations in the same PR.
  - Files: `data_20260902181820` (ref high-water), `…191029` (restore leads), `…193408`, `…193546`, `…194228` ("owed repairs").
  - `…193546` records that the H05 parity check had *caused* `results_admitted` to be zeroed. That is a parity check doing active harm, which is rule 5's warning in practice.

### F7 — MAJOR — PRs #134–#157 — §6: determinations are built on a population umbrella; judgment never crosses terms
- All live determinations and extractions use only the identity lens `MOB`: `specifications [('MOB', 8)]`, `source_value_extractions [('MOB', 48)]`. The ICF lens is 0 of 8 on specifications, and 0 of 48 on extractions (needs 1).
  - Command: `select identity_code,count(*) … group by 1` and the `sum(icf_code is not null)` query.
- `term_adjudications` holds 0 rows against 57 `observed_terms`. §6 says "Zero links after judgment is a defect."
- **No live determination exists.** All 8 `specifications` rows carry `retired_at`. Spec 8 was retired with no successor, because "the engine cannot yet recompute the cell".
  - Command: `select specification_id,retired_at,superseded_by_specification_id from specifications`.

### F8 — MINOR — PRs #119–#136 — §4: hand-written SQL in data migrations
- 18 of the period's 82 data migrations were not captured from CLI activity.
  - Command: loop over `git diff --name-only --diff-filter=A ce33ef6^1 1d49a62 -- 'scripts/migrations/data_*'` and count files lacking `captured by scripts/research/emit_batch_sql.py`.
- Most target tables `db.py` could not reach at the time: `decisions` (5 files, and there is still no CLI verb, so this coverage gap was never fixed), `item_taxonomy_links`, `population_icf_links`, and `search_executions` / `search_candidates` updates made before `amend-search` / `resolve-candidate` existed (both first appear in `cdfc415`, 2026-09-16).
  - Command: `git log -S'"<verb>"' -- scripts/db.py`.
- **Clear bypass:** `data_20260913060013` and `…060346` hand-`INSERT INTO gaps`, although `add-gap` existed at the period start (`git show ce33ef6^1:scripts/db.py | grep add-gap`).
- The batch 13 and 14 "part 1 of 2" `UPDATE specifications` files are CLI-originated, not hand-written: `retire-specification` appears in `scratchpad/batch-14-co2-professional-bodies/commands.jsonl`. They are captures that were split by hand.

### F9 — MINOR — PRs #136, #137, #142, #144, #155 — §4 "mirror the Pydantic model": schema↔model drift introduced in the period
- Of the 14 tables created in the period, 2 are mapped to a model: `base_parameters` (DRIFT: `accessibility_direction` and `direction_rationale` from 078 are missing) and `extraction_relations` (OK).
  - Command: the `validate_pydantic_schemas.py` output, run before the owner instruction.
- `EvidenceStateRecord` lacks every column added to `specifications` in 079, 080, 083, 086 and 087.
- `BPCMetadata` is broken (F5).
- The validator itself is advisory, prints "213 drift findings (informational)", and uses the curated `MODEL_TABLE_MAP`, which CLAUDE.md rule 8 already lists as a violation. As a gate it is vacuous.
- `user_version` is consistent: every migration from 065 to 095 sets `user_version` to its own number (loop check), and the live value is 95.

### F10 — MINOR — PRs #125, #134 — §8 / §4: tables added with no possible writer
- 074 created `icf_medical_map` and `identity_medical_map`, each with an FK into `base_taxonomy_medical`. That table has held 0 rows at every merge sampled (`708948a`, `1a6e24d`, `0bad045`, `be25c89`, `1d49a62`).
- Both tables were UNWRITABLE at birth. 074's header acknowledges the content half is blocked on the owner.
- The §4 derivation today lists 19 UNWRITABLE FK columns across 18 tables.
  - Command: CLAUDE.md §4 snippet.

### F11 — MINOR — PR #144 (087), PR #153 (088) — rule 5, borderline
- `specifications.value_notations` holds source-"stated" notations as JSON beside `specification_extraction_links`. It is defensible as a derived rendering, but it is a second place where a stated value now lives.
- 088 adds `search_candidates.resolved_ref_id` beside `search_admissions`, and integrity check S01 (`scripts/tests/test_db_integrity.py:293`) asserts that the two agree. That is a parity check. It does compare two *different* edges (candidate→ref and exec→ref), and 088's header cites a real mismatch on batch 17 (candidates 107 and 108), so it has caught a defect. Keep it, but it is a cross-check, not a single home.

### Rule-5 remedies done correctly in the period (for balance)
- **069** moved `prior_expectation` to the research stage, with writer-retire and then reader-retire.
- **093 (#156)** replaced five JSON ref-arrays with the `convergence_sources` junction. The writer (`assess_cell.py:1960-1990`) and the reader (`validate_evidence_state.py:329-381`) were both retired, and no parity check was added.
- **#157** retired `specifications.governing_refs` and deleted the H01/H02/H06/H07 parity checks (`scripts/tests/test_db_integrity.py:1050-1110`). The dual home that 077 (#136) had opened was therefore held up by a parity check for about eight days.
- **073** asked the stage question before dropping `v_item_extractions` (render + judgment + evidence) and justified it (073:170-196).

### Rule 8 (argparse `choices=`)
The net trend in `scripts/db.py` is good:
- At the period start: 34 `choices=`, 0 derived from the schema.
- Now: 51 `choices=`, 25 derived from the schema.
- Command: `git show ce33ef6^1:scripts/db.py | grep -c 'choices='`, the same with `choices=dbcore\.\(schema_choices\|check_values\)`, and both again on HEAD.
- New literals added in the period: `next-id` extended its string list with `"ref"`, and `_AMENDABLE_SVE_FIELDS` is a curated set.
  - Command: `git diff ce33ef6^1 1d49a62 -- scripts/db.py | grep '^+.*choices=' | grep -v dbcore`.
- CLAUDE.md rule 8 states that 24 were derived on 2026-09-20; the command above gives 25 today. The count had already gone stale.

---

## Churn (item 7)
- **Schema migrations in the period: 31 (065–095).** Command: `git diff --name-only --diff-filter=A ce33ef6^1 1d49a62 -- 'scripts/migrations/0*' | wc -l`.
- **Corrections of an earlier migration from the same period: 7, i.e. 23%.** Each one's own header says it repairs, completes or reverses in-period work:
  - 072 repairs 071
  - 073 is the owed sweep of 071
  - 076 fixes identifier reuse from 071 and the clear
  - 081 fixes the axes FKs from 065/071/073/074/076
  - 090 fixes the view blind spot from 073/076
  - 091 does the "siblings 089 left behind"
  - 095 drops 094, one day after it was added
  - Counting 092 (091's sibling table) and 084 (the planned sweep for 083) as well gives 9/31.
- `specifications` has had DDL applied by 8 of those 31 migrations, including 3 full rebuilds (071, 076, 081). Command: `grep -lE '(ALTER|CREATE|DROP) TABLE\s+"?(_081_new_)?specifications' scripts/migrations/0{65..95}_*.sql`.
- `evidence_sources` was rebuilt twice in one PR (089 and 091, #155). `source_locators` was rebuilt twice (082 in #137, 092 in #156).
- **Data migrations: 82.** 22 of them have summaries naming a fix, correction, retraction or restoration.
  - Command: summary-keyword grep `fix|correct|compensat|restor|repair|revers|retract|undo|wrong|mistake|misattribut|misrepresent|misclassif`.
  - This is a keyword proxy [UNVERIFIED as an exact count of compensations].
- Immutability held: no existing migration file was modified or deleted in any PR. Command: per-merge `git diff --name-status … -- scripts/migrations/ | grep -v '^A'` returns nothing.

---

## Per-PR compliance (one line each)
| PR | Arch. compliance |
|---|---|
| #116 | OK. Tooling only; no DB change. |
| #119 | OK. Retires cross-stage copies by NULL-forward; the data migration is hand-SQL on reachable tables (`citation_mining`, `evidence_sources` UPDATE) (F8). |
| #118, #120, #121, #122 | OK. Records and rulings only; no DB change. |
| #123 | OK-ish. Hand `INSERT INTO decisions`; there is no CLI verb (F8). |
| #124 | OK-ish. The same `decisions` hand-SQL. |
| #125 | **Non-compliant.** 065 keys a new judgment-shaped table on `item_code` and puts its FK into `axes` (F2, F4); 10 hand-inserted rows. |
| #126 | **Mixed.** A bulk hand DELETE retraction, then 5 compensating migrations in the same PR (F6). 067 is a sound identity fix. |
| #127 | OK. Captured batch. |
| #128 | OK. 069 is a textbook rule-5 fix; 068 and 070 are clean. |
| #129, #130, #132, #133, #135 | OK. No DB change (#130 and #133 touch `db.py`/`dbcore.py` only). |
| #131 | **Non-compliant, then repaired in the same PR.** 071 broke 3 views; 072 repaired them; 073 is the owed sweep; 071 built its FK into `axes` (F2, F5). |
| #134 | Mixed. 074 creates tables that cannot be written (F10) and has the `axes` FK (F2). |
| #136 | **Non-compliant.** 080 copies facts into `functional_basis` and `determination_gates` (F3); the corpus clear freed identifiers, forcing 076 (F6); hand `INSERT INTO gaps` although the CLI verb existed (F8). 081 correctly reverses F2. 075 and 077 are sound. |
| #137 | OK. Retire-in-place (083) with a planned view sweep (084); 082 is clean. |
| #138, #139, #141 | OK. No DB change. |
| #140, #143, #145, #146, #147, #152, #154 | OK. Captured batches plus in-PR corrective data migrations. |
| #142 | **Non-compliant.** The 085 rename sweep missed `schemas/bpc_metadata.py:78` (the module no longer imports) and `db.py:90` (F5). |
| #144 | Mostly OK. The 087 JSON notation store is borderline (F11); 086 is clean. |
| #148, #149, #150, #151 | OK. No DB change. |
| #153 | OK. 088 adds a real edge (a parity check, but one with merit). A scratch DB was committed on the branch and removed before merge (`c794b83`). |
| #155 | Mixed. 089 → 091 → (#156) 092 is incremental rework; 090 closes a real blind spot. |
| #156 | Mixed. 093 is an exemplary rule-5 fix. 094 added a table with no reader, inside a PR titled as a visualisation. |
| #157 | OK. Reverses 094; retires `governing_refs` and its parity checks correctly. |

---

## Systemic causes
- **The schema is designed by migration.** A column or FK lands before its sweep and its readers are designed. The repair follows as the next migration (071→072→073→076→081), which yields a 23% correction rate and three rebuilds of the table this project most needs to hold still.
- **Retraction by bulk DELETE.** Both owner-ruled clears (2026-09-01 and 2026-09-13) were hand DELETEs with no identity-floor guard, and each generated a cascade of compensations. The retire-in-place pattern (083) arrived afterwards and covers `specifications` only.
- **The gates are blind to the failure shapes that actually occurred:** count-only reproducibility (F1), name-only reference audit (F5), no execution probe over views, and an advisory drift validator driven by a curated map (F9). Green is not evidence.
- **Some writers sit outside the sanctioned path:** `resolve_dois` and the source-verification bot write evidence rows directly (F1), and `decisions` still has no CLI verb, so every ruling is recorded in hand SQL.
- **Rulings bind prose faster than DDL.** The `axes` ruling (08-18) and the `item_code` ruling (08-26) were each contradicted by DDL written after them (065, 071, 073, 074, 076), and only an adversarial pass or a later session caught it.
- **Framing drifted back to population umbrellas.** Every determination is `MOB`-only, and term adjudication is at zero. The §6 ICF-first posture is not reaching the data.
