# Session — Ecosystem tooling: assessment, consolidation, work-kind gating

**Date:** 2026-08-01
**Branch:** `claude/ecosystem-tools-consolidate-gate-dvv6qi`
**PR:** #74 (merged, `839be60`)
**Doctrine SHA:** `0f2f525`
**Kind:** tooling / governance. **No content, no synthesis, no DB writes.**

## Task

"Assess all ecosystem tools, validators, CI etc and consolidate wherever possible as well as
gate their running based upon kind of work being performed." Later in the session: an
adversarial review of each deferred proposal, then execute, commit and merge.

## Method

Every one of the 158 executable files under `scripts/` and `tools/` was **run once** against a
clean checkout of `main` with `pydantic`, `PyYAML` and `jsonschema` installed, and its exit code
and wall-clock time recorded. Nothing in the assessment is inferred from reading source. This
mattered more than expected: several scripts that read like working gates turn out to crash, and
several that looked abandoned are green and cheap. Re-derive the whole baseline with
`python3 scripts/run_checks.py --all`.

## What was found

**F1 — CI's pull-request path filters had never evaluated true.** Three `ci.yml` jobs were gated
on `contains(github.event.pull_request.changed_files, 'data/')`. `changed_files` on the PR
payload is an **integer** — the count of changed files — so `contains(12, 'data/')` is always
false. The `schema`, `db_integrity` and `governance` jobs therefore **never ran on any pull
request in the repository's history**; they ran only on push to `main`, i.e. after merge.
CLAUDE.md §7 already recorded the symptom ("in practice runs only syntax + structure"); the
cause was undiagnosed.

**F2 — Four hand-kept check lists had drifted.** `ci.yml`, `audit.yml`, `research-contract.yml`
and `preflight.sh` each transcribed their own. `validate_axes` and
`validate_verification_consistency` existed **only** in the local script, so CI had never once
run them. `validate_jurisdiction` and `validate_temporal` existed only in CI. The
migration-reproducibility invariant — the gate that actually enforces "never write the DB
directly" — existed as **two separately-maintained inline heredocs**.

**F3 — 109 of 158 scripts were referenced by nothing.** Mostly benign (one-shot converters,
migration probes), but it made an unwired *enforcer* indistinguishable from an unwired
*converter* — the shape of the 2026-07-24 "28 enforcers wired to nothing" finding.

**F4 — `main` is not branch-protected.** Verified against the API: `protected: false`, no
required status checks. **Every "BLOCKING" label in the workflows is nominal** — a failing gate
paints a red X and stops nothing. CLAUDE.md §1 called `main` "protected by CI", which was
aspirational rather than descriptive; corrected.

**F5 — `contamination_sampler.py` writes files as a side effect of being run.** Executing it
created `data/doctrine_recheck/sample_2026-08-01.yaml` in the working tree (removed). It is a
generator requiring human judgment per doctrine-recheck §2.6, not a check, and must never sit in
a battery.

## What was built

Workflows **8 → 4**; check lists **4 → 1**.

- `governance/check-registry.yaml` — the single inventory. **51 active** (27 blocking / 21
  advisory / 3 informational) + **20 quarantined with a stated reason each**, so an unwired
  enforcer stays visible rather than becoming another silent 28.
- `scripts/run_checks.py` — the only thing that invokes a check. Classifies a diff into work
  kinds (`data`/`schema`/`synthesis`/`governance`/`render`/`tooling`) and runs the intersection.
  Selectivity: docs-only 6, `render` 10, `tooling` 16, `governance` 17, `schema` 20,
  `synthesis` 21, `data` 37.
- `ci.yml` absorbed `audit.yml` + `research-contract.yml`; a `classify` job emits the battery set
  and every other job gates on it. **No check names remain in any workflow.**
- `regenerate-derived.yml` absorbed the three identical `regenerate-*.yml` as a 3-leg matrix.
- `scripts/audit/migration_reproducibility.py` and `scripts/ci_helpers/check_doctrine_token.py` —
  the two inline blobs, now scripts with `--selftest`s.
- `preflight.sh` kept its name and became a wrapper over the same runner.

Retired workflows are in `_archived/workflows/` with a mapping README — moved, not deleted, per
CLAUDE.md §9 guardrail 2. A workflow cannot be redirect-stubbed: a stub left in
`.github/workflows/` would still execute.

## Corrections to my own findings (made by the adversarial pass, not by re-reading)

Both were written confidently into the first draft of `references/tooling-register.md` and both
were wrong. They are corrected **in place and marked**, not silently amended.

1. **`validate_reasoning.py` is not broken.** I called it "does not gate — reports errors and
   exits 0" and proposed fixing the exit code. It has a `--strict` flag: `--strict` exits 1,
   bare exits 0, verified both ways on the same corpus. The gate worked; nobody had passed it
   the flag. It is now wired **with** `--strict`. *Generalisable: before calling a tool broken,
   check for a mode you did not invoke.*
2. **`test_validate_evidence_state_2_4.py` is the opposite of stale.** I grouped it with
   `validate_db.py` as "written against a schema the DB no longer has". `governing_refs` **does**
   exist on `evidence_cell_state`; the crash happens inside `validate_evidence_state.py` running
   against the test's **fixture**, which predates the column. Retiring it on my reasoning would
   have deleted live regression cover for a wired blocking check.

## Adversarial review of the deferred proposals

**Executed:** wire `validate_reasoning --strict` (advisory); wire 8 green regression tests
(advisory, new `tests` battery keyed to `tooling`); regenerate the stale derived outputs; split
`test_db_integrity` into its own `db_integrity` battery.

**Withdrawn as unwise:**
- *Retiring the three broken duplicates.* `scripts/db.py:1120` **invokes** `validate_db.py` as a
  subprocess, so archiving it breaks a live path in the read/query workhorse. Its remaining
  callers sit in four `sessions/` records and a DR — historical documents stating what was true
  then, which must not be rewritten to tidy a filename. Quarantine already achieves the goal and
  is the **correct terminal state**, not a waypoint to retirement.
- *Promoting the advisory checks to blocking.* `research_protocol_audit` (2138 issues),
  `metadata_integrity_audit` (FAIL) and `population_integrity_audit` (31) are all red. Promoting
  them in the same window branch protection goes on would make the repo unmergeable outright.

## Verification

CI proved three properties live rather than in theory: `DB integrity` **skipped** while
`Data layer` ran (the battery split works); `Research contract` **succeeded** while containing
the red advisory `validate_reasoning` (levels work); `classify` passed its own registry selftest
before fanning out. Final run: 10 succeeded, 2 correctly skipped, 0 failed.

`run_checks.py --all` after the change reproduces the pre-change baseline exactly — no
regressions. The extracted reproducibility gate returns an identical PASS on all 7 invariants.

The `--selftest` earned its keep immediately, catching a bug in my own classifier before it
shipped: `path.lstrip("./")` strips those two *characters* in any order, silently turning
`.github/workflows/ci.yml` into `github/...` and misclassifying every workflow edit.

## Not done / honest limits

- **Branch protection was NOT enabled.** The owner asked for it explicitly; it could not be done
  from this session. The GitHub API returns `403 GitHub access is not enabled for this session`
  and no available tool exposes branch protection. **This is the one instruction in the session
  that went unfulfilled.** The full configuration — required-check set and three traps — is in
  `references/tooling-register.md` §6.7.
- **`test_db_integrity` is still RED** (26/35). Quantified: **106 of 863** `evidence_sources`
  rows carry a `verification_status` outside the enum; **80** `COMPLETE` rows have neither
  `first_author_last` nor `is_corporate_primary`. Content backlog, not a tooling defect.
- **`sessions/LATEST` was deliberately NOT advanced to this session.** It is read by the blocking
  `citation_mining_session` check. Tested: pointing it here yields "Total in scope: 191,
  Outstanding: 0" — the check would pass by having nothing to check. That is precisely the
  vacuous-green pattern this session spent its time removing, so making it worse to satisfy a
  naming convention would be self-defeating. LATEST remains stale (it points at a June session
  while July research sessions exist); fixing it properly means pointing it at the last
  *research* session, which is an owner call about what the pointer is for.
- No content, no synthesis, no DB writes, no migrations. The Opus synthesis floor was not
  approached: nothing in this session touched `best_practice_synthesis`.

---

# Planning instructions for the next session

**Read first:** `references/tooling-register.md` (the whole thing — §4 findings, §6 the
adversarially-reviewed proposal list with evidence). Then `governance/check-registry.yaml` for
what actually runs. Those two files are the durable state; this record is narrative around them.

**Orient mechanically, not from prose:**
```
pip install -r requirements.txt jsonschema
python3 scripts/run_checks.py --selftest      # registry coherent?
python3 scripts/run_checks.py --list          # what runs, what's quarantined and why
scripts/preflight.sh --all                    # the current true red/green picture
```
Expect `test_db_integrity`, `validate_reasoning`, `research_protocol_audit`,
`metadata_integrity_audit` and `population_integrity_audit` to be red. Those are **known and
pre-existing** — do not treat them as your regression. Confirm the delta before assuming
otherwise (`git worktree add /tmp/base origin/main` and run the same check).

**Owner-only, blocks nothing else:** enabling branch protection (§6.7). Do not require the
`DB integrity (content checks)` job until the backlog below is cleared, or no data-touching PR
will ever merge. Do require `Classify change` — a job skipped by an `if:` reports as *passing*
for required checks, so a battery-only requirement leaves a hole.

**Candidate next tasks, in the order I'd take them:**

1. **Clear the `test_db_integrity` backlog** (largest, highest value). 106 out-of-enum
   `verification_status` values and 80 authorless `COMPLETE` rows, via migrations —
   `scripts/emit_data_migration.py` then `scripts/migrate_db.py`, never a hand-edit. This is
   what stands between the repo and a merge gate that means something. It is **data work**: the
   R1–R15 research contract and migrations-only rule are live, and the `SessionStart` hook will
   re-inject them.
2. **Fix `test_validate_evidence_state_2_4.py`'s fixture** — add `governing_refs` to the fixture
   DB (one column), then register it in the `tests` battery. Small, self-contained, and it
   restores regression cover for a wired blocking check.
3. **Triage the quarantine, one script at a time.** Twenty entries, each with a stated reason.
   `pmp_audit` (3 issues) and `reasoning_doc_citations_audit` (2) are the smallest and most
   likely to become real gates quickly.
4. **Decide who owns schema drift** — `schema_reference_drift_audit.py` (red) and
   `validate_pydantic_schemas.py` (240 findings, exits 0) overlap. CLAUDE.md §10 calls
   `schemas/*.py` ↔ SQLite drift "a bug, not a convention", so one should become operative and
   the other retire. Needs an owner decision, then a small change.
5. **Adjudicate `validate_conflict.py`'s 11 errors** — unknown population codes `IntD` and `VIS`
   in `references/conflict-matrices/`. Either the matrices are stale or the code list is. This
   is **content**, and it touches population codes, so `DR-2026-07-22-work-from-axes` and
   `governance/functional-taxonomy.md` §3.3 govern: work from the functional axes, never coin
   umbrellas.
6. **Move `full_db_metadata_verification.py` (~298s, network-bound) onto the source-verification
   schedule**, beside `resolve-dois.yml`. Small.

**How to add a check** (do not edit a workflow — `ci.yml` has no check names in it and should
not gain any): add to `checks:` in the registry, run `--selftest`, run
`--kinds <kind> --explain` to confirm it fires where you expect, land it **advisory**, promote to
blocking in a **separate** commit once its false-positive rate is known.

**Two traps this session hit, worth not repeating:**
- Unquoted bash heredocs command-substitute backticks. A commit message with `` `tests` `` in it
  silently lost three terms. Use `<<'EOF'`.
- Before calling a tool broken, check `--help` for a mode you did not invoke (see the
  `validate_reasoning` correction above).
