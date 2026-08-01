# Ecosystem tooling register — assessment, consolidation, gating

**Date:** 2026-08-01
**Status:** OPERATIVE. §2–§3 and the "Executed" half of §6 are done and in CI. §4–§5 are
FINDINGS. The remainder of §6 is proposals — two of them withdrawn on review as unwise, one
blocked on repo-settings access the session does not have.
**Revised:** 2026-08-01, after an adversarial re-review of every proposal. Two claims in the
first draft (F3, F5) were overturned by that review and are corrected in place, with the
correction marked rather than silently applied.
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

Resulting selectivity, out of 51 registered checks:

| Change is… | Checks selected |
|---|---|
| docs-only (no kind matched) | 6 |
| `render` | 10 |
| `tooling` | 16 |
| `governance` | 17 |
| `schema` | 20 |
| `synthesis` | 21 |
| `data` | 37 |

`kinds: [always]` means the check is cheap enough that gating buys nothing — gating exists to
save time and reduce noise, and below ~2s of stdlib-only work neither applies. **Cost decides,
not principle.** `validate_bpc` and `validate_cross_refs` are deliberately ungated for this
reason: gating a 0.2s check would only create a way for a misclassified diff to slip past it.

Levels map to the architecture v2.3 enforcement spectrum and live in the registry, not in
workflow YAML: **27 blocking / 21 advisory / 3 informational**. `run_checks.py` exits non-zero
only when a *blocking* check fails, which is why `continue-on-error:` no longer appears
scattered through job definitions where it was easy to lose track of.

Every check newly wired by this change — `matrix_consistency`, `audit_evidence_metadata`,
`pipeline_contract_audit`, `validate_axes`, `validate_verification_consistency`,
`validate_reasoning --strict`, and the eight `tests` battery entries — landed as
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

**F3 — `validate_reasoning.py` needs `--strict`, and nothing passed it.** Invoked bare it
reports `1 with errors` (a missing `F. Provenance trail` section) and **exits 0**; with
`--strict` it exits 1 (`if args.strict and err_files: return 1`). Verified both ways against
the same corpus. This is the *nine-step-synthesis* contract — the check the 2026-07-23
enforcement plan (finding F2) identified as the one whose absence let PR #56 pass green.

> *Corrected 2026-08-01:* the first draft of this register called it "broken — does not gate"
> and proposed fixing the exit code. That was wrong. The gate works; nobody had passed it the
> flag. It is now wired **with `--strict`**, advisory (it is red on one doc). The lesson
> generalises — before calling a tool broken, check whether it has a mode you did not invoke.

> *Corrected again 2026-08-01 (second pass):* the sentence that stood here — "`validate_pydantic_schemas.py`
> genuinely does have the exits-0-while-reporting-240-findings shape, with no strict mode" — was
> itself an instance of the error the paragraph above it warns about. It **has** `--strict`
> (`scripts/audit/validate_pydantic_schemas.py:255`); verified both ways, bare exits 0 and
> `--strict` exits 1. Having just corrected this mistake for `validate_reasoning`, the same
> draft repeated it one paragraph later about a different tool. The check is now wired with
> `--strict`, advisory. **The lesson did not generalise by being written down** — it generalised
> only when a later pass re-ran every tool's `--help`. That is an argument for the mechanical
> re-check, not for a better-remembered rule.

`validate_commits.py` is a third instance of the same shape in the other direction: both its
bare and `--strict` invocations exit 1, but what they report is the script's own rot, not the
commits' — see its quarantine entry.

**F4 — `contamination_sampler.py` writes files as a side effect of being run.** Executing it
created `data/doctrine_recheck/sample_2026-08-01.yaml` in the working tree. It is a generator,
not a check, and per `governance/doctrine-recheck.md` §2.6 it requires human judgment and runs
only at scheduled rechecks. It must never appear in a check battery; it is quarantined with
that reason recorded.

**F5 — Three scripts crash rather than fail, for two different reasons.** A crashing gate is
worse than a missing one: it reads as noise rather than as a finding.

- `validate_db.py` (`no such column: doi_less_key`) and `validate_items.py`
  (`IndexError: No item with that key`) expect a schema the DB no longer has. Genuinely stale.
- `scripts/tests/test_validate_evidence_state_2_4.py` (`no such column: governing_refs`) is the
  **opposite** case. `governing_refs` *does* exist on `evidence_cell_state`; the crash happens
  inside `scripts/validate_evidence_state.py` when it runs against the test's **fixture** DB,
  which predates the column. The script is current and the fixture is behind it — a one-column
  fixture update, not a stale tool.

> *Corrected 2026-08-01:* the first draft lumped all three together as "written against a
> schema the DB no longer has". For the third that is backwards, and it matters: retiring it on
> that reasoning would have deleted live regression cover for a wired blocking check.

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
| `test_db_integrity` | blocking | **STILL RED. 26/35 checks pass.** Failures in B01/B02/B05/B06 (enum values), C01–C04 (verification audit trail), G02 (author rows). **Both figures and the verdict in the first draft were wrong — see §4.1 below.** The out-of-enum count is **81, not 106**, and the failure is a *split* tool/content verdict, not a uniform content backlog. Held in its own `db_integrity` battery so branch protection can be enabled without deadlocking every data-touching PR on it. |
| `evidentiary_audit_fresh` | blocking | **FIXED 2026-08-01.** Regenerated via `scripts/regenerate_derived.sh`. The drift was purely the report's "as-of" date (2026-07-26 → 2026-07-27, tracking the DB's own `max(updated_at)` after the source-verification commit); no substantive figure moved. Both `--check` gates now pass. |
| `validate_reasoning` | advisory | Newly wired with `--strict`. Red on 1 doc (missing `F. Provenance trail`). See F3. |
| `research_protocol_audit` | advisory | 2138 issues (largely multilingual-coverage warnings). Advisory before this change too. |
| `metadata_integrity_audit` | advisory | VERDICT: FAIL. Advisory before this change too. |
| `population_integrity_audit` | advisory | 31 issues. Advisory before this change too. |
| `citation_mining_backlog_t2/t3` | informational | Backlog surfaces, not pass/fail claims. |

### §4.1 The `test_db_integrity` failure, re-derived 2026-08-01

The first draft asserted "**106 of 863** rows carry a `verification_status` outside the enum…
That is a content backlog, not a tooling defect." Both halves are wrong, and the second half
was load-bearing: it is the premise on which §6.7 defers requiring this job in branch
protection, and on which standing task 12 is scoped as data work.

**The count is 81.** 106 is `863 − 757` — total rows minus plain `VERIFIED` — which counts the
25 `UNVERIFIED-1` rows as violations even though `UNVERIFIED-1` **is** in the test's own list.
The measured distribution:

| `verification_status` | rows | in the test's enum? |
|---|--:|---|
| `VERIFIED` | 757 | yes |
| `VERIFIED-2` | 71 | no |
| `UNVERIFIED-1` | 25 | **yes — wrongly counted as a violation** |
| `DISPUTED` | 7 | no |
| `VERIFIED-WITH-CORRECTION` | 2 | no |
| `VERIFIED-1` | 1 | no |

**The verdict is split.** Per failing sub-check:

| Sub-check | Verdict | Why |
|---|---|---|
| B01, B06 | **stale test** | The test's list was last curated **May 2026** (its own comments cite the 2026-05-12 proposal and DR-2026-05-19). `DISPUTED` and `CLOSED-DECIDED` were then created by the **owner-approved** DR-2026-07-20 migration; `VERIFIED-WITH-CORRECTION` is in `schemas/enums.py` and the test simply omits it. `VERIFIED-2` (71 rows, 19 migrations) records verification by convergent retrieval rather than a first-hand render — an honesty distinction that collapsing to `VERIFIED` would destroy. |
| B02, B05 | **mixed** | `PARTIAL` and `code` are coined consistently with disclosed rationale across several sessions; the lowercase `high`/`medium` (4 rows) and `grey_literature`/`magazine_article` (3 rows) are genuine junk. |
| C01–C04, G02 | **genuine content backlog** | One July citation-mining batch inserted rows with DOIs but no `doi_resolution_outcome`, no `source_type` and premature `COMPLETE` labels. G02's figure is **113**, not 80 — 80 was C03's number. The scheduled resolver cannot self-heal these: every phase targets `WHERE doi IS NULL`, and Phase-4 author enrichment filters on a `source_type` these rows do not have. |

**Not fixed here, deliberately.** Widening the test's enum would be the obvious tooling fix and
is the wrong unilateral act: `verification_status` has **no CHECK constraint**, and four
vocabularies coexist — the test's list, `schemas/enums.py`, the stale draft in
`architecture/schema-spec.md`, and live practice. Ratifying one is a D-SCHEMA decision. The
established pattern is visible in the test's own comments (`COMPLETE-STATUTORY` per DR-2026-05-18,
`IS-PAYWALL` per DR-2026-05-19): the vocabulary changes, a DR ratifies it, the test is amended.
What went missing in July was that third step. **That makes most of B01/B06 process debt, not
content debt** — and it means the content backlog standing task 12 must clear is C01–C04/G02,
not the enum rows.

---

## §5. Quarantine — registered, never selected

**Revised 2026-08-01 (second pass).** Every entry was re-run and its stated reason checked
against observed behaviour. **Five of the twenty reasons were factually wrong**, four entries
were de-quarantined, and the count is now **16**. The corrections are recorded in the registry
at each entry. That five of twenty stated reasons did not survive their first audit is the
finding here: a quarantine reason is an *assertion about a tool*, and writing one down does not
verify it.

De-quarantined and now wired advisory: `pmp_audit`, `reasoning_doc_citations_audit`,
`claims_docket` (the registered command was missing its `check` subcommand — the recorded "no
default action, exits 0" was a fact about the bare invocation, not the tool), and
`validate_pydantic_schemas` (with `--strict`).

Remaining categories:

- **Broken** (crash or don't gate): `validate_db`, `validate_items`.
  *(`validate_reasoning` was listed here in the first draft and should not have been — it was
  wired with `--strict` by the same session that wrote this list. Corrected.)*
- **Red, needing triage before they can gate**: `schema_reference_drift_audit` (whose stated
  subject was wrong — it scans *scripts' SQL table references*, not `schemas/*.py`, and its
  signal is now 12/19 lexical false positives), `adjudication_integrity` (274 tier
  inconsistencies), `code_currency_audit`, `validate_conflict` (11 unknown population codes —
  note its own detection regex is also old-taxonomy), `pre_rehab_banner_audit` (**not** red by
  design, as first recorded: it is a file↔DB drift gate red on a fixable 6-slug mismatch).
- **Not actually gates** (surfacing tools, reports, or generators whose exit code carries no
  verdict): `jurisdictional_divergence` (though the registry's own `informational` level fits
  it), `contamination_sampler`, `check_phase_a_complete` (itself partly rotten — it reports "0
  item headings found" against the v10 parts), `validate_commits` (red against *present*
  compliant commits because its skill/author/merge token lists have rotted, not against
  history), `validate_audit_runs` (green with real assertions over 87 `item_audit_runs` rows;
  wiring awaits only a named owner).
- **Wrong shape for CI**: `register_integrity_check` (needs an `html` argument *and* still
  enforces I3's repealed absolute form — the ENGINE-LAG flagged in the 2026-07-23 plan; it
  would false-fail correct weak-band rendering under DR-2026-07-21 Option A),
  `claims_docket` (subcommand CLI with no default action),
  `full_db_metadata_verification` (**~298 seconds**, network-bound — correct as a scheduled
  job, never as a PR gate).
- **Vacuous**: `validate_conflicts` (green, but the `conflicts` table has 0 rows, so it
  asserts nothing), `validate_item` (green, but its `data/items` YAML corpus does not exist).

---

## §6. Proposals — adversarially reviewed 2026-08-01

Each of the original eight was re-examined against the evidence rather than carried forward on
momentum. Three were **executed**, two were **withdrawn as unwise**, one is **blocked on
access**, and the rest stand. Where the review overturned an earlier claim in this file, the
correction is recorded at the finding (F3, F5) rather than quietly applied.

### Executed

1. **Wire `validate_reasoning.py` with `--strict`** (advisory). The nine-step-synthesis
   contract now runs on synthesis diffs. See F3 — the earlier "fix the exit code" framing was
   wrong; it needed a flag, not a patch.
2. **Regenerate the stale evidentiary audit.** One of the two red blocking gates is now green.
   Drift was the as-of date only.
3. **Wire the 8 green regression tests** (advisory, new `tests` battery, keyed to `tooling`).
   Six carry mutation harnesses or assertion counts; `test_directness_2_2` is recorded as
   partially vacuous (its live-smoke leg SKIPs without `/tmp/work14.db`) so its pass is not read
   as broader than it is. `test_generate_parts_4_2` was **excluded** — it SKIPs entirely without
   a fixture DB and would be a pure green tick.
4. **Split `test_db_integrity` into its own `db_integrity` battery.** Prerequisite for enabling
   branch protection without freezing data work — see below.

### Withdrawn as unwise

5. **Retiring the three broken duplicates — WITHDRAWN.** `scripts/db.py:1120` *invokes*
   `validate_db.py` as a subprocess, so archiving it breaks a live path in the read/query
   workhorse. Its remaining references sit in four `sessions/` records and a DR — historical
   documents that state what was true at the time and must not be rewritten to tidy a filename.
   `validate_items.py` is the same story via DR-2026-07-23 and two workplans. Retirement buys
   tidiness at the cost of editing immutable records, and **quarantine already achieves the
   actual goal**: the script can no longer be mistaken for a working gate. Quarantine is the
   correct terminal state, not a waypoint to retirement.
6. **Promoting the advisory checks to blocking — WITHDRAWN, and specifically inadvisable now.**
   `research_protocol_audit` (2138 issues), `metadata_integrity_audit` (FAIL) and
   `population_integrity_audit` (31) are all red. Promoting them in the same window that branch
   protection goes on would make the repository unmergeable outright. The shakedown norm exists
   for exactly this; the flip stays a separate, deliberate, later decision.

### Blocked on access — needs the owner

7. **Enable branch protection on `main`.** Could not be executed from this session: the GitHub
   API returns `403 GitHub access is not enabled for this session`, and no available tool
   exposes branch protection. It must be set in repo Settings → Branches. **The configuration
   matters more than the switch** — three traps:

   - **Do not require the `DB integrity (content checks)` job.** It is red against a real
     content backlog (§4), so requiring it would make every data-touching PR permanently
     unmergeable — i.e. it would freeze the project's main activity. This is why that check was
     split into its own battery.
   - **Do require `Classify change (work kinds → batteries)`.** A GitHub job skipped by an `if:`
     condition reports as *passing* for required status checks. So requiring only the battery
     jobs leaves a hole: if classification breaks, the batteries skip and the PR goes green on
     checks that never ran. `classify` always runs and carries the registry selftest, so it is
     the one job whose failure means the gating itself is broken.
   - **Do not require pull-request reviews** (or leave admin bypass on). This is a single-author
     repo; a review requirement with no second reviewer is a deadlock.

   Recommended initial required set — every one of these is green today:

   ```
   Classify change (work kinds → batteries)
   Syntax (UTF-8, JSON, YAML)
   Structure (BPC, cross-refs)
   Data layer (DB integrity, migration reproducibility, citation mining)
   Schema (entity YAML, evidence state, populations, jurisdictions)
   Governance (decisions, doctrine recheck, adversarial use, contract)
   Attestations (presence, schema, evidence, verdict)
   Research contract (definition-of-done + its enforcers)
   Render (derived-output freshness, rendered-document integrity)
   ```

   Add `DB integrity (content checks)` once the backlog in §4 is cleared.

   > **Fragility worth knowing:** required checks are matched by job **name string**. The names
   > above are long and contain commas and parentheses. Renaming a job in `ci.yml` silently
   > turns its required check into "expected — waiting", and every PR hangs. If you enable
   > protection, treat those `name:` fields as a public interface.

### Still standing

8. **Adjudicate `validate_conflict.py`'s 11 errors** — unknown population codes. The first draft
   named `IntD`/`VIS`; the full set is `IntD, VIS, NEU, OFS, DBL`, none of which exist among the
   23 live `populations` codes. The validator's own detection regex is old-taxonomy too, so
   fixing the matrices alone will not clear it. Content + tooling; `DR-2026-07-22-work-from-axes`
   governs (work from the functional axes, never coin umbrellas).
10. **Move `full_db_metadata_verification.py` (~298s, network-bound) onto the source-verification
    schedule**, beside `resolve-dois.yml`. Confirmed a pure audit with no DB writes; it also
    accepts an undocumented positional row-limit, so a bounded smoke variant is possible.
12. **Clear the `test_db_integrity` backlog** — **scoped down by §4.1**. The genuine content
    debt is C01–C04/G02: one July citation-mining batch (~105 rows) needing
    `doi_resolution_outcome`, `source_type`, and author data or a `COMPLETE` downgrade, plus 7
    rows with no audit trail and 7 junk enum values. The enum rows are **not** part of it.

### Resolved by the 2026-08-01 second pass

9. ~~**Decide who owns schema drift**~~ — **the premise was false.** The two tools never
   overlapped: `validate_pydantic_schemas.py` compares Pydantic models to SQLite columns;
   `schema_reference_drift_audit.py` scans *scripts' SQL table references* against the live DB
   and its docstring explicitly disclaims the Pydantic comparison. Both the registry's and this
   file's descriptions of them were wrong. Resolved by wiring `validate_pydantic_schemas
   --strict` as the owner of the §10 invariant (advisory, 236 findings) and correcting the other
   entry. **Proposed, not executed:** retiring `schema_reference_drift_audit` — its one gating
   check is carried with better precision by the already-wired `graph_audit`
   (`code.phantom_table`, CTE/view-aware), but retirement is owner-gated.
11. ~~**Update `test_validate_evidence_state_2_4.py`'s fixture**~~ — **done.** It was not "one
    column": the fixture built its DDL from migration 024 alone, so it needed to track 026 and
    027 as well. It now discovers its DDL from the migrations that touch the tables and carries
    a guard that fails as a stale *fixture* rather than as a broken validator. Two assertions
    were also absent rather than merely unrunnable, including the `stated ⇒ governing_refs`
    anti-hallucination gate, which had no test at all. Wired advisory; 12/12.
    It had been in **neither** the active checks nor the quarantine block — unwired with no
    stated reason, which is the exact condition this register exists to make impossible.

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
