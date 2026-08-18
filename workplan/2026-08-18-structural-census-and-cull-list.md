# 2026-08-18 — Structural census and cull list

**Question asked (owner, verbatim):** what is directly concerned with code/evidence/tables, what is
directly concerned with compliance/guardrails, and what is "recursively built [to] serve no function
beyond evaluating an evaluator of an evaluator" — then a cull list for everything that serves neither
the project nor direct compliance.

**Method.** Read-only census (Fable 5) over every check, script, skill, governance doc, workplan,
register and DB table; classification by *what each artifact takes as input*. Verified independently
by Opus 5 where marked ✓ — the ratio, the four largest cull rows and their caller sweeps, the
`.ignore` contents, the `scripts/convert/` absence and the registry text quoted in §5. Unmarked rows
are the census's, re-derivable by the sweep shown.

**Nothing here is executed.** Retirement is owner-gated (`CLAUDE.md` §9 guardrail 4) and means
**retire to `_archived/` mirroring the origin path**, never delete (guardrail 2). Redirect-stubs are
required for anything still referenced.

---

## 1. The ratio ✓

| | Lines |
|---|---|
| **Primary deliverable** — `references/bpc-reasoning/` + `references/connection-reasoning/` | **471** |
| Session records | 63,041 |
| Workplans | 52,640 |
| Audits | 47,183 |
| Governance | 13,373 |

**345 lines of process record per line of the thing the repository exists to produce.**

**43 of 66 tables are empty ✓**, including all six synthesis-core tables — `specifications`,
`evidence_sources`, `bpc_metadata`, `gaps`, `conflicts`, `connections` all at **0**.

The frame is real and populated: 93 items, 23 populations, 17 axes, 2,382 term aliases, 109
jurisdictional values, 158 item↔axis links, 372 item↔population links, 835 recovered source locators.
**The frame is ~100% populated; the evidence→synthesis pipeline is 0%.**

The apparatus is not disproportionate to the project's ambition. It is disproportionate to what
currently exists, and a large part of it is guarding nothing.

## 2. Classification by level

Level is assigned by **what the artifact takes as input**, not by where it lives.

| Level | Definition | Code (lines) | Checks (of 65) |
|---|---|---|---|
| **L0 substance** | Input is the world. Evidence, items, populations, BPC content, renders, and the code that reads/writes them | ~8,300 + 7,430 migration SQL | — |
| **L1 first-order** | Input is L0. *Is the guidebook correct?* | ~19,000 | ~44 |
| **L2 second-order** | Input is L1. *Is the checker correct?* | ~7,500 | ~18 |
| **L3+** | Input is L2+. Registers tracking audits, plans remediating plans, passes reviewing passes | ~400 code; ~46,500 live workplan prose | ~3 |

In **code** the shape is 1 : 2.3 : 1 — defensible *if the L1 subjects existed*. In **prose** it is not:
the August meta-cascade alone is 25,774 lines across 28 workplan files.

**Empty-subject census.** 16 of 65 active checks currently examine nothing. Of the blocking ones, two
are legitimately diff-scoped (`attestation_presence`, `attestation_schema`); the rest —
`source_slug_links_duplicates`, `citation_mining_session`, `validate_evidence_state`,
`validate_verification_consistency`, `check_rendered_docs` — guard corpora emptied by the 2026-08-06
reset or not yet built. **Dormant, not defective.** Four further checks are *red* on zero subjects
(`research_dod` R1, `test_verification_pipeline`, `test_directness_2_2`'s live-smoke leg) — the
un-instrumented second polarity.

## 3. Orphans — chains that never reach L0

The owner's actual question. Each with what its loss would cost, stated honestly.

| Orphan | Chain | Cost of losing it |
|---|---|---|
| **August meta-cascade** — 28 workplan files + 13 `execution-plan-2026-08-12/` files, **25,774 lines** | plan → audit-of-plan → adversarial-pass-of-audit → consolidation-of-passes (L3→L5) | **Nothing operational.** Exactly one is load-bearing: `2026-08-17-consolidated-action-plan.md`, which supersedes the rest by consolidation. What is lost is provenance detail — which is what `_superseded/` exists to hold |
| `probe_pipeline.py` (1,718) + its ~30k-line probe log | measured how the apparatus behaves → apparatus processes empty tables | Re-writing the harness if a future probe pass is wanted. `walk_harness.py` is separately cited by the live writer plan and is **not** an orphan |
| `workplan_naming` check (173) | audits whether *plans sort by date* | `CLAUDE.md` §9's "sort workplan/ by date" degrades. The real fix is fewer live workplans, which would let this retire |
| `claims_docket` + `integrity-protocol` skill | warrants for claims made *by sessions about the repo* | **Keep it.** Orphan by chain, but it polices the failure mode that generated most of the other orphans — ≥7 asserted-not-derived claims in one week |
| `references/tooling-register.md` §4–§6 as a live surface | register describing the checks; registry superseded it as inventory | The §6.7 required-check recommendation. Reduce to a stub *after* transcribing that, not archive |
| `validate_commits.py` (247) · `validate_audit_runs.py` (105) · `adjudication_integrity` pair (220) · `schema_reference_drift_audit` (215) | checkers of records of running checkers | **Nothing.** All quarantined, superseded or corpus-dissolved |
| Decisions **triple** store — `decisions/*.md` + 5,558-line YAML + DB `decisions` (163 rows), held equal both directions by `test_db_integrity` L01 | an L2 check whose whole function is keeping a duplicate alive | Owner decision #2; sweep already complete |

**Self-referential loops.** The repo's own T1 is the sharpest: the ratification-sweep gate that would
stop obligations rotting in prose is *itself* an obligation rotting in prose. Also: the PR #103
adversarial pass wrote its own discharge status into the brief it was discharging.

## 4. Cull list

Every row is **owner-gated**. Sweeps shown were actually run.

### 4a. Tier A — cull now, zero or near-zero dependents (~41,000 lines)

| # | Path(s) | Lines | Ground | Caller sweep | What breaks | Stub? |
|---|---|---|---|---|---|---|
| 1 ✓ | `references/claim-reference-join.{json,md}` | **16,526** | superseded | `git grep -l -- scripts skills governance tools .github schemas` → one hit, a *mention* in `retired-vocabulary.yaml` | Nothing. REF-id-era index; the reset deleted every REF-id it joins | no |
| 2 ✓ | `references/global-reference-registry.{json,md}` | **10,224** | superseded | same → one prose line in `governance/conceptual-model.md` | Nothing; patch one line | yes (md) |
| 3 ✓ | `workplan/deprecated/` (16 files) | **6,324** | stale-in-live-location | `.ignore:53` covers `workplan/_superseded/` but **not** `workplan/deprecated/` | Nothing — already a graveyard, merely parked on the live search surface. Move to `_superseded/` | no |
| 4 ✓ | `references/specification-database.json` | **3,755** | superseded | same sweep → **zero hits** | Nothing. April snapshot of 73 specs | no |
| 5 | `references/bibliography-v11-draft.md` | 1,789 | superseded | zero live-code hits | Nothing; superseded by the compiler pipeline | no |
| 6 | `references/citation-mining-register.md` | 319 | stale-in-live-location | one hit: `research-log-manager_SKILL.md`, which itself states the register **is archived** | Nothing — but the file carries **no banner** and still says "CHECK this register BEFORE mining" | yes |
| 7 | `references/coverage-matrix.md` | 120 | stale | zero live-code hits | Nothing. 2026-04-08 snapshot | no |
| 8 | `scripts/workflows/anchor-correctness-sweep.js` | ~300 | one-time, executed | only its own file + DRs recording the sweep | Nothing; results ratified in DR-2026-07-20 | no |
| 9 | `scripts/probes/citation_mining_pipeline.py` | 254 | abandoned | frozen working notes + one workplan | Nothing; its input table has 0 rows | no |
| 10 | `scripts/validate_commits.py` | 247 | duplicated | quarantined; no CI or skill caller | Nothing; `check_commit_msg.py` + `check_doctrine_token.py` are the wired pair | no |
| 11 | `scripts/audit/schema_reference_drift_audit.py` | 215 | superseded | retirement **already proposed in-registry**; `graph_audit` carries the signal better | Nothing; transcribe one legacy finding first | no |
| 12 | `scripts/validate_audit_runs.py` | 105 | dead | registry: "unreferenced by any contract; wire only with a stated owner" — none in 17 days | Nothing | no |

### 4b. Tier B — cull after one named prerequisite (~35,000 lines)

| Path(s) | Lines | The one prerequisite |
|---|---|---|
| `working/mobile-app-prototype-v9/` | 9,121 | Owner ruling; DR-2026-07-12 item 4 lists its `HANDOFF.md` |
| August meta-cascade minus the 08-17 plan | ~24,000 | Confirm the 08-17 plan's §0 supersession covers each, then `_superseded/` |
| Old live workplan stratum (~55 files) | ~13,000 | Per-file sweep; the `workplan_naming` grandfather list is the exact census |
| `data/decisions/decision_register.yaml` + importer + guard + L01 | ~5,900 | **Owner decision #2** |
| `references/connection-register-active.md` + `-archive.md` | 3,581 | Patch 3 skill references; files carry "Do NOT read" banners on the live surface |
| April governance drafts (`armature_v3_review`/`v4`/`v4_integration`/`v4_resolutions` + 6 others) | ~2,850 | Execute DR-2026-07-12's P2 consolidation item |
| `scripts/tests/probe_pipeline.py` | 1,718 | Writer-plan confirmation that only `walk_harness.py` is shared |
| `scripts/generate/room_page.py` + `site/rooms/` | ~1,500 | **Owner decision #8**, room stratum |
| `scripts/validate_temporal.py` | 544 | Owner ratification the quarantine note already requests — see §5 |
| `scripts/verify_resolved_dois.py` | 287 | **Owner decision #8** |
| `scripts/check_phase_a_complete.py` | 234 | Confirm the live BPC workplan carries its status |
| `adjudication_integrity` + its test | 220 | Owner call on the 274-finding backlog the reset dissolved |
| `references/slug-registry.md` | 130 | Patch `validate_cross_refs.py` + one skill |
| `skills/question-author_SKILL.md` | 118 | Governed skill retirement. Its own header: "⚠ INOPERATIVE — every SQL statement below targets a table that does not exist" |

### 4c. Tier C — DORMANT, do **not** cull

Empty because of the 2026-08-06 reset or pre-Phase-E state. Correct machinery, absent subject.

- **Checks:** `source_slug_links_duplicates`, `citation_mining_session`/`_backlog_t2`/`_t3`,
  `validate_evidence_state`, `validate_verification_consistency`, `research_protocol_audit`,
  `metadata_integrity_audit`, `gap_mining_audit`, `population_integrity_audit`, `pmp_audit`,
  `reasoning_doc_citations_audit`, `check_rendered_docs`, `validate_conflicts`,
  `full_db_metadata_verification`, and the red legs of `test_verification_pipeline` /
  `test_directness_2_2`.
- **Skills:** `evidence-metadata-rehabilitation`, `gap-driven-mining`, `citation-miner`,
  `citation-verifier`, `specification-curator`, `item-specification-writer`.
- **Revival trigger:** first `evidence_sources` / `specifications` rows at Phase B/E restart.

Culling these would only have to be undone.

### 4d. Contested — arguable both ways, not recommended either way

`index.html` (803, the intended-end-state mockup vs a dead-link duplicate) · `tooling-register.md`
(reduce-to-stub after transcription) · `table_connectivity.py` (82; the quarantine entry is doing its
job) · `jurisdictional_divergence` pair (the audit is quarantined while its **test runs in every
battery** — an active L2 guarding a never-selected L1) · `population_page.py` (a wiring question, not
a retirement) · `code_currency_audit` / `pre_rehab_banner_audit` (real adjudicable findings) ·
`working/evidence-migration/` (3,150) · seven references-root analysis docs **on which no caller sweep
was run** — off the list by the census's own rule until someone runs it.

## 5. Two defects found in passing

1. ✓ **A quarantined check's revival path is broken.** `governance/check-registry.yaml:1441` keeps
   `validate_temporal` re-registerable because *"its generator, `scripts/convert/version_retrofit.py`,
   still exists"*. It does not — `scripts/convert/` was archived in the Tier-1 batch on 2026-08-15.
   The entry preserves a check whose stated path back is gone.
2. ✓ **`workplan/deprecated/` is not hidden from search** while `workplan/_superseded/` is
   (`.ignore:53`). A directory named *deprecated* is fully greppable, so every session searching for
   prior work can land in it and get an answer that was true in April. This is the `.ignore`
   mechanism's own rationale (`DR-2026-08-06-cold-storage-search-scope`) failing to cover the
   directory most obviously in its scope.

## 6. What must not be cut

- **The write path and its gates** — `emit_data_migration.py`, `migrate_db.py`, `db.py`,
  `scripts/migrations/`, `migration_reproducibility(+deep)`, `readonly_db_open_audit`,
  `db_path_env_audit`. A naive "not CI-reachable" cull would delete the only sanctioned write path;
  the remediation workplan §6 warns about exactly this and is right.
- **The frame and its validators** — the populated L0 with live L1.
- **The registry, runner and selftests** — burned four times by vacuous passes and once by a
  self-administered amnesty. This instrumentation has earned its keep.
- **Attestations, DRs, sessions, `_archived/`, frozen audits** — the governed audit trail.
- **`working/pilot/` + `assess_cell.py` + the two `*-complete-provision.md` files** — the single
  end-to-end worked example of the intended pipeline, and among the only real L0 synthesis here.
- **Tier C** — see above.

## 7. Not classified

Seven references-root analysis docs (no sweeps run) · `references/audit-briefs/` (58 files — may hold
the only surviving copy of pre-reset gap content, since `gaps` is now 0) · `references/change-orders/`
· `misc/`, `assets/` · the `sessions/session-artifacts/` subtree · `skills/deprecated/` contents ·
whether `graph_audit`'s 847 nodes are still content-bearing post-reset · the live branch-protection
required-check set.
