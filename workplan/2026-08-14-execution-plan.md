# 2026-08-14 — Execution plan for the remediation workplan

**Executes** `workplan/2026-08-14-remediation-workplan.md` (the plan) against
`workplan/2026-08-14-pipeline-audit-synthesis.md` (the findings). This document says *who does
what, in what order, at what tier*, and — first — *what is not ours to execute*.

**Baseline, re-derived at HEAD `058d729` rather than inherited** (guardrail §9-1). The workplan's
executable-layer claims were spot-checked before planning; all held:

| Fact | Workplan says | Verified at HEAD |
|---|---|---|
| `run_checks.py --all` | 57 green / 8 advisory (synthesis) | **56 green / 9 advisory / 0 blocking** — the extra red is `context_map_fresh`, exactly as the plan §2.8 predicted |
| `--selftest` | PASS | PASS (C1–C7; 32/65 unattributed, 4 contract criteria unclaimed) |
| Active checks | 65: 28 blocking / 34 advisory / 3 informational | identical |
| `min_items` coverage | 6 of 65 | **6 of 65**; `no_floor` exists nowhere |
| `readonly_db_open_audit.py` | prints a false `40/40` | prints `RESULTS: 40/40` |
| `verify_urls.py` zero-pool write | inserts a run row regardless of `pool_size` | confirmed, `scripts/verify_urls.py:416–433` — pool computed, row inserted unconditionally |
| `item_code` grammar split | two graph extractors at `^[A-K]-\d{2}$` | confirmed: `extract_db.py:44`, `extract_content.py:34`; canonical `[a-z]?` form in `schemas/item.py:57` |
| `EXAMINED:`/vacuity | convention exists, runner flattens it | confirmed — `EXAMINED_RE` + `vacuity_failure()` already in `run_checks.py:272–301`; no NOTHING-IN-SCOPE status |
| Doctrine SHA | — | `0f2f525` |

**A trap this baseline caught.** The first `--all` run reported **5 blocking failures**
(`validate_schema`, `validate_evidence_state`, `audit_adversarial_use`, `decision_capture`,
`doctrine_recheck`). None was real: `pip install -r requirements.txt` had aborted on a PyYAML
system-package conflict, so `pydantic` was absent and every pydantic-dependent check failed at
import. Installing `pydantic==2.13.3` alone cleared all five. **A red blocking check in this repo is
an environment claim before it is a repo claim** — this is §9-1 in a form the guardrail does not
currently name, and it is the same shape as the audit's own §2.2 false-absence family.

---

## 1. Scope boundary — what we execute, and why the rest is not ours

The plan is explicit: *"Nothing here has been executed. Every migration, file move, and doctrine
edit below is a proposal."* That sentence, plus `CLAUDE.md` §5 ("for irreversible or structural
moves, propose; don't unilaterally execute"), draws the line for us:

| Track | Contents | Disposition |
|---|---|---|
| §0 + Track A | 9 executable-layer commits — code, registry, self-tests | **EXECUTE** |
| Track B, commits D–F (partial) | Corrections to `CLAUDE.md`, a *derived map* that says of itself "this file should be corrected" | **EXECUTE** (factual corrections only) |
| Track B, commits A–C, G, H | Doctrine amendment + one SHA rotation; append-only ledger amendments; DR forward-notes and ratification flips; a new protocol section + register entry + migration | **DEFER — owner** |
| Track C | Migrations 058–063 | **DEFER — D-SCHEMA, Change-Order (decision #4)** |
| Track D | Retirements, file moves, migrations 065–066 | **DEFER — owner-gated (§9-4, decision #8)** |
| §7 | Ten owner decisions, three DG-NON | **DEFER — not pre-decided** |

Two judgment calls inside that boundary, stated so they can be overruled:

1. **§0's guard is executed, not deferred.** Decision #5 is the durable answer and is the owner's;
   the plan itself frames the ten-line guard as the bridge and sets a deadline of **2026-08-15
   06:00 UTC** — inside 24 hours. Landing a guard that makes a scheduled job write *nothing when it
   has nothing to do* neither forecloses #5 nor institutionalises the third write path. Deferring it
   costs the exact rebuild reproducibility the audit called its strongest positive result.
2. **New checks land `advisory`, never blocking.** Plan §9 puts promotion-before-known-false-positive-rate
   out of scope, and the promotion discipline is `CLAUDE.md` §2's spectrum. Two new checks are born
   here (C8's structural assertion is a selftest, not a registry check; the range guards are B07/B08);
   both start advisory.

**Not executed and not deferred — declined as out of plan:** anything touching content research,
the 28 quantified item names (§5, frame), and Track C/D prototyping beyond what already exists.

---

## 2. Tier assignments

The repo's routing floor (PI rule #2, DR-2026-06-10) binds `best_practice_synthesis` to Opus-class.
**No commit in scope writes synthesis**, so that floor is not the live constraint here. The live
constraint is the audit's own Lesson 2 — *never act on a single agent's absence claim* — so tiering
is by **judgment density and blast radius**, and every delegated unit carries a verification command
its own output must satisfy.

| Tier | Assigned work | Rationale |
|---|---|---|
| **Opus (direct — this session)** | A4 vacuity design + A6 C8 assertion (the runner every check flows through); scope boundary; commit composition; the fidelity review's adjudication | Design decisions with repo-wide blast radius. A4 changes how 65 checks are *read*; a wrong call here manufactures the failure mode it is meant to fix. |
| **Opus (subagent, adversarial)** | Independent fidelity review of the full diff before push | The repo's own culture: every planning pass in this series was broken by its reviewer. A reviewer that shares my priors is worthless, so it re-derives rather than inherits. |
| **Sonnet (subagents)** | A1, A2, A3, A5, A7, A8, A9 — bounded code fixes with a named file set, a stated defect, and a mechanical acceptance test | Spec-bounded work. Each has a falsifiable done-condition (a self-test that flips, a grep that returns zero, a count that changes), so tier risk is absorbed by the acceptance gate rather than by trust. |
| **Haiku** | Not used | The census work that would suit it (rw-connect enumeration, floor coverage) is *inside* the acceptance criteria of A3 and A6, where an independent enumeration pass would be re-run by the check itself anyway. Splitting it would add a handoff without adding a verification. |

**Delegation contract.** Subagents edit the working tree and **do not commit** — commits are composed
here, one per plan item, so the ledger keeps the plan's numbering and a bad unit can be dropped
without unpicking history. Every subagent is given: the defect, the file set, the acceptance command,
and an explicit instruction to report *what it could not verify* rather than to round up.

---

## 3. Wave sequencing

Waves exist because of file collisions, not ceremony. `run_checks.py` is touched by A4 and A6;
several check scripts are touched by both A5 (banners) and A2/A3 (their defects).

> **Sequencing correction, found while writing this plan.** A9 was drafted into Wave 1 as
> "`emit_data_migration.py` + registry". It is not a registry change: `ENUM_GUARDS` entries name
> their enforcer as `test_db_integrity.py [B03]`/`[B04]`, so B07/B08 are **B-series checks inside
> `test_db_integrity.py`** — the same file A7 rewrites. A9 therefore moves to Wave 3, serialized
> *after* A7. Recorded rather than silently fixed, because "no table is touched by both tracks" was
> the plan's own basis for calling its ordering a convention rather than a dependency, and here the
> convention had a real dependency hiding in it.

**Wave 1 — parallel, disjoint file sets (Sonnet ×3)**

| Item | Files | Defect | Acceptance |
|---|---|---|---|
| **A1** | `scripts/verify_urls.py` | Inserts a `url_verification_runs` row at `pool_size == 0`; the table is not in `EXEMPT_TABLES`, so a scheduled run ends exact rebuild reproducibility | Early return before the INSERT; prints `EXAMINED: 0` + `NOTHING-IN-SCOPE`; `test_url_verifier` 25/25; `migration_reproducibility --deep` PASS |
| **A2** | `graph_audit.py`, `graph/extract_db.py`, `graph/extract_content.py`, `register_integrity_check` | `fetchone()[0]` on an empty `connections` table → `TypeError`; a mutation missed by the check's own selftest; `^[A-K]-\d{2}$` rejects the live `A-10b` | `test_graph_audit` green; `register_integrity_check` FIRES on all mutations incl. COMPLETENESS; `A-10b` matched by both extractors |
| **A3** | `readonly_db_open_audit.py` + the reader files it exonerates | Prints `40/40` on a matcher with a blind spot; the plan names **9 rw connects across 8 files**, incl. `generate_parts.py:435` and `tools/regenerate_vetting_surface.py:41` (docstring says "Read-only") | Widened matcher; every rw open on the canonical DB in a reader either converted to `mode=ro` or explicitly justified; audit re-prints a *true* certificate |
**Wave 2 — the runner (Opus, direct; serialized against Wave 1's registry edits)**

- **A4 — NOTHING-IN-SCOPE in the runner.** A parsed line extending the existing `EXAMINED:`
  convention, *not* an exit code (0/1 is spoken for) and *not* a sidecar (65 scripts would need
  rewriting). Acceptance: the already-instrumented checks flip with **zero script changes**;
  `--selftest` stays PASS; the summary line distinguishes green from nothing-in-scope.
- **A6 — declare the floor.** `min_items` or an explicit `no_floor` on all 65 active checks, plus
  **C8**, a selftest assertion forcing every *future* check to declare its vacuity regime. C8 is the
  structural half; without it A6 is a one-time sweep that decays. This is the repo's four-times-repeated
  failure mode, so the fix must be the assertion, not the sweep.

**Wave 3 — post-runner (Sonnet). A5 and A8 in parallel; A7 then A9 serialized on `test_db_integrity.py`.**

| Item | Files | Work | Acceptance |
|---|---|---|---|
| **A5** | remaining zero-subject checks | Extend the `EXAMINED:` contract so the runner can see them | Each prints a truthful subject count; `--all` renders them as nothing-in-scope, not green |
| **A7** | `scripts/tests/test_db_integrity.py`, `data/decisions/decision_register.yaml` | L01 compares 6 of 22 columns; D-0158/59/60 diverge on `delegation_rationale`. Widen to full-field **and** reconcile the three rows *toward the DB* (§9-5: the DB is canonical) | L01 detects exactly D-0158/59/60 on exactly `delegation_rationale` before the fix, zero false positives across the other 157; green after; **YAML edit only, no migration** |
| **A8** | `preflight.sh`, `governance/context-map.yaml` | `preflight.sh:33–36` asserts `test_db_integrity` is red on main; it passes 70/70. Regenerate the context map the synthesis commit skipped | Prose matches observed state; `context_map_fresh` green |
| **A9** *(after A7)* | `emit_data_migration.py`, `scripts/tests/test_db_integrity.py` | `evidence_sources.tier` is bare `INTEGER`; `ENUM_GUARDS` cannot see unquoted integer literals, so `tier = 7` passes everything | New `RANGE_GUARDS` at the write path + B07/B08 range checks; a migration writing `tier = 7` is refused and a valid one is not; `test_db_integrity` still green |

**Wave 4 — `CLAUDE.md` factual corrections (Sonnet, single file)**

Four false statements, all verified: §1 "protected by CI" vs §0/§7 "not branch-protected" — **`main`
*is* protected**, so all three are wrong; §4/§6 describe the pre-057 migration layout; §8's
re-attestation model is the retired flat five-commit window (materiality via
`governance/doctrine-deltas.json` is live, `RE_ATTESTATION_WINDOW` is a dead constant); §10 names
`session_pointer_resolvable` as a blocking check that exists in neither code nor registry.

Corrections only. **No doctrine, no ledger, no PI** — those are Track B commits A–C and belong to
the owner.

**Wave 5 — adversarial audit (four independent lenses), then push.** See §4.

---

## 4. The end-of-execution adversarial audit

Four **independent** lenses, run in parallel against the finished diff, each blind to the others'
verdicts and each instructed to *refute* rather than to confirm. A lens that returns "looks good"
without having tried to break something has not run. Findings are adjudicated here (Opus, direct);
a confirmed finding is fixed or reverted before push, and a rejected one is recorded with its reason
rather than dropped.

| Lens | Tier | Asks |
|---|---|---|
| **Fidelity** | Opus | Does the diff do what the workplan said, and *only* that? Did anything owner-gated get executed? Is every commit-message claim re-derived rather than inherited? |
| **Logic** | Opus | Are the new predicates *correct* — off-by-one, inverted conditions, a guard that fires on the wrong branch, a vacuity status that a real failure could masquerade as? Does any fix create the defect it removes? |
| **Minimization** | Sonnet | Is any of this code unnecessary? Duplicated logic, a helper that restates an existing one, a new abstraction where a parameter would do, dead branches, defensive code for conditions the caller already excludes. The plan's own standard is "the fix is ten lines". |
| **Structure** | Sonnet | Compliance with house form: commit-message grammar and doctrine-token rules, registry-not-workflow for check changes, `GUIDEBOOK_DB_PATH` honoured, migrations-only respected, `git grep` not ripgrep in sweeps, no hand-edits to generated output, advisory-at-birth for new checks. |

### 4.1 Fidelity criteria — what the fidelity lens is instructed to break

Not "does it look right". Five falsifiable questions, each with a way to answer *no*:

1. **Did anything owner-gated get executed?** A migration, a file move into `_archived/`, a doctrine
   or ledger edit, a check promoted to blocking, a DG-NON item decided. Any hit is a revert.
2. **Does A4 make vacuity visible, or just relabel it?** A reviewer must be able to tell an earned
   green from a zero-subject green on a *blocking* check, from the summary line alone.
3. **Is C8 actually structural?** Does a newly added registry entry with no floor declaration fail
   the selftest? If not, A6 decays and the repo re-runs this failure mode a fifth time.
4. **Did A3's certificate become true, or merely different?** The count moving from 40/40 to something
   else proves nothing; the question is whether a reader holding a rw handle on the canonical DB can
   still pass.
5. **Is every claim in the commit messages re-derived?** The audit's Lesson 2 applies to us: an
   absence we assert must have been searched for with `git grep` (never ripgrep — the root `.ignore`
   hides seven directories and makes an unsafe claim look safe).

Acceptance for the whole batch: `--selftest` PASS, **0 blocking failures**, and the advisory red count
**strictly lower** than the baseline 9 — with each remaining red named and attributed.

---

## 5. What this plan hands the owner

Executing Track A does not reduce the decision surface; it makes the instruments trustworthy enough
to act on it. The queue is unchanged: **decisions #1–#10** in the workplan §7, of which #5 has the
tomorrow-morning deadline (bridged, not resolved, by A1), #4 gates the six prototyped migrations,
and #1, #6, #7 are the ones where the planners disagreed or the doctrine is genuinely open.

One thing this plan adds to that queue: **half of #10's premise is now confirmed from inside the
container.** `main` is branch-protected — the GitHub API returns `"protected": true`, verified
directly this session, not inherited from the workplan. But that is all it establishes. **Protection
being on does not say which checks are required**, and the required set is the actual content of
decision #10. An earlier draft of this section concluded "the blocking level is load-bearing"; that
does not follow, and it converted an open decision into a settled premise — the same move the audit
criticised in four analyses. Retracted, and retracted in `CLAUDE.md` §0 too, where the correction
had reproduced it.

---

## 6. Corrections from the pre-execution adversarial review

The plan was reviewed against the workplan before Wave 1 committed. Three claims it attacked hardest
— A3's nine read-write handles across eight files, A7's exactly-three diverging rows, and the A9/A7
collision — survived independent re-derivation. Four findings did not, and all four were acted on:

1. **A2's caller sweep covered 2 of 8 sites.** The plan scoped the `item_code` grammar fix to the two
   graph extractors on the reasoning that the other narrow matches guarded "different concepts". They
   do not: `schemas/{specification,room,conflict,population,failure_demand_recovery}.py`,
   (the last was named `fdr_specialist.py` on the date of this sweep; renamed 2026-08-15 per DR-2026-07-13 H6)
   `scripts/validate_item.py` and `scripts/convert/convert_spec_db.py` all guard item codes, and all
   rejected the live `A-10b`. `schemas/specification.py` is on the core spine — it would have refused
   a specification for an item its own item schema accepts. Swept in full; `git grep` now returns zero
   narrow sites outside `_archived/`.
2. **`.github/CODEOWNERS:29-30` carried the same false branch-protection claim** and was not in
   Wave 4. Added.
3. **The §5 overclaim above.** Retracted.
4. **`migration_reproducibility.py` fingerprinted the wrong directory** — a live defect in a
   *blocking* gate, found by the workplan §6 in passing and owned by no track. Pulled into Track A
   and fixed: it is a bug, not a retirement, so parking it behind the owner queue would have been
   filing it under the wrong gate.

**Also recorded, not acted on:** six Track A targets sit in CODEOWNERS-protected paths
(`scripts/audit/**`, `governance/check-registry.yaml`, `governance/context-map.yaml`). That is a
review request on the PR, not a bar to executing — `CLAUDE.md` §7 directs sessions to edit the
registry — but the disposition table above should be read with it in mind.

**And declined, with the reason:** `governance/retired-vocabulary.yaml:306` excuses
`verify_resolved_dois.py`'s `/tmp` default by naming a workflow that never runs it. The false
sentence is one line, but the exemption it justifies is bound to owner decision #8 (wire the script,
or archive it), and correcting the rationale without touching the exemption leaves a guard resting on
nothing. Left for the owner with the finding attached, rather than half-fixed.

### 6.1 The rule A6 actually applied

The plan said "`min_items` or an explicit `no_floor` on all 65" without saying which gets which, and
declaring a floor on a legitimately-empty *blocking* check converts it to a blocking FAIL through
`vacuity_failure`. The rule used, recorded so it can be argued with:

- **`min_items`** only where the subject is a corpus whose emptiness could only ever mean *the sweep
  broke* — repo-file sets and registry-derived sets. Four added (`workplan_naming`,
  `pipeline_contract_audit`, `validate_schema_cross_check`, `research_contract_baseline_ratchet`),
  all at **1**, because the failure being caught is a glob resolving to nothing; a floor tuned near
  the live count would instead go red on ordinary churn.
- **`no_floor`** everywhere else, with a **derived** reason, never an invented one:
  `not-instrumented` (38 — prints no `EXAMINED:` line, so no floor is declarable yet),
  `selftest` (12 — subject is its own fixtures), `empty-by-decision` (5 — instrumented, examining
  zero because the corpus was emptied by decision). This follows C7's `unattributed` precedent
  explicitly: writing 55 bespoke justifications in one sitting is how a register fills with plausible
  fiction.

A first pass classified two instrumented checks as already-declared because the substring
`min_items:` appears in `note:` **prose** narrating a floor that was added and retired. Anchored to
the key position and re-run — the same blind-spot shape as the A3 matcher defect, in the tool written
to fix that class of defect.
