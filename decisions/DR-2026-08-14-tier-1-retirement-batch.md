# DR-2026-08-14 — The Tier-1 retirement batch

**Status:** OPERATIVE — 2026-08-14 (executed 2026-08-15).
**Decision by:** Owner approval 2026-08-14 — "APPROVE WHOLE TIER-1 BATCH".
**Category:** D-OP, with a D-SCHEMA component (migration 059 drops two tables and a view).
**Delegation:** DG-NON — file moves and retirements are owner-gated (`CLAUDE.md` §9 guardrail 4).
**Scoped by:** `workplan/2026-08-14-remediation-workplan.md` §6, itself a correction of the
2026-08-14 synthesis's over-aggressive cull list.

---

## 1. What was retired

**Files — 28 Python modules and 4 probe-log artefacts,** archived to `_archived/` at their origin
paths: `scripts/convert/**` (13 files, 2,669 lines), `scripts/db/**` (3), eight of ten
`scripts/migrate/**`, `init_db.py`, `validate_db.py`, `migrate_evidence_sources_v2.py`,
`scripts/tests/test_generate_parts_4_2.py`, and the two superseded same-day probe-log pairs.

**Database — migration 059:** `db_meta` (2 rows), `population_reclass` (29 rows),
`v_source_reach` (view).

**CLI:** `db.py init` and `db.py validate`, the two subcommands that invoked archived scripts.

## 2. What was deliberately kept, and why each would have been a mistake to take

- **`scripts/migrate/migrate_decisions.py` and `_legacy_guard.py`.** The decision-register YAML is
  a live dual store pending owner decision #2. Archiving its importer would have quietly prejudged
  a decision explicitly held open.
- **`audits/2026-08-12c-*`.** The newest of three same-day probe runs, and cited **by line number**
  by a plan that has not been executed: `workplan/2026-08-13-writer-plan.md:189` quotes
  `audits/2026-08-12c-pipeline-probe-log.md:12147`. Archiving it breaks a pinpoint citation.
- **The `validate_db` registry entry**, kept at `status: retired` rather than deleted. It carries the
  script's one unresolved substantive finding — C4, **31 connections with zero targets**. That is a
  *content* defect. Deleting the entry would have buried a real finding inside a tooling cleanup,
  which is the failure mode this batch exists to reduce.

## 3. The definition of "unreachable" this batch used

A cull driven by "nothing in CI runs it" would have deleted `emit_data_migration.py` — the only
sanctioned way to write the canonical database — along with `db.py`, `generate_parts.py` and the
dynamically-imported `schemas/*.py`. That is not a hypothetical: the 2026-08-14 synthesis produced
exactly that list, and its own retirement pass had to rescue five load-bearing items, two of them
read by *blocking* gates.

Reachability was therefore tested six ways: registry or CI selection, **gate-readership**, contract
or doctrine citation, operator CLI paths, transitive imports, and scheduled jobs.

Every sweep used `git grep`, never ripgrep. The root `.ignore` hides seven directories; a sweep run
through it makes an unsafe deletion look safe.

## 4. False positives the sweep produced, recorded so the next sweep does not re-derive them

- **`validate_db` in `scripts/validate_evidence_state.py` and its test is a FUNCTION name**, not the
  script. Three of the six live hits were this.
- **`EXCLUDE_PARTS` / `EXCLUDE_DIRS` in the two path audits exclude by path *part*.** Their `"db"`
  and `"migrate"` entries stay: they cost nothing and still catch a directory of that name
  reappearing. `db_path_env_audit.py`'s docstring asserted `scripts/db/**` exists and was corrected
  rather than left true-sounding.
- **`population_reclass` in `validate_population.py` was an `EXCLUDED_TABLES` entry** — an exclusion,
  not a read. Removed with the table, since excluding a table that no longer exists is dead
  reasoning that reads as live.

## 5. What was checked before dropping, rather than assumed

- **`v_source_reach_all` does not reference `v_source_reach`.** Both matched a naive dependency scan
  because one name contains the other. They are independent SELECTs over base tables — which is also
  why the survivor is the honest one: the dropped view INNER JOINs, so a source reaching nothing
  vanishes from the result and the view cannot distinguish "no such source" from "reaches nothing".
- **The `population_reclass` crosswalk is not lost.** Its 29 old-code → canonical-code rows survive
  in the 057 baseline's INSERT statements (immutable, replayed on every rebuild), in
  `governance/retired-vocabulary.yaml`'s deferred entry which spells the mapping out, and in
  DR-2026-07-22, which cites the column by name.
- **Nothing reads `db_meta`** — verified across `scripts/`, `schemas/`, `tools/`, `governance/` and
  `.github/`. Its two surviving rows were a creation stamp and the repo name.

## 6. Verification

Scratch rebuild reaches `user_version` 59 with all three objects absent and `v_source_reach_all`
surviving; 18 views execute; no FK violations; `integrity_check` ok. `test_db_integrity` 72/72.
`validate_population` PASS over 425 values across 14 columns. `--deep` reproducibility PASS. Every
`cmd` in the check registry still resolves to a file that exists. `db.py init` and `db.py validate`
verified absent from `--help` by invoking them.

`run_checks.py --all`: 46 green, 13 nothing-in-scope, 6 advisory failures, 0 blocking — the same six
advisory failures as a clean `origin/main` baseline. Green rose by three and vacuous fell by three
for a reason worth naming rather than claiming as improvement: `attestation_presence`, `_schema` and
`_verdict` are changeset-scoped, and the preceding commit gave them a real attestation to examine.
**They were not fixed; they were fed.**

## 7. Reversal

Forward-only, like every migration here. Re-adding any of the three database objects when a reader
appears is a small migration. Restoring a file is a `git mv` back — and the archive README says
plainly that this must not be done merely to satisfy a stale reference in a dated workplan, audit or
session record, because those are frozen and correct for their date.
