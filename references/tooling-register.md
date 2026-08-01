# Ecosystem tooling register — assessment, consolidation, gating

**Date:** 2026-08-01
**Status:** OPERATIVE for §2–§3 (executed). §5–§6 are FINDINGS and OWNER-GATED PROPOSALS —
nothing in them has been executed.
**Scope:** every script under `scripts/` and `tools/`, every GitHub Actions workflow, the
harness hooks in `.claude/settings.json`, and the local gate `scripts/preflight.sh`.
**Method:** every script in `scripts/` and `tools/` was executed once against a clean
checkout of `main` with `pydantic`, `PyYAML` and `jsonschema` installed, and its exit code
and wall-clock time recorded. Nothing below is inferred from reading a script; the RED/GREEN
calls are observed. Re-derive any of it with `python3 scripts/run_checks.py --all`.

> This is a **derived map**, like CLAUDE.md. The authoritative inventory is
> `governance/check-registry.yaml`. Where this file disagrees with the registry, the
> registry wins and this file is the thing to correct.

---

## §1. What was there — the facts ledger

158 executable files under `scripts/` and `tools/`. **109 of them (69%) were referenced by
no workflow, no hook, and not by `preflight.sh`.** That is not automatically wrong — most
are one-shot converters and migration probes that have done their job — but it means an
unwired *enforcer* was indistinguishable from an unwired *converter*, which is exactly how
the 2026-07-24 finding ("28 enforcer scripts existed on disk while being referenced by NO
workflow") happened and could happen again.

**Eight workflows. Four separate hand-kept lists of checks.** `ci.yml`, `audit.yml`,
`research-contract.yml` and `preflight.sh` each transcribed their own list, and the four had
already drifted apart:

| Check | `ci.yml` | `audit.yml` | `research-contract.yml` | `preflight.sh` |
|---|:--:|:--:|:--:|:--:|
| `validate_axes` | — | — | — | ✓ |
| `validate_verification_consistency` | — | — | — | ✓ |
| `validate_jurisdiction` | ✓ | — | — | — |
| `validate_temporal` | ✓ | — | — | — |
| `check_rendered_docs` | — | — | — | ✓ |
| `render_audit.js` | — | — | — | ✓ |
| migration reproducibility | — | ✓ *(inline heredoc)* | — | ✓ *(second inline heredoc)* |

Two of those checks existed **only** in the local script, so CI had never once run them. The
migration-reproducibility invariant — the gate that actually enforces "never write the DB
directly" — existed as **two separately-maintained inline heredocs**. Adding a table to one
list would not have added it to the other, and nothing would have said so.

Three more workflows (`regenerate-vetting-surface`, `regenerate-evidentiary-audit`,
`regenerate-pipeline-completeness`) were structurally identical: same checkout, same Python
setup, same byte-identical short-circuit, same three-attempt race-aware push retry. They
differed only in generator, staged files, commit prefix and trigger paths.

---

## §2. What was consolidated (executed)

**Workflows: 8 → 4.**

| Before | After |
|---|---|
| `ci.yml`, `audit.yml`, `research-contract.yml` | **`ci.yml`** — one classify-gated workflow |
| `regenerate-{vetting-surface,evidentiary-audit,pipeline-completeness}.yml` | **`regenerate-derived.yml`** — one 3-leg matrix |
| `resolve-dois.yml`, `verify-urls.yml` | unchanged — see below |

Retired workflows are in `_archived/workflows/` with a README mapping each to its
destination. They were moved, not deleted (CLAUDE.md §9 guardrail 2); a workflow cannot be
redirect-stubbed, because a stub left in `.github/workflows/` would still execute.

`resolve-dois.yml` and `verify-urls.yml` were **deliberately left separate**: different
schedules, concurrency groups, network profiles and state tables (`pipeline_runs` vs
`url_verification_runs`), and almost no shared logic. Merging them would require routing a
cron to a job via `github.event.schedule` conditionals — more fragility than the saved
duplication is worth.

**Check lists: 4 → 1.** `governance/check-registry.yaml` is now the only inventory.
`scripts/run_checks.py` is the only thing that invokes a check. `ci.yml` and `preflight.sh`
both call that runner and contain no check names at all. Adding a check means editing the
registry; it does not mean editing a workflow, and it cannot mean adding it to three lists
and forgetting the fourth.

**Two inline blobs became scripts:**

- `scripts/audit/migration_reproducibility.py` — was the duplicated heredoc pair. Same 7
  core invariants, same DR-2026-05-28 exemptions (`evidence_source_authors`, `pipeline_runs`),
  verified to produce an identical PASS. Has a `--selftest` that builds two DBs differing by
  one row and asserts the comparator fires.
- `scripts/ci_helpers/check_doctrine_token.py` — was ~45 lines of inline bash in `ci.yml`
  that could not be run or tested locally. Same four exemptions (E1 non-synthesis, E2
  doctrine self-modification, E3 bot author, E4 merge commit), now with a 9-case `--selftest`.

**`preflight.sh`** kept its name and contract and became a thin wrapper. It now gates on your
diff by default; `--all` runs everything.

---

## §3. The gating model (executed)

Each check declares the **work kinds** it is relevant to. `run_checks.py` classifies a diff
into kinds and runs the intersection.

| Kind | Paths |
|---|---|
| `schema` | `schemas/**`, `scripts/migrations/**` |
| `governance` | `governance/**`, `decisions/**`, `attestations/**`, `references/project-standards.md`, `references/skill-registry.md`, `architecture/**` |
| `synthesis` | `references/bpc-reasoning/**`, `references/connection-reasoning/**`, `references/bpc/**`, `sessions/**` |
| `data` | `data/**` |
| `render` | `parts/**`, `site/**`, `specs/**`, `tools/*.html`, `audits/evidentiary-base-audit*`, `index.html`, `assets/**` |
| `tooling` | `scripts/**`, `tools/**`, `.github/**`, `.claude/**`, `requirements.txt` |

Resulting selectivity, out of 42 registered checks:

| Change is… | Checks selected |
|---|---|
| docs-only (no kind matched) | 6 |
| `tooling` | 8 |
| `render` | 10 |
| `governance` | 16 |
| `schema` | 19 |
| `synthesis` | 20 |
| `data` | 34 |

`kinds: [always]` means the check is cheap enough that gating buys nothing — gating exists to
save time and reduce noise, and below ~2s of stdlib-only work neither applies. **Cost decides,
not principle.** `validate_bpc` and `validate_cross_refs` are deliberately ungated for this
reason: gating a 0.2s check would only create a way for a misclassified diff to slip past it.

Levels map to the architecture v2.3 enforcement spectrum and live in the registry, not in
workflow YAML: **27 blocking / 12 advisory / 3 informational**. `run_checks.py` exits non-zero
only when a *blocking* check fails, which is why `continue-on-error:` no longer appears
scattered through job definitions where it was easy to lose track of.

Every check newly wired by this change — `matrix_consistency`, `audit_evidence_metadata`,
`pipeline_contract_audit`, `validate_axes`, `validate_verification_consistency` — landed as
**advisory**, per the repo's shakedown norm (precedent: `audit.yml`'s `attestation_evidence`,
all of `research-contract.yml`). Nothing was promoted to blocking in the commit that first
wired it.

---

## §4. Findings — defects in the apparatus itself

**F1 — CI's PR path filters never evaluated true. (Fixed.)** Three jobs were gated on

```yaml
contains(github.event.pull_request.changed_files, 'data/')
```

`changed_files` on the pull-request payload is an **integer** — the *count* of changed files.
`contains(12, 'data/')` is always false. The `schema`, `db_integrity` and `governance` jobs
therefore **never ran on any pull request in the repository's history**; they ran only on push
to `main`, i.e. after merge. The symptom was already recorded in CLAUDE.md §7 ("on a pull
request, `ci.yml` in practice runs only `syntax` + `structure`") — this is the cause. Thirteen
checks that could not previously run on a PR now run on the PRs that warrant them.

**F2 — `main` is not branch-protected.** Verified against the GitHub API on 2026-08-01:
`main` reports `protected: false`. There are no required status checks. **Every "BLOCKING"
label in the workflows is nominal** — a failing gate paints a red X and stops nothing.
CLAUDE.md §1 describes `main` as "protected by CI", which is aspirational rather than
descriptive. The registry still declares levels honestly, so they become teeth the day
protection is switched on; switching it on is an owner decision (§6).

**F3 — `validate_reasoning.py` does not gate.** It reports `1 with errors` (a missing
`F. Provenance trail` section) and **exits 0**. This is the *nine-step-synthesis* contract —
the check the 2026-07-23 enforcement plan (finding F2) identified as the one whose absence let
PR #56 pass green. Wiring it as-is would have added a green tick that means nothing, so it is
quarantined rather than wired. Fixing the exit code is a prerequisite, not a nicety.
`validate_pydantic_schemas.py` has the same shape: exits 0 while reporting 240 drift findings.

**F4 — `contamination_sampler.py` writes files as a side effect of being run.** Executing it
created `data/doctrine_recheck/sample_2026-08-01.yaml` in the working tree. It is a generator,
not a check, and per `governance/doctrine-recheck.md` §2.6 it requires human judgment and runs
only at scheduled rechecks. It must never appear in a check battery; it is quarantined with
that reason recorded.

**F5 — Three scripts crash rather than fail.** `validate_db.py`
(`no such column: doi_less_key`), `validate_items.py` (`IndexError: No item with that key`),
and `scripts/tests/test_validate_evidence_state_2_4.py` (`no such column: governing_refs`) are
written against a schema the DB no longer has. A crashing gate is worse than a missing one: it
reads as noise rather than as a finding.

**F6 — A classification bug, caught by the new selftest.** The first draft of the classifier
used `path.lstrip("./")`, which strips those two *characters* in any order — silently turning
`.github/workflows/ci.yml` into `github/workflows/ci.yml` and misclassifying every workflow
edit as unrecognised. `--selftest` caught it before the code was committed. Recorded because
it is the argument for the selftest existing.

### Gates currently RED on `main` (pre-existing; not caused by this change)

Baselined before any edit and unchanged after. Reported rather than demoted — a red gate that
gets quietly downgraded to advisory stops being information.

| Check | Level | State |
|---|---|---|
| `test_db_integrity` | blocking | **26/35 checks pass.** Failures in B05/B06 (enum values), C01–C04 (verification audit trail), G02 (author rows). Pre-existing owner-gated debt. |
| `evidentiary_audit_fresh` | blocking | **Committed outputs are stale versus the DB.** `audits/evidentiary-base-audit.{md,json}` and `tools/evidentiary-audit-dashboard.html` do not match a fresh regeneration. Fix: `scripts/regenerate_derived.sh`, then commit. Deliberately *not* fixed here — regenerating derived content is a separate act from consolidating tooling, and the drift is worth an owner's attention rather than a silent paper-over. |
| `research_protocol_audit` | advisory | 2138 issues (largely multilingual-coverage warnings). Advisory before this change too. |
| `metadata_integrity_audit` | advisory | VERDICT: FAIL. Advisory before this change too. |
| `population_integrity_audit` | advisory | 31 issues. Advisory before this change too. |
| `citation_mining_backlog_t2/t3` | informational | Backlog surfaces, not pass/fail claims. |

---

## §5. Quarantine — registered, never selected

21 scripts are registered in the `quarantine:` block of the registry with a stated reason, so
that an unwired enforcer stays *visible* instead of becoming another silent 28. Full reasons
are in the registry; the categories are:

- **Broken** (crash or don't gate): `validate_db`, `validate_items`, `validate_reasoning`.
- **Red, needing triage before they can gate**: `pmp_audit` (3), `reasoning_doc_citations_audit`
  (2), `schema_reference_drift_audit`, `adjudication_integrity` (274 tier inconsistencies),
  `code_currency_audit`, `validate_conflict` (11 unknown population codes),
  `pre_rehab_banner_audit` (red *by design* pre-launch — would be permanently red).
- **Not actually gates** (surfacing tools, reports, or generators whose exit code carries no
  verdict): `jurisdictional_divergence`, `validate_pydantic_schemas`, `contamination_sampler`,
  `check_phase_a_complete`, `validate_commits`, `validate_audit_runs`.
- **Wrong shape for CI**: `register_integrity_check` (needs an `html` argument *and* still
  enforces I3's repealed absolute form — the ENGINE-LAG flagged in the 2026-07-23 plan; it
  would false-fail correct weak-band rendering under DR-2026-07-21 Option A),
  `claims_docket` (subcommand CLI with no default action),
  `full_db_metadata_verification` (**~298 seconds**, network-bound — correct as a scheduled
  job, never as a PR gate).
- **Vacuous**: `validate_conflicts` (green, but the `conflicts` table has 0 rows, so it
  asserts nothing), `validate_item` (green, but its `data/items` YAML corpus does not exist).

---

## §6. Owner-gated proposals — NOT executed

Each needs a decision; none is a unilateral call.

1. **Enable branch protection on `main`** with the `classify` job plus the blocking batteries
   as required checks. Until then, F2 stands and "blocking" means "red X". This is the single
   highest-leverage change available, and it costs nothing to make except accepting that the
   two red gates in §4 must be fixed or explicitly waived first.
2. **Fix `validate_reasoning.py`'s exit code, then wire it** (advisory first). It is the
   nine-step-synthesis contract, and it is the specific check whose absence the 2026-07-23
   plan blamed for PR #56. Registered as `broken` today.
3. **Retire the three broken duplicates** to `_archived/` — `validate_db.py` (superseded by
   `test_db_integrity.py`, which CLAUDE.md §7 already tells you to prefer), `validate_items.py`
   (duplicate of the green `validate_item.py`), and
   `scripts/tests/test_validate_evidence_state_2_4.py`. File retirement is owner-gated
   (CLAUDE.md §9 guardrail 4), so they are quarantined and left in place.
4. **Adjudicate `validate_conflict.py`'s 11 errors** — unknown population codes `IntD` and
   `VIS` in `references/conflict-matrices/`. Either the matrices are stale or the code list
   is; either way it is a real finding, and it is *content*, not tooling.
5. **Decide who owns schema drift.** `schema_reference_drift_audit.py` (red) and
   `validate_pydantic_schemas.py` (240 findings, exits 0) overlap. CLAUDE.md §10 calls
   `schemas/*.py` ↔ SQLite drift "a bug, not a convention", so one of the two should become the
   operative gate and the other should be retired.
6. **Move `full_db_metadata_verification.py` onto the source-verification schedule.** At ~298s
   and network-bound it belongs beside `resolve-dois.yml`, not in any PR path.
7. **Wire the 8 green, unwired tests.** `test_assess_cell_pilot`, `test_directness_2_2`,
   `test_evidence_cell_state_2_3`, `test_graph_audit` (27s), `test_jurisdictional_divergence`,
   `test_pipeline_contract`, `test_url_verifier`, `test_verification_pipeline` all pass and are
   invoked by nothing. They are cheap regression cover for the audit scripts and are the
   obvious next registry additions; held back here only to keep this change reviewable.
8. **Promote the shakedown checks to blocking** once their false-positive rate is known — the
   flip is meant to be a separate, deliberate, owner-gated commit.

---

## §7. How to add or change a check

1. Add an entry to `checks:` in `governance/check-registry.yaml`: `id`, `cmd`, `battery`,
   `kinds`, `level`, `cost`.
2. `python3 scripts/run_checks.py --selftest` — verifies the id is unique, the battery is
   declared, the executable exists, and the level is spelled correctly.
3. `python3 scripts/run_checks.py --kinds <kind> --explain` — confirm it is selected when you
   expect and skipped when you don't.
4. Land it as `advisory`. Promote to `blocking` in a **separate** commit once you know its
   false-positive rate.

Do **not** add the check to a workflow. `ci.yml` has no check names in it and should not gain
any; that property is the whole point.

`governance/check-registry.yaml` and `.github/workflows/` are both CODEOWNERS-protected, so
every change here carries owner sign-off by construction.
