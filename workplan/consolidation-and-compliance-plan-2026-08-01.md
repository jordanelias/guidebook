# Consolidation & compliance plan — every contract, every exchange

**Date:** 2026-08-01
**Status:** PROPOSED — owner decisions marked ⚑ block the phases that contain them.
**Scope:** code, CI, hooks, scripts, and the contract documents that govern them. No content, no synthesis.
**Basis:** the contract inventory, boundary map and check-apparatus audits run 2026-08-01
(`references/tooling-register.md` §4.1–§4.4). Every figure below was re-derived directly; none is
carried from prose.

---

## 1. The problem, stated precisely

This project has **~18 contracts** and **57 active checks**. Enforcement is real and substantial.
What is broken is the *map between them*, and it is broken in both directions at once:

| Failure | Evidence |
|---|---|
| A contract criterion names an enforcer that **does not run** | `pipeline-contract.yaml` `register-invariants` → `register_integrity_check.py`, which is quarantined. `pipeline_contract_audit.py:43-46` classifies by **file existence**, so it reports VERIFIABLE. |
| A **blocking check enforces nothing** | `validate_schema.py` prints `No entity files found to validate.` and exits 0. Its `ENTITY_REGISTRY` names six `data/` subdirectories that do not exist. Two registry entries rest on it, one blocking. |
| A contract exists in **two copies that disagree** | R1–R15 lives only in `.claude/settings.json:23` and `research_batch_dod.py:18-86`. R2 says mine `T1-T3` at depth 2-3; the operative rule (`project-standards.md:124`) says **Tier 1-2**. R1 drops Tier 2 from a pass its own source defines as Co-1/**T2**/Co-2. |
| Most checks have **no stated authority** | **51 of 57** active checks trace to no contract criterion — including **26 blocking** ones. |
| Real boundaries have **no contract at all** | `site/` (116 files), `parts/v10/` (stale by 13 schema versions), `.claude/settings.json` (not even syntax-checked), direct DB writers. |

The through-line: **this repo already knows that a fact stated twice will drift** — it is why
`check-registry.yaml` exists and why `commit_gate.py` was extracted. That principle has been
applied to checks and to the commit gates, and to nothing else.

**Organising principle for everything below:**

> One source per fact. Every check declares its authority. Every contract criterion resolves to a
> check that actually runs. Vacuity is detectable.

---

## 2. Phase 0 — Stop the vacuous gates *(no owner decision needed except ⚑0.1)*

These are checks that currently report green while examining nothing. They are worse than absent,
because they are counted as coverage.

**0.1 ⚑ `validate_schema` — decide its fate.** It is blocking and has never validated anything.
Two options, and this is a genuine fork:
- **(a) Point it at reality** — rewrite `ENTITY_REGISTRY` to the corpora that exist
  (`data/decisions/`, `data/adversarial_use/`, `data/doctrine_recheck/`,
  `data/jurisdictional_values/`) against their Pydantic models.
- **(b) Retire it** — the YAML corpora it was written for never materialised; `decision_capture.py`,
  `audit_adversarial_use.py` and `doctrine_recheck.py` already validate three of the four.
*Recommendation: (a) for `jurisdictional_values` only (the one corpus with a real DB counterpart and
no validator), and retire the rest of its registry.* Until decided, demote to `advisory` with the
vacuity recorded — a blocking gate that cannot fail is a false claim of coverage.

**0.2 Add a vacuity guard convention.** Any check that iterates a corpus must report the count it
examined, and `run_checks.py` must treat *"examined 0 items"* as `SKIP`, not `PASS`. This is the
generalisation of three separate findings (`validate_schema`, `validate_item`, `validate_conflicts`,
`claims_docket` with no docket). Implement as an optional `min_items:` field in the registry plus a
convention that checks print `EXAMINED: n`.

**0.3 Fix `check_json.py`'s blind spot.** Its `glob("**/*.json")` skips dot-directories, so
`.claude/settings.json` — which carries R1–R15 and whose corruption silently disables both hooks —
is never parsed. One-line fix; add `.claude/` and `.github/` explicitly.

**0.4 `validate_jurisdiction.py:157-161`** targets `data/sources`, which does not exist, and returns
empty. Same shape as 0.1 at smaller scale — point it at `data/jurisdictional_values/` or drop that
sub-check.

---

## 3. Phase 1 — One source for the research contract ⚑

R1–R15 is the contract the owner declared research **invalid** without. It is the least consolidated
thing in the repo.

**1.1 Create `governance/research-contract.yaml`** — one machine-readable source: `id`, `phase`
(before-admitting / while-searching / when-filing), `rule` text, `anchor` (the
`project-standards.md` RULE or skill section it derives from), and `enforcer` (the
`research_batch_dod.py` check id, or `null`).

**1.2 Generate both consumers from it.** The `SessionStart` hook text and
`research_batch_dod.py`'s rule table both become derived artifacts. Add
`research_contract_sync` to the registry: regenerate and diff, fail on mismatch — the same shape as
the existing `--check` freshness gates. This is the `commit_gate.py` pattern applied to the
contract that matters most.

**1.3 ⚑ Resolve the three live divergences.** These are doctrine questions, not formatting:
- **R2 scope:** hook says `T1-T3`; `project-standards.md:124` says **Tier 1-2**;
  `gap-driven-mining_SKILL.md:75` says "Depth-1 enforced". Three live obligations, mutually
  inconsistent. One must win.
- **R3 locator:** hook says *clause/section/page*; the script and CLAUDE.md say *DOI + page/table*.
  These describe different source classes and may both be right — if so, say so as R3a/R3b.
- **R1 composition:** both copies say Co-1/Co-2; the cited source
  (`multilingual-research_SKILL.md:60`) says Co-1/**T2**/Co-2.

**1.4 Make the `Stop` hook's verdict visible.** It currently runs
`… 2>/dev/null | tail -n 20 || true` — the exit code is discarded by three separate mechanisms. Keep
it non-blocking (that is deliberate), but surface PASS/FAIL rather than swallowing it.

---

## 4. Phase 2 — Join the contract to the registry

This is the core consolidation: make "compliance" mechanically checkable in both directions.

**2.1 `pipeline_contract_audit.py` must consult the registry, not the filesystem.** Replace
`classify_check`'s `path.exists()` with a lookup into `check-registry.yaml`, yielding
`ACTIVE / QUARANTINED / UNREGISTERED / NONE`. This alone converts `register-invariants` from
phantom-VERIFIABLE to correctly-QUARANTINED. **~10 lines; highest value-per-line in this plan.**

**2.2 Contract criteria reference check *ids*, not script paths.** A path is an implementation
detail that a rename breaks silently; an id is the registry's primary key and is selftested for
existence.

**2.3 Add `basis:` to every registry entry.** One field naming the authority a check enforces:
a contract criterion id, a DR, a `project-standards.md` RULE, or the literal `hygiene` for
UTF-8/JSON/YAML parsing. Then extend `run_checks.py --selftest` with two assertions:
- every check has a `basis`, and non-`hygiene` bases resolve to a real criterion/DR/RULE;
- every contract criterion resolves to an active check, or carries an explicit `unenforced:` reason.

This is the mechanism that makes the user's question — *"is every contract complied with?"* —
answerable by running one command. 57 entries to populate: mechanical, and the act of populating it
is itself the audit.

**2.4 Expand the pipeline contract to cover the 26 unbacked blocking checks**, or — more honestly —
accept that most are hygiene and let `basis: hygiene` absorb them. Do **not** write contract prose
to justify a UTF-8 check.

---

## 5. Phase 3 — Close the unchecked boundaries

Ordered by cost-before-anyone-notices.

**3.1 Derived-output freshness.** `parts/v10/` carries fingerprint `3d7fb5d50de6`; the live DB
fingerprints `b015d2e84025` (built at `user_version` 25, now 38). Add `--check` to
`generate_parts.py` and `regenerate_vetting_surface.py`, mirroring the existing
`pipeline_completeness.py --check` pattern, and register both. **Expect `parts` to land RED** — it
genuinely is stale; that is the point.

**3.2 `site/` — 116 generated files, zero coverage.** `site/**` is a declared `render` kind with no
check behind it. Minimum viable: a manifest + fingerprint check, same pattern as 3.1.

**3.3 Migration immutability.** Every migration header promises it is *"immutable once committed"*,
and nothing verifies it: no script re-hashes `scripts/migrations/data_*.sql` against
`data_migrations.content_sha`. Add a direct check — cheap, stdlib, and it makes the deep
comparison's incidental detection redundant. Also validate `BASELINE_DATA_CUTOFF_TS`
(`migrate_db.py:111`) against the highest baseline on disk.

**3.4 ⚑ Guard the canonical DB at the point of writing.** `scripts/db.py` defaults to the canonical
path, commits directly, and **15 skills point at it**. `item_audit_pipeline.py` runs four
`DELETE FROM` statements against it. The correct pattern already exists in exactly one place —
`assess_cell.py:445` refuses the canonical path. Propose: make refusal the default for write paths,
with an explicit `--i-am-a-migration` escape. This is behaviour change to a tool 15 skills depend
on, so it is owner-gated.

**3.5 `skills/**` belongs to no work kind.** A skills-only diff triggers only `always` checks, and
nothing resolves the script paths skills name — two of which are already broken
(`scripts/db/migrate_all.py` targets a non-existent `data/db/guidebook.db`). Add a `skills` kind and
a reference-resolution check.

**3.6 Bot commits and the commit contract.** Three workflows push messages that carry neither the
canonical shape nor a doctrine token, and the two DB-writing workflows push a mutated
`data/guidebook.db` to `main` **without running any battery first**. Either bring their messages
into the contract or record the exemption in `commit_gate.py` where the other exemptions live —
currently it is neither enforced nor exempted, just unexamined.

**3.7 Entity YAML ↔ DB.** `data/decisions/decision_register.yaml` holds **156** decisions; the
`decisions` table holds **0**. CLAUDE.md already calls the table "empty scaffolding", so the drift
is known — but nothing asserts the intended direction. Either reconcile or record `decisions` as
YAML-canonical and drop the table.

---

## 6. Phase 4 — Deduplicate the mechanics

**4.1 Retire the second commit regex.** `validate_commits.py` carries a divergent format regex and
three rotted allowlists. Quarantined, so harmless — but it is a second definition of the repo's
most-restated contract. Repair to consume `commit_gate.py` + `check_commit_msg.PATTERN`, or retire ⚑.

**4.2 Single marker map.** ●/◐/○ is defined in `tier-system.md` §5, restated in
`project-standards.md:26` *with an extra clause*, and again in `CLAUDE.md:194-197` — which itself
flags that `mission-and-epistemics.md` still carries a superseded **two**-marker scheme. Reconcile
the doctrine drift ⚑, then have one source and cross-references.

**4.3 Exemption lists.** `EXEMPT_TABLES` (2 entries) is authoritative but incomplete —
`evidence_sources` and `url_verification_runs` are written by the same scheduled jobs and were never
added. This is the ⚑ owner decision already surfaced by `--deep`.

**4.4 Rule-identifier vocabulary.** `rules_in_scope` validates against the skill registry **∪**
`EXTRA_RULE_IDS`, a hardcoded set inside `adherence_log_audit.py:84-104`, while
`attestation.schema.json:18` points only at the registry — a third, incomplete statement. Move
`EXTRA_RULE_IDS` into `references/skill-registry.md` as a declared second section.

**4.5 Shared selftest harness.** 18 scripts implement `--selftest`; 7 define their own `check()`.
Low priority, mechanical, and worth doing *last* — it touches many files for modest gain.

---

## 7. Phase 5 — Cost and noise

**5.1 Fold the double rebuild.** `migration_reproducibility` and `…_deep` each run a full
`migrate_db.py --rebuild`: **66.1s of the board's 109.7s (60%)**. The deep comparison is a strict
superset. Make the script emit both verdicts from one rebuild and have the registry select which to
gate on, or let the deep check reuse a cached rebuild via `--rebuilt-from`.

**5.2 ⚑ The four red advisories are on the clock.** `migration_reproducibility_deep`,
`validate_pydantic_schemas`, `pmp_audit`, `reasoning_doc_citations_audit` were landed to make
invisible failures visible. If their owner decisions are not taken, re-quarantine them: a check
nobody can act on is noise, and this project's own thesis is that a normalised red board is how the
next real failure gets missed.

**5.3 CODEOWNERS gaps.** Three contract-bearing paths are unprotected: `.claude/settings.json`
(carries R1–R15), `references/project-standards.md` (119 RULE blocks, the operative ledger), and
`scripts/ci_helpers/` (the commit gates). Adding them is one line each ⚑.

---

## 8. Sequencing and verification

**Order:** Phase 0 → 2 → 1 → 3 → 4 → 5. Phase 2 before Phase 1 because `basis:` is the frame that
makes the research-contract work checkable rather than merely tidy. Phase 0 first because a vacuous
blocking gate corrupts every coverage claim made after it.

**Each phase verifies the same way**, per `references/tooling-register.md` §7:
1. `python3 scripts/run_checks.py --selftest`
2. `scripts/preflight.sh` on the diff; `--all` before merge
3. New checks land **advisory**, promoted in a separate commit
4. Every new check gets a selftest case **written from a reproduction**, then mutation-tested
   against the pre-fix code — the 2026-08-01 lesson was that four defects survived a selftest with
   six passing cases
5. Re-derive, never re-cite: every figure in this plan is re-computable, and several counts in the
   record were falsified within an hour of being written

**Definition of done for the whole effort:** `run_checks.py --selftest` answers *"does every contract
have a live enforcer, and does every enforcer have a stated authority?"* — and fails when it does not.

---

## 9. Owner decisions ⚑, collected

| # | Decision | Blocks |
|---|---|---|
| 0.1 | `validate_schema`: repoint or retire | Phase 0 |
| 1.3 | R2 tier scope / R3 locator class / R1 pass composition | Phase 1 |
| 3.4 | Make `scripts/db.py` refuse the canonical path by default | 3.4 only |
| 4.1 | Retire `validate_commits.py` | 4.1 only |
| 4.2 | Reconcile the two-marker scheme in `mission-and-epistemics.md` | 4.2 only |
| 4.3 | Widen DR-2026-05-28 exemptions, or require migrations from the jobs | 4.3, 5.1 |
| 5.2 | Take the four advisory decisions, or re-quarantine | 5.2 |
| 5.3 | Extend CODEOWNERS to the three unprotected contract paths | 5.3 |

Nothing in Phases 0.2–0.4, 2, 3.1–3.3, 3.5, 5.1 requires an owner decision.
