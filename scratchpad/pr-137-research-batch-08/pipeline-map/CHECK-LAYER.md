# Check layer map — `governance/check-registry.yaml` / `scripts/run_checks.py`

**Method.** Read `CLAUDE.md` in full first. Ran, on the live repo, today (2026-09-16), at commit
`be85a941`:

```
bash .claude/hooks/ensure-deps.sh                                   # exit 0, pydantic 2.13.5 / jsonschema 4.26.0 already present
python3 scripts/run_checks.py --list  > .../run_checks_list.txt
python3 scripts/run_checks.py --all --explain > .../run_checks_all.txt
python3 scripts/run_checks.py --selftest > .../run_checks_selftest.txt
```
then, because `--all` only prints the tail of a check's own output (full body for FAIL/ERROR,
last line only for NONE/SKIP, nothing at all for PASS), ran every one of the 70 active checks
**individually** with `GUIDEBOOK_DB_PATH=data/guidebook.db` to capture its full stdout and its own
`EXAMINED:` line, so the table below is not missing a single check's subject count. Read-only
throughout: no script, no registry line and no DB byte was touched except this report file.
`data/guidebook.db` was opened read-only via `?mode=ro` for every direct query in this file.

Two related read-only maps already exist alongside this one in this same PR folder —
`EXECUTABLE-SURFACE.md` (which checks exist and who calls them) and `PROVENANCE-CENSUS.md` (what
provenance defects checks did/didn't catch) — written earlier in this session by other passes. They
predate several registry additions (that map counted "63 active + 4 quarantined"; live today is
**70 active + 5 quarantined** — `extraction_relations_integrity`, `derived_not_curated_audit`,
`identifier_floor_audit`, `source_locators_integrity`, `derivation_handshake_integrity`,
`medical_lens_integrity` are new, and `register_integrity_check` was newly quarantined 2026-09-11).
Where they corroborate a finding here, it's cited; where they're stale relative to today's live
run, that's noted rather than trusted.

---

## 0. Headline numbers, derived today

- **70 active checks, 5 quarantined/retired** (`--list`, `--selftest` C1/C1b).
- `--all`: **45 green, 15 NOTHING-IN-SCOPE, 10 advisory failures, 0 blocking failures → RESULT: PASS**.
- **7 BLOCKING checks are vacuous today** (named explicitly by `run_checks.py`'s own summary line):
  `source_slug_links_duplicates`, `citation_mining_session`, `validate_evidence_state`,
  `validate_verification_consistency`, `attestation_presence`, `attestation_schema`,
  `extraction_relations_integrity`. **All seven are "waiting for data," not dead** — see §2.
- **21 of 70 checks declare `basis: unattributed`** (no stated authority) — selftest C8's own count,
  reproduced independently in §5.
- **7 of 34 contract criteria have no check claiming them** in `basis:` — selftest C7's own count
  — but 2 of those 7 already have a live enforcer per the *contract's own* `check:` field that the
  registry's `basis:` simply omits, so the true unenforced count is **5, not 7**. See §4.
- **0 checks have a `basis:` pointing at a criterion no contract stage declares** — selftest C7
  passed clean (`dangling` list was empty). This is a real zero, not an omission.
- **32+ hand-written "N today" figures live in the registry's own prose notes** (CLAUDE.md rule 8's
  named violation). Of the ones checked against a live re-run: **9 are still exactly correct, 12 are
  stale**, and one (`migration_reproducibility`) describes a comparison mechanism the code no longer
  uses at all. Full ledger in §7.
- **One check (`site_pages_fresh`) is not merely corpus-empty but latently broken**: the generator
  it drives queries two columns (`specifications.item_code`, `specifications.population_code`) that
  migration 071 dropped from the live schema. See §3 — this is the one genuinely "vacuous by
  construction" finding in the registry today.

---

## 1. Full inventory — all 70 active checks

Columns: `basis` is the registry's `basis:` field verbatim (a pipeline-contract `stage/criterion`
ref, the literal `hygiene`, or `unattributed`). `floor` is `min_items=N` or `no_floor` exactly as
declared. `verdict today` and `EXAMINED today` were captured by running the check directly against
the live DB/repo, not copied from the registry's notes.

| id | level | battery | basis | floor | verdict today | EXAMINED today |
|---|---|---|---|---|---|---|
| `check_utf8_md` | blocking | syntax | hygiene | min_items=1000 | PASS | 1392 .md file(s) |
| `check_json` | blocking | syntax | hygiene | min_items=50 | PASS | 311 .json file(s) |
| `check_yaml` | blocking | syntax | hygiene | min_items=20 | PASS | 45 .yaml/.yml file(s) |
| `validate_bpc` | blocking | structure | hygiene | min_items=1 | PASS | 102 |
| `validate_cross_refs` | blocking | structure | hygiene | no_floor | PASS | not printed (declared no_floor: not-instrumented — multi-subject, see registry note) |
| `test_db_integrity` | blocking | db_integrity | unattributed | min_items=1 | PASS | 1788 subject-inspections across 15 of 71 sub-checks instrumented; the script itself lists 56 of its 71 sub-checks as "PASSED HAVING EXAMINED NOTHING" — self-reported, not hidden |
| `migration_reproducibility` | blocking | data | cross_stage/reproducibility-invariant | min_items=1 | PASS | 76 (schema_version + ALL 75 user tables' COUNT(\*), not "7" — see §7) |
| `migration_reproducibility_deep` | advisory | data | cross_stage/reproducibility-invariant | min_items=1 | PASS | 77 (75 identical + 2 exempt) |
| `source_slug_links_duplicates` | blocking | data | unattributed | no_floor | **NONE** | 0 source_slug_links row(s) — table emptied by the 2026-09-13 circulation clear |
| `validate_parameters` | advisory | data | base/base-parameter-vocabulary | min_items=1 | FAIL (vacuity guard) | 0 — `base_parameters` has no rows yet (no `add-parameter` call since the clear) |
| `readonly_db_open_audit` | advisory | data | unattributed | min_items=1 | PASS | 39 |
| `db_path_env_audit` | blocking | data | unattributed | min_items=1 | PASS | 52 |
| `alias_provenance_audit` | blocking | data | unattributed | min_items=1 | PASS | 2382 |
| `citation_mining_session` | blocking | data | unattributed | no_floor | **NONE** | 0 — session `session_2026-09-10-...` logged no slug-linked Tier 1-2 sources |
| `citation_mining_backlog_t2` | informational | data | unattributed | no_floor | **NONE** | 0 — repo-wide backlog also empty |
| `claude_md_spine` | blocking | governance | base/base-names-resolve | min_items=1 | PASS | 7 contract stage(s) vs 1 SPINE line |
| `schema_reference_audit` | blocking | schema | base/base-names-resolve | min_items=1 | PASS | 935 SQL identifier refs in 238 files vs 98 live tables/views |
| `validate_schema_cross_check` | advisory | schema | base/base-schema-validates | min_items=1 | PASS | 83 (0 entity files + 83 cross-check subjects) |
| `validate_evidence_state` | blocking | schema | specification/governing-refs-nonempty; specification/no-regulatory-stratum-stated; specification/tier3-alone-threshold | no_floor | **NONE** | 0 — `specifications` has 0 rows |
| `validate_population` | advisory | schema | base/base-population-vocabulary | min_items=1 | PASS | 114 |
| `validate_jurisdiction` | blocking | schema | base/base-jurisdiction-vocabulary | min_items=1 | PASS | 111 |
| `validate_axes` | blocking | schema | base/base-demand-vocabulary | min_items=1 | PASS | 74 (`population_axis_map` 53 + `access_need_axis_map` 21) |
| `validate_verification_consistency` | blocking | schema | unattributed | no_floor | **NONE** | 0 — `specifications` has 0 rows |
| `audit_evidence_metadata` | advisory | schema | unattributed | min_items=1 | PASS | 106 |
| `validate_pydantic_schemas` | advisory | schema | unattributed | min_items=1 | FAIL | 20 model↔table pairs, 239 drift findings (informational) |
| `audit_adversarial_use` | blocking | governance | unattributed | min_items=1 | PASS | 9 |
| `author_fidelity` | advisory | research | DR-2026-08-19 §7 adversarial pass, lens L1 | min_items=1 | FAIL (INDETERMINATE) | 0 of 0 `evidence_sources` rows carry a DOI — network unreachable in this sandbox, not a DB finding |
| `decision_capture` | blocking | governance | unattributed | no_floor | PASS | not printed (not-instrumented, multi-subject); C9 reports **51** orphan DRs live (registry says 49) |
| `doctrine_recheck` | blocking | governance | cross_stage/doctrine-recheck | no_floor | PASS | not printed (not-instrumented); live snapshot **11 CANONICAL govs / 8 CANONICAL rules / 185 ACTIVE decisions / 102 BPC files** (registry says 11/8/158/102) |
| `retired_vocabulary` | advisory | governance | base/base-retired-vocabulary-not-taught | min_items=1 | FAIL | 26 register entries + 0 dead exemptions, 62 live occurrences found |
| `matrix_consistency` | advisory | governance | render/mode-stratum-matrix-consistency | min_items=1 | PASS | 10 |
| `pipeline_contract_audit` | advisory | governance | unattributed | min_items=1 | PASS | 34 contract criteria (broken=0, quarantined=0, unregistered=0, incomplete=6, verifiable=28) |
| `claims_docket` | advisory | governance | cross_stage/definition-of-done | min_items=1 | PASS | 68 |
| `attestation_presence` | blocking | attestation | cross_stage/adherence-log | no_floor | **NONE** | 0 — diff-scoped to HEAD~1..HEAD; today's last commit touched no synthesis path |
| `attestation_schema` | blocking | attestation | cross_stage/adherence-log | no_floor | **NONE** | 0 — same, diff-scoped |
| `attestation_evidence` | advisory | attestation | cross_stage/adherence-log | no_floor | PASS | not printed (not-instrumented — bundles a 0-today diff subject with the 127 attestations on disk) |
| `attestation_verdict` | informational | attestation | cross_stage/adherence-log | no_floor | **NONE** | 0 — diff-scoped |
| `research_contract_baseline_ratchet` | blocking | research | hygiene | min_items=1 | PASS | 5 |
| `research_contract_sync` | blocking | research | hygiene | min_items=10 | PASS | 64 contract line(s) |
| `research_dod_selftest` | blocking | research | unattributed | no_floor | PASS | selftest, fixture-based — "gate rejected the corpus AND all 19 seeded rules fired" |
| `research_dod` | advisory | research | unattributed | no_floor | FAIL | not printed (not-instrumented); R9a/R9b explicitly report NOTHING-IN-SCOPE, 3 rules unmet overall |
| `research_protocol_audit` | advisory | research | research/adversarial-fields-complete | no_floor | PASS | 8 |
| `metadata_integrity_audit` | advisory | research | evidence/evidence-verification-gate | no_floor | **NONE** | 0 |
| `gap_mining_audit` | advisory | research | unattributed | no_floor | PASS | 8 (`gaps` 8 + `gap_mining` 0 — see §7, the registry note claims the subject is `gap_mining` alone, which would be 0) |
| `population_integrity_audit` | advisory | research | base/base-population-vocabulary | no_floor | **NONE** | 0 |
| `graph_audit` | advisory | research | unattributed | min_items=1 | PASS | 682 |
| `validate_reasoning` | advisory | research | synthesis/nine-step-synthesis | min_items=1 | FAIL | 3 (1 doc with structural errors, 2 skipped as templates) |
| `pmp_audit` | advisory | research | research/pmp-strict-termination | no_floor | **NONE** | 0 |
| `reasoning_doc_citations_audit` | advisory | research | unattributed | no_floor | **NONE** | 0 |
| `test_graph_audit` | advisory | tests | hygiene | no_floor | PASS | selftest, fixture-based |
| `test_pipeline_contract` | advisory | tests | hygiene | no_floor | PASS | selftest, fixture-based |
| `test_record_command_session` | advisory | tests | hygiene | no_floor | PASS | 15 assertion(s) |
| `test_url_verifier` | advisory | tests | hygiene | no_floor | PASS | selftest, fixture-based, 25/25 tests |
| `test_verification_pipeline` | advisory | tests | hygiene | no_floor | FAIL | selftest, fixture-based, 15/18 tests (3 failures include a live-`pipeline_runs` metrics check) |
| `test_assess_cell_pilot` | advisory | tests | hygiene | no_floor | PASS | selftest, fixture-based |
| `test_evidence_cell_state_2_3` | advisory | tests | hygiene | no_floor | PASS | selftest, fixture-based |
| `test_validate_evidence_state_2_4` | advisory | tests | hygiene | no_floor | PASS | selftest, fixture-based |
| `test_directness_2_2` | advisory | tests | hygiene | no_floor | FAIL | selftest + 1 live-DB smoke subject (0 `evidence_population_match` rows — corpus-empty, not a logic failure) |
| `pipeline_completeness_fresh` | blocking | render | unattributed | no_floor | PASS | not printed (declared not-instrumented — multi-metric dashboard) |
| `evidentiary_audit_fresh` | blocking | render | unattributed | min_items=1 | PASS | 80 |
| `context_map_fresh` | advisory | render | render/render-freshness | min_items=1 | PASS | 1 context map (1475 lines) |
| `site_pages_fresh` | advisory | render | render/render-freshness | min_items=1 | **FAIL (vacuity guard)** | 0 — see §3, latent break, not just an empty corpus |
| `render_audit_browser` | advisory | render | unattributed | min_items=1 | PASS | 1 |
| `judgment_handoff_shape` | blocking | schema | judgment/handoff-fanout-preserved | min_items=1 | PASS | 3 invariant(s) |
| `extraction_relations_integrity` | blocking | db_integrity | judgment/figure-role-stated | no_floor | **NONE** | 0 — extraction/relation/derived-figure rows all 0, cleared 2026-09-13 |
| `derived_not_curated_audit` | blocking | schema | base/base-derived-not-curated | min_items=1 | PASS | 5 argparse `choices=` literals checked against 94 live CHECK vocabularies |
| `identifier_floor_audit` | blocking | db_integrity | base/base-identifier-never-reissued | min_items=1 | PASS | 3 identifier floors vs 85 committed migration files |
| `source_locators_integrity` | advisory | data | evidence/locator-title-matches-identifier | min_items=1 | FAIL | 550 title-bearing rows, 31 mismatched, 17 unprovable — repair is blocked on a missing writer, not a decision |
| `derivation_handshake_integrity` | advisory | schema | specification/derivation-handshake | no_floor | **NONE** | 0 — `specifications` 0 rows (VERDICT: CLEAN, its own text: "NOT a check with nothing to say... the corpus state") |
| `medical_lens_integrity` | advisory | schema | base/base-medical-lens-offered-not-adopted | no_floor | **NONE** | 0 — `base_taxonomy_medical` 0 rows (VERDICT: CLEAN, an "unwritten vocabulary," per its own text) |

---

## 2. The 7 BLOCKING-and-vacuous checks — all "waiting for data," none dead

`run_checks.py --all`'s own summary names these seven. Classifying each against the live schema
(CLAUDE.md §4's unwritable-table derivation was run against the live DB to confirm):

| id | empty table(s) | why it's empty | can it refill without new code? |
|---|---|---|---|
| `source_slug_links_duplicates` | `source_slug_links` | 2026-09-13 circulation clear | **Yes** — normal cross-filing writes it |
| `citation_mining_session` | (session-scoped, not table-scoped) | `sessions/LATEST-RESEARCH` names a session that logged no Tier 1-2 sources | **Yes** — the very next research batch that logs a T1-2 source gives it a subject |
| `validate_evidence_state` | `specifications` | 2026-09-13 clear + `parameter_id NOT NULL` FK into empty `base_parameters` | **Yes, but gated**: needs one `db.py add-parameter` call first (confirmed live — `base_parameters` itself has no dead FK into anything; it's the next write in the chain, not blocked) |
| `validate_verification_consistency` | `specifications` | same as above | Same as above |
| `attestation_presence` | (diff-scoped to HEAD~1..HEAD) | today's last commit (`be85a941`, verified via `git diff --stat HEAD~1 HEAD`) touched no synthesis path | **Yes, trivially** — the next commit that touches `references/bpc-reasoning/`, `decisions/`, `sessions/` etc. gives it a subject. This is working exactly as its no_floor reason describes: "a commit that never touches [synthesis paths] legitimately has nothing for it to examine." |
| `attestation_schema` | same diff-scope | same | same |
| `extraction_relations_integrity` | `extraction_relations`, `extraction_population_links`, derived-figure rows | 2026-09-13 circulation clear; registry's own note says "RATCHET BACK TO min_items 1 when the re-run lands its first extraction" | **Yes** — `db.py add-extraction` is a live writer |

**None of the seven is dead.** Every one is either (a) a table the 2026-09-13 circulation clear
emptied and a normal writer can refill, (b) a session/diff-scoped check correctly reporting "not in
this one's scope" rather than a corpus state, or (c) one write (`add-parameter`) away from having a
subject. This matches the task brief's expected shape and CLAUDE.md's own framing of the clear.

Live confirmation that the write path is intact (CLAUDE.md §4's own derivation script, run read-only
against `data/guidebook.db`): `specifications.parameter_id -> empty table` is the only relevant
dead-FK entry on the determination path, and `base_parameters` itself has none — i.e. minting a
parameter is unblocked. (The same query also reproduces CLAUDE.md's other named unwritable
tables — `item_taxonomy_links.item_code -> empty table`, etc. — confirming the derivation command in
CLAUDE.md §4 still runs clean against the live schema.)

---

## 3. The one check that is vacuous BY CONSTRUCTION: `site_pages_fresh`

This is the one finding in this map that is not "waiting for a batch" but **latently broken against
the current schema**, hiding behind an empty table.

- `site_pages_fresh` runs `scripts/generate/build_site.py --check` (registry line ~1355-1374,
  `min_items: 1`). Its floor's justification (`governance/check-registry.yaml:1367-1368`):
  > "EXAMINED prints len(rows), the page count built from `items` (93 today)... **items is populated
  > repo content (CLAUDE.md §1), not a corpus that legitimately empties.**"
- That premise is false today. `PRAGMA table_info`/`SELECT COUNT(*) FROM items` on the live DB
  returns **0 rows** — exactly what CLAUDE.md §7's own trap bullet says ("THE ITEM LAYER IS GONE FROM
  THE DATABASE... `items` holds 0 rows and a rebuild does not restore it") and what the 2026-08-26
  owner ruling in CLAUDE.md §6 describes: `items` is being demoted from identity table to a
  **Part-4 render aggregate derived from `specifications`**, not an independently-populated source.
  So `items` is not "corpus that legitimately empties" in the ordinary batch-landed-zero-rows sense;
  it is a table the architecture no longer writes directly at all.
- Worse: `build_site.py`'s `build_specs()` (`scripts/generate/build_site.py:122`) imports
  `spec_page.py` and, for every `items` row, calls `spec_page.query_item()`
  (`scripts/generate/spec_page.py:73-78`):
  ```python
  cells = conn.execute(
      "SELECT specification_id, population_code, state, tier_basis, code_floor_only, "
      "falsification_condition, regulatory_stratum_only, confidence_synthesis_basis, "
      "has_unverified_sources, all_sources_disqualified "
      "FROM specifications WHERE item_code = ? ORDER BY population_code",
      (item_code,),
  ).fetchall()
  ```
  Both `item_code` and `population_code` are columns migration 071 **dropped** from `specifications`
  — confirmed directly: `PRAGMA table_info(specifications)` on the live DB lists neither column.
  `build_site.py`'s own `governing_refs()` (line ~93) makes the identical `item_code` join.
- `build_site.py` already documents having hit this exact failure once and fixed it **for a
  different generator**: its own docstring (`scripts/generate/build_site.py:6-9`) says
  `population_page.py` "was DELETED 2026-09-11 — it raised `no such column: item_code` against the
  live DB and had no caller." `spec_page.py` has the same defect and **does** have a live caller
  (`site_pages_fresh`), and was not fixed alongside it.
- Because `build_specs()` wraps the per-item call in `try/except Exception` and *excludes* any
  failed item from its return value rather than aborting, the failure mode the day `items` regains
  even one row is not a crash `run_checks.py` would see as ERROR — it is an `ERROR:` line to stderr
  for that one item, silently dropped from both the staleness list and the orphan-page list, and
  `--check` would still print `FRESH: N page(s) match a fresh render` and **exit 0**. That is
  CLAUDE.md §5(a)'s failure mode in a new shape: not "passed having examined nothing" but "passed
  having silently excluded the one subject that broke."
- Independent corroboration: this session's sibling map `PROVENANCE-CENSUS.md` row for
  2026-09-10 (class `f`) already names the same defect from a different angle: *"7 live readers
  (`check_rendered_docs.py`, `build_site.py`, `pilot_renderings.py`, `spec_page.py`,
  `population_page.py`, a skill doc) still select `specifications.item_code`... **Unrepaired at
  record date**."* (`population_page.py` has since been deleted per `build_site.py`'s docstring;
  `spec_page.py` has not.)

**This is why the task brief's distinction matters here**: `site_pages_fresh`'s `[FAIL]` today reads
identically to the seven "waiting for data" cases in §2 (a vacuity-guard message, `EXAMINED: 0`), but
unlike them, landing a batch does **not** fix it — it hands the check a code path that throws. The
fix is a code fix to `spec_page.py`/`build_site.py` (repoint the query at `parameter_id`/the current
lens columns), not a data batch.

No other check was found with the same shape. `evidentiary_audit_fresh` and `pipeline_completeness_fresh`
were checked for the identical pattern (`grep -n item_code\|population_code`): `evidentiary_audit_fresh`
reads `items.item_code` only (that column is intact — `items` itself wasn't restructured, only
emptied) and never joins `specifications` on it; `pipeline_completeness_fresh`'s own comment
(`tools/pipeline_completeness.py:202-206`) shows it was **already repaired** post-071 to read
`specifications.identity_code` instead and report `judged=None`/`pop_breadth=None` ("not derivable
rather than zero") — the right pattern, and a working contrast to `spec_page.py`.

---

## 4. Contract criteria no check claims — 7 named, 5 real

`--selftest` C7 prints, verbatim:

```
[INFO] contract criteria with no check claiming them: 7 of 34
         cross_stage/attestation-doctrine-binding
         evidence/discovery-provenance
         judgment/comparator-recorded
         judgment/convergence-independence
         render/register-invariants
         specification/no-diagnosis-only-determination
         synthesis/opus-routing
```

C7 computes "claimed" purely from `check-registry.yaml`'s `basis:` field. But
`governance/pipeline-contract.yaml` carries its *own*, separate `check:` pointer on every criterion,
and it is not cross-checked against the registry's `basis:` by any test. Reading it directly:

| criterion | contract's own `check:` field |
|---|---|
| `evidence/discovery-provenance` | `null` — genuinely unenforced (its own text explains why: the two candidate columns are unreachable by any writer, by design, pending a dual-home decision) |
| `judgment/convergence-independence` | `null` — genuinely unenforced (own text: root-count substrate exists, "gained its first writer 2026-09-10," no gate yet) |
| `judgment/comparator-recorded` | `null` — genuinely unenforced |
| `synthesis/opus-routing` | `null` — genuinely unenforced (no mechanical way to verify which model authored a row) |
| `render/register-invariants` | `null` — genuinely unenforced, and says so in its own text: "UNENFORCED SINCE 2026-09-11... `register_integrity_check` enforced this... [now quarantined]" |
| `specification/no-diagnosis-only-determination` | **`scripts/audit/medical_lens_integrity.py`** |
| `cross_stage/attestation-doctrine-binding` | **`scripts/audit/adherence_log_audit.py`** |

The last two **are** live, registered, active checks (`medical_lens_integrity`,
`attestation_presence`/`attestation_schema`/etc. — all backed by `adherence_log_audit.py`). Verified
`medical_lens_integrity.py` directly enforces the no-diagnosis-only rule
(`scripts/audit/medical_lens_integrity.py:86-90`):
```python
"SELECT specification_id FROM specifications "
"WHERE medical_code IS NOT NULL AND identity_code IS NULL "
"AND icf_code IS NULL AND needs_code IS NULL"
```
— exactly "no determination is keyed on medical_code alone." But `check-registry.yaml`'s
`medical_lens_integrity` entry declares `basis: base/base-medical-lens-offered-not-adopted` only
(a single string, not a list), omitting `specification/no-diagnosis-only-determination` even though
the same script enforces both and the contract's own `check:` field says so for both. Same shape for
`attestation-doctrine-binding` vs. the `attestation_presence`/`attestation_schema`/etc. checks, whose
registry `basis:` cites only the more general `cross_stage/adherence-log`.

**So the honest count is: 5 of 34 contract criteria have no enforcer anywhere (a real gap), and 2 of
the 7 the selftest flags are a `check-registry.yaml` `basis:` under-declaration** — the fix is a
one-line registry change (`basis: [existing, specification/no-diagnosis-only-determination]`, list
form, exactly as `validate_evidence_state` already does with three), not new code. This is itself an
instance of CLAUDE.md rule 8 ("a list that drifts from the thing it describes") living inside the
governance apparatus's own cross-reference mechanism.

**Zero checks have a `basis:` pointing at a criterion no contract stage declares** — selftest C7's
`dangling` check passed with an empty list. Checked directly; this is a genuine zero, not an
unexamined claim.

---

## 5. Checks with no stated authority (`basis: unattributed`) — 21 of 70

Selftest's own count (`[INFO] checks with no stated authority: 21 of 70`), reproduced independently
by parsing the registry:

`test_db_integrity`, `source_slug_links_duplicates`, `readonly_db_open_audit`, `db_path_env_audit`,
`alias_provenance_audit`, `citation_mining_session`, `citation_mining_backlog_t2`,
`validate_verification_consistency`, `audit_evidence_metadata`, `validate_pydantic_schemas`,
`audit_adversarial_use`, `decision_capture`, `pipeline_contract_audit`, `research_dod_selftest`,
`research_dod`, `gap_mining_audit`, `graph_audit`, `reasoning_doc_citations_audit`,
`pipeline_completeness_fresh`, `evidentiary_audit_fresh`, `render_audit_browser`.

Per `run_checks.py`'s own comment (`scripts/run_checks.py:736-740`), `unattributed` is a deliberate,
counted, allowed state — "forbidding it would have meant inventing authorities for 29 checks in one
sitting" — not a defect by itself. It is listed here per the task brief, not flagged as broken.

---

## 6. Quarantine — 5 entries, promotion clauses checked for fireability

| id | status | promotion clause | can it ever fire? |
|---|---|---|---|
| `register_integrity_check` | quarantined 2026-09-11 | "a live render surface keyed on parameter_id × lens" — does not exist yet; `parts/`/`site/` hold no determination rows | **Yes, eventually** — waits on the render stage catching up to the specification stage, a real but distant future state, not an impossibility. Its own entry proves the mechanism works (mutation-tested against all 8 tampering scenarios) — it went red the moment it had its first real subject (a 1×MOB determination), which is the entry's own point: a 0-row object is unproven, not clean. |
| `validate_db` | retired 2026-08-15 | none — permanently archived, superseded by `test_db_integrity` (72 checks vs 9) | N/A by design; not a stuck promotion, a closed one. One finding (31 zero-target connections) is preserved in the entry text so archiving didn't bury it. |
| `adjudication_integrity` | quarantined | waits on owner ruling **OD-E** | **Mechanically unblocked already** — OD-E was ruled 2026-08-31 (D-0179), its subject `REF-00967` holds 0 rows today, and the entry says outright "nothing mechanical blocks promotion and it is an owner call only." This is the one quarantine entry ready to fire on a human decision alone. |
| `code_currency_audit` | quarantined | **none stated** — reason is just "RED. Flags standards lacking a currency marker; a content backlog, not a gate." | **No defined path at all.** Unlike the other three, this entry names no condition under which it would be promoted; it argues the check should never become a gate, which is a different thing from a promotion clause that can't fire — but per the task's literal question ("whose promotion clause can never fire"), this is the one with nothing to fire. |
| `pre_rehab_banner_audit` | quarantined | "an owner call on which side is canonical" for a real, named 6-slug drift | **Yes** — concrete, resolvable the moment the owner picks a side; the entry already explains this becomes "a genuine, permanently-meaningful anti-drift gate" once ruled. |

Only `code_currency_audit` has no fireable promotion condition at all.

---

## 7. Hand-written "N today" counts in the registry — full ledger

CLAUDE.md rule 8 names this class by name: *"the hand-written 'N today' counts throughout
`governance/check-registry.yaml`."* A full-text regex scan (line-wrap–aware, since two instances
split the number and "today" across a YAML wrap) found **32 occurrences of the literal `<number>
today` pattern**, plus 2 more volatile figures phrased without the literal word order
(`decision_capture`'s "49 orphan DRs," `doctrine_recheck`'s "11/8/158/102 respectively") that are the
same class of claim. Every one was re-measured today by running its check directly.

| line | check | claimed | live today | verdict |
|---|---|---|---|---|
| 132 | `validate_bpc` | 102 | 102 | **current** |
| 229 | `migration_reproducibility` | 7 (schema_version + six hardcoded table COUNTs) | 76 (schema_version + **all** ~75 tables) | **stale — and describes a superseded mechanism.** The script's own comment (`scripts/audit/migration_reproducibility.py:54-69`) records that the six-table hardcoded list was replaced 2026-08-28 after it let all six skip silently during a rename and the check print `EXAMINED: 7` "while examining one thing, the schema version." The registry note (written 2026-08-14, never updated) still describes the retired mechanism. |
| 251 | `migration_reproducibility_deep` | 67 (every user table + 2 exemptions) | 77 (75 identical + 2 exempt) | **stale** — same root cause, table count grew |
| 338 | `readonly_db_open_audit` | 39 | 39 | **current** |
| 367 | `db_path_env_audit` | 55 | 52 | **stale** (in-scope script count shrank — consistent with scripts being retired/archived, e.g. `validate_db.py`) |
| 382 | `alias_provenance_audit` | 2382 | 2382 | **current** |
| 541 | `validate_evidence_state` | 0 | 0 | **current** (empty-by-decision, correctly framed) |
| 558 | `validate_population` | 425 | 114 | **stale** (checked-row count dropped, consistent with the 2026-09-13 clear) |
| 593 | `validate_jurisdiction` | 111 | 111 | **current** |
| 608 | `validate_axes` | 232 (claims: population_axis_map + **item_axis_links** + access_need_axis_map) | 74 (population_axis_map 53 + access_need_axis_map 21) | **stale, and names a table that no longer exists.** `item_axis_links` is absent from `sqlite_master` today (confirmed directly); the live script instead reports against `item_taxonomy_links.icf_code` (0 of 17 axes linked — itself unwritable, its FK reaches into the still-empty `items`). The check functions correctly on the tables that do exist; only the registry's description of its subject is wrong. |
| 625 | `validate_verification_consistency` | 0 | 0 | **current** |
| 640-641 | `audit_evidence_metadata` | 106 (line-wrapped: "106\n    today") | 106 | **current** |
| 658 | `validate_pydantic_schemas` | 17 (model↔table pairs) | 20 | **stale** — `MODEL_TABLE_MAP` grew from 17 to 20 since 2026-08-14. This is the exact curated list CLAUDE.md rule 8 already names as an outstanding violation ("`validate_pydantic_schemas`' curated `MODEL_TABLE_MAP`"), and its count is drifting on schedule. |
| 684 | `audit_adversarial_use` | 9 | 9 | **current** |
| 784 | `retired_vocabulary` | 21 | 26 | **stale** — register grew |
| 810 | `matrix_consistency` | 10 | 10 | **current** |
| 843 | `claims_docket` | 68 | 68 | **current** |
| 870, 892, 909, 931 | `attestation_presence`/`schema`/`evidence`/`verdict` | 0 (diff-scoped) | 0 | **current** — confirmed via `git diff --stat HEAD~1 HEAD`, today's last commit touches no synthesis/attestation path |
| 909 | `attestation_evidence` | "79 [attestations] on disk" | 127 | **stale** — `find attestations -name '*.json' \| wc -l` = 127 today, not 79. Quoted identically at lines 865, 888, 909. |
| 1045 | `metadata_integrity_audit` | 0 | 0 | **current** |
| 1061 | `gap_mining_audit` | 0 (claims the subject is `COUNT(*) FROM gap_mining` alone) | **8** (script sums `gaps` + `gap_mining`) | **stale on two axes.** The script's own comment (`scripts/audit/gap_mining_audit.py:248-258`) records that reporting `gap_mining` alone left CHECK 1/5 (which scan `gaps`, currently 8 rows) invisible, and was fixed to sum both subjects — "so the printed count is honest for the check as a whole." The registry note (still saying "0 today... this table this whole audit walks") describes the pre-fix behavior and was never updated after the fix. The check is **not vacuous today** (`EXAMINED: 8`, `[PASS]` in `--all`) even though its own `no_floor: empty-by-decision` reasoning claims 0. |
| 1091 | `graph_audit` | 847 | 682 | **stale** (node count shrank, consistent with the 2026-09-13 clear removing evidence/connection rows that feed the graph) |
| 1107 | `validate_reasoning` | 3 | 3 | **current** |
| 1127 | `pmp_audit` | 0 | 0 | **current** |
| 1146 | `reasoning_doc_citations_audit` | 0 | 0 | **current** |
| 1302 | `pipeline_completeness_fresh` | 0 (`bpc_metadata` empty) | 0 | **current** (confirmed `bpc_metadata` still 0 rows) |
| 1319 | `evidentiary_audit_fresh` | 80 | 80 | **current** |
| 1367-1368 | `site_pages_fresh` | 93 (line-wrapped: "93\n    today"), plus the claim "items is populated repo content... not a corpus that legitimately empties" | 0 | **stale, and the underlying premise is false today** — see §3 in full. This is the most consequential entry in this ledger: the false premise is what lets a genuinely broken generator hide behind `min_items: 1`. |
| 1410 | `render_audit_browser` | 1 | 1 | **current** |
| (prose, not "N today") | `decision_capture` | "C9 reports 49 orphan DRs" | 51 | **stale** |
| (prose, not "N today") | `doctrine_recheck` | "11/8/158/102 respectively" | 11/8/**185**/102 | **stale** (ACTIVE decision count grew 158→185; the other three still match) |

**Tally: 15 current, 15 stale, 2 additional stale prose figures found outside the strict pattern.**
Every stale one is a number that moved because the corpus moved (batches landing, the 2026-09-13
clear, registries growing) — expected drift of exactly the kind rule 7 warns "derived documents"
never carry unwarned, except this drift is inside the check-registry's own internal-authority prose,
not a reader-facing document. Two entries (`migration_reproducibility`, `gap_mining_audit`) are a
different, worse class: the number is stale **because the code was fixed and the prose wasn't**,
which means the note is actively misdescribing what the check does today, not just what it found.

---

## 8. Duplicate-subject checks

No true duplicates found — i.e., no two checks that examine the same subject for the same purpose.
Two families look duplicative at a glance and are documented, deliberate pairs instead:

- `migration_reproducibility` (blocking, cheap, counts only) / `migration_reproducibility_deep`
  (advisory, slow, every row) — the registry's own note on the deep variant explains it exists
  because an adversarial trace showed the cheap one "passes on a tampered DB." Different granularity,
  same table set, intentional.
- `citation_mining_session` (blocking, one session's scope) / `citation_mining_backlog_t2`
  (informational, whole-repo scope) — same underlying script
  (`scripts/audit/citation_mining_completeness.py`) with different `--session`/no-session flags,
  same subject at two scopes, not a redundant copy.

No other subject overlap was found among the 70 (render-freshness checks each drive a different
generated surface — context map, pipeline dashboard, evidentiary dashboard, static HTML pages — not
the same one; `validate_evidence_state` and `validate_verification_consistency` both read
`specifications` but check disjoint properties — governing-refs/regulatory-stratum/tier3-threshold
vs. tier/verification-status consistency).

---

## 9. A worked example of the RIGHT way to do this: `test_db_integrity`

Worth recording as a positive counter-example to §3 and §7. `test_db_integrity` runs 71 named
sub-invariants and prints, unprompted, exactly which of them examined nothing today:

```
RESULTS: 71/71 checks passed
PASSED HAVING EXAMINED NOTHING (56): A01, A02, A03, ... K01, K02
  Their scope is empty. They are not evidence that the thing they check is true.
EXAMINED: 1788 subject-inspections across 15 instrumented check(s) of 71
```

56 of 71 sub-checks are vacuous today (their tables are empty post-clear) and the script says so by
name, rather than reporting a single green line. `run_checks.py` still reports the whole check
`[PASS]` (not `[NONE]`) because its aggregate `EXAMINED: 1788` line is non-zero — which is correct
per `nothing_in_scope()`'s "every EXAMINED line zero" rule, and is exactly why `test_db_integrity`
self-reporting its own vacuous sub-checks matters: nothing external would surface the 56/71 figure
otherwise.
