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

---

# PART II — Closing out, and getting back to research

**Added 2026-08-02.** Phases 0, 1, 2, 5.1 and 5.3 are done (PR #77). This part is
deliberately about **stopping**, not building. The apparatus is now more elaborate than
the corpus it governs; every further enforcement hour is an hour not spent on the
guidebook.

## The reframe that makes this tractable

`test_db_integrity` — the one blocking red — is **not** an apparatus problem wearing a
content mask. Measured 2026-08-02:

| Sub-check | Rows | Nature |
|---|--:|---|
| `C01` VERIFIED with no audit trail | 7 | content |
| `C02` DOI-bearing, no resolution outcome | 105 | content |
| `C03` COMPLETE with no author | 80 | content |
| `G02` COMPLETE person-authored, no author rows | 113 | content |
| **distinct rows behind C02/C03/G02** | **110** | **content** |
| `B01` out-of-enum `verification_status` | 81 | **stale test** (~80 of 81) |

**Clearing those 110 rows IS research work.** It is source verification under R9/R10 —
re-retrieve the locator, record the outcome, capture the authors. So "resolve everything
so we can get back to research" and "clear the red gate" are the same activity, not
competing ones. That is the single most useful thing in this document.

## Step 1 — Land PR #77 *(unblocked; do first)*

It is green except the pre-existing `test_db_integrity`. Merge it. Waiting for that gate
to go green before merging tooling fixes couples unrelated work — the fixes are what make
the rest of this plan measurable.

## Step 2 — One decision sitting *(~1 hour, unblocks everything else)*

Six decisions, batched. Recommendations given so this is an approval exercise, not a
research exercise.

| # | Decision | Recommendation |
|---|---|---|
| **D1** | Ratify the `verification_status` vocabulary (D-SCHEMA) | **Ratify** `VERIFIED-2`, `DISPUTED`, `VERIFIED-WITH-CORRECTION`, `CLOSED-DECIDED`. `DISPUTED`/`CLOSED-DECIDED` already came from an owner-approved DR; `VERIFIED-WITH-CORRECTION` is already in `schemas/enums.py`. One DR + update `enums.py` and the test list together. **Turns B01/B06 green honestly** and shrinks the red gate to its genuine content half. |
| **D2** | `--deep`'s two divergences | **Widen DR-2026-05-28's exemption list**, scoped to *columns* not whole tables: `evidence_sources`' Crossref enrichment set plus `url_verification_runs`. Same scheduled writers already exempted for two other tables; requiring migrations from a network-bound cron job is impractical. Column-scoping keeps the gate live for everything else in that table. |
| **D3** | What `schemas/*.py` mirrors | **SQLite, for the models in `MODEL_TABLE_MAP` only.** Move or drop the YAML-layer models (`Population`, `Item`) from that map. Decides how much of the 236 is real — probably collapses it to ~9 reconciliation items. |
| **D4** | The 6-slug banner/DB mismatch | **DB is canonical** (CLAUDE.md §2). Update the six banners; `pre_rehab_banner_audit` then becomes a real anti-drift gate rather than a permanent red. |
| **D5** | `sessions/LATEST` | **Point it at the current session** *or* de-scope `citation_mining_session` from session-filtering. Today it is a blocking gate passing on 4.7% coverage. Either fixes it; leaving it is the worst option. |
| **D6** | `schema_reference_drift_audit` | **Retire to `_archived/`.** Its one gating check is carried with better precision by the wired `graph_audit`, and its hit count moved three times in one session purely from prose. |

## Step 3 — Make red mean something *(~2 hours, high leverage)*

The four red advisories are scenery. The fix is the pattern this repo already invented in
`governance/research-contract-baseline.json`: **baseline the count, fail on increase.**

- Add `baseline: <n>` to the registry alongside `level:`.
- `run_checks.py` fails an advisory only when its finding count **exceeds** the baseline.
- Applies to `validate_pydantic_schemas` (236), `population_integrity_audit` (31),
  `pmp_audit` (3), `reasoning_doc_citations_audit` (2), `research_protocol_audit`.

This converts "permanently red, ignore it" into "red means someone made it worse" — which
is the property this whole effort has been trying to buy. It also means the four checks
I added stop being noise without being re-quarantined.

**This is the one piece of new apparatus this document endorses**, because it is what lets
everything else stop.

## Step 4 — Clear the 110 rows *(research work; several sessions)*

Under the research contract, not around it. Per batch:

1. `emit_data_migration` only — never touch the DB directly.
2. **R10 forbids fabricating a resolution outcome.** Each DOI must actually be
   re-retrieved. `NO-MATCH` is a legitimate outcome for pre-DOI-era sources; a guess is not.
3. Note the scheduled resolver **cannot** self-heal these: every phase targets
   `WHERE doi IS NULL`, and Phase-4 author enrichment filters on a `source_type` these
   rows lack. Fixing `source_type` first lets the cron job do the author half.
4. Gate each batch with `research_batch_dod.py --session <id>`.

When this finishes, `test_db_integrity` goes green on its own merits and the blocking red
disappears — without anyone editing a gate to agree with the data.

## Step 5 — Explicitly close the apparatus phase

**Dropped. Not deferred — dropped**, with the reason recorded so a later session does not
rediscover them as gaps:

| Item | Why dropped |
|---|---|
| 3.1/3.2 `parts/` + `site/` freshness checks | `parts/v10` is 13 schema versions stale and `site/` has 116 uncovered files. Adding checks would add two permanent reds to a board this plan is trying to quieten. Record the staleness in the register; regenerate when the render pipeline is next worked on. |
| 3.4 DB write guard in `db.py` | Touches a tool 15 skills depend on. Real risk, low current harm. |
| 4.5 Shared selftest harness | Touches ~18 files for modest gain. |

**Kept, because each is under ~30 lines and closes a stated-but-unverified promise:**

- **3.3 migration immutability** — every migration header promises it, nothing checks it.
- **3.5 `skills/` work-kind** — `skills/**` is in no kind, so a skills-only diff runs
  almost nothing, and two skills already name a path that does not exist.
- **3.6 bot-commit exemption** — record it in `commit_gate.py` where the other exemptions
  live. Currently neither enforced nor exempted, just unexamined.
- **4.4 `EXTRA_RULE_IDS`** → into `references/skill-registry.md` as a declared second
  section, so the rule vocabulary has one home.

## Step 6 — Then stop, and revisit the tool question later

A comparative review (2026-08-02) found this project has hand-rolled equivalents of
**pre-commit** (the check registry), **Alembic/Flyway** (migration checksums), **pytest**
(which exits 5 on zero tests collected — the vacuity guard, built in), and
**betterer/ratchet** (the baseline pattern in Step 3). The opaque SQLite blob is what
creates the need for the reproducibility gate at all; **sqlite-diffable** or **Dolt** would
make drift visible in `git diff` and delete that category of apparatus.

**None of that should be done now.** It is recorded so the next architecture decision is
informed, not so it becomes Phase 6. The correct next move after Step 4 is guidebook
content.

## Definition of done for this whole effort

1. PR #77 merged.
2. Six decisions taken (Step 2).
3. Advisories baselined, so red means regression (Step 3).
4. The 110 rows cleared, so `test_db_integrity` is green on its merits (Step 4).
5. The four kept items landed; the dropped ones recorded as dropped (Step 5).

At that point the board is green-or-meaningfully-red, every check states its authority,
every contract has one source — and there is no apparatus work queued. **That is the exit
condition.**
