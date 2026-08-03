# Architecture decision and execution plan

**Date:** 2026-08-02 · **Status:** PROPOSED · **Supersedes:** `workplan/_superseded/comprehensive-plan-2026-08-02.md`,
`workplan/_superseded/prune-and-reinvest-plan-2026-08-02.md`, `workplan/_superseded/consolidation-and-compliance-plan-2026-08-01.md`

> **Filename adopts the `YYYY-MM-DD-slug.md` convention this plan mandates (W4.3).** The three
> superseded plans do not sort chronologically by name; this one does. Practice before precept.

**How this was tested.** Four independent read-only reviews ran against the live repo on 2026-08-02:
a viability simulation of the proposed schema map (built a throwaway map + comparator in scratch and
ran it against all 62 tables), a three-tier artifact-model test (classified every non-DB artifact and
executed the proposed invariant), a contract-triple census (all 112 edges scored for
constraint/check/log), and an adversarial review briefed to kill the design. **The design was
substantially rejected.** This plan records what survived and why.

**Revised 2026-08-02, later the same day**, after W1, W5.1 and W5.2 landed and a fifth adversarial
pass ran against them. §0 is new. Findings that changed priority are marked **[NEW]**; items whose
diagnosis was wrong are marked **[CORRECTED]** rather than quietly rewritten.

---

## 0. Executive overview — what all of this is for

### The goal

> **Any published best practice can be walked backwards — to the values it rests on, the sources
> those values came from, the population it claims to serve, and the doctrine that governed the
> judgement — and at every step the difference between "nothing found" and "not looked for" is
> visible.**

Everything below is justified by that sentence or it does not belong in this plan.

### The one number that measures it

The **fully-evidenced walk**: topic → source → captured value → population match → specification →
best-practice cell, with every hop required rather than optional.

| | |
|---|---|
| Backbone walk (topic → source → spec → best practice) | **306 tuples**, 7 topics, 13 cells |
| …of which pass through a captured value | 42 |
| …of which are population-matched to the cell's population | **0** |
| **Fully evidenced** | **0** |

**Zero.** Not one best practice in the database can show its work. That is the number this plan
exists to move, and it should be reported at the top of every future status.

### What is and is not broken

The structure is far sounder than the data. The walk **executes** — every stage 1–11 has a table and
a key, and 73 declared foreign keys have zero orphans. Two genuine structural absences remain
(no `rooms` table; no `jurisdictions`/`languages` vocabulary), and one genuine disconnection
(`jurisdictional_values` cannot name its source). Everything else that looks like a broken pipe is
an **empty** pipe: 8 extractions and 64 population matches against 863 sources.

Distinguishing these two is the discipline this plan most often failed at, in both directions —
once proposing a junction table to fix reachability that already worked, once reporting a comparator
artifact as dangling data. **Test the logic before blaming the data, and test the data before
blaming the logic.**

### The three principles, learned the hard way

1. **A column holds one domain.** Where a value and its qualifying prose must coexist, pair the
   value column with a `<column>_note` overflow rather than forcing a split at write time. A first
   attempt to split by heuristic mis-handled 120 rows and destroyed a real identifier.
2. **A status ships with its check, or it does not ship.** `data_capture_status` shipped with a
   biconditional; `citation_mining_status` shipped without one and was wrong from creation — 80
   sources misreported, and nothing in the system could contradict it.
3. **Absence must be recordable.** A NULL that means "never looked" and a NULL that means "looked,
   nothing there" will be re-searched forever. 337 sources have no DOI and no resolution outcome;
   75 have `NO-MATCH` and never need looking at again. The pattern already exists in four places
   under four names and is generalised nowhere.

### How to use this plan

Each item states **which link in the walk it makes demonstrable**. An item that cannot answer that
is either a genuine hygiene fix (say so) or should be dropped. Priority follows the walk: a link
nothing can traverse outranks a link that is merely unenforced.

---

## 0.1 Reading order for a new session

Read these, in this order, before touching anything. Roughly 40 minutes.

| # | Read | For |
|---|---|---|
| 1 | `CLAUDE.md` §0, §4, §7, §8 | the non-negotiables: commit format, migrations-only, how to run checks |
| 2 | **this file, §0** | the goal and the one number that measures it |
| 3 | `governance/pipeline-operations.md` | what the five operations are, and why "mining" unqualified is banned |
| 4 | **`references/tooling-register.md`** | **read this BEFORE proposing any tooling work.** 600+ lines of existing diagnosis. This plan re-derived findings it already held, and one item (⚑7) was framed as an owner decision when the register had already called it a stale test |
| 5 | `sessions/handoff-next-session.md` | where the last session stopped |
| 6 | `git log --oneline -25` | what moved recently; commit bodies carry the reasoning |

Then derive current state rather than trusting any number written down:

```
python3 scripts/audit/table_connectivity.py     # islands, edges, the walk, missing features
python3 scripts/tests/test_db_integrity.py      # expect ~31/41; nine content rows + C10
scripts/preflight.sh                            # gate your own diff
python3 scripts/run_checks.py --changed-from origin/main --explain
```

**Do not trust a count in prose — including in this file.** Every volatile number here was true when
written and may not be now.

### 0.2 Lessons this effort paid for

These are not general advice. Each one cost a defect, all of them in the same session, and every one
was in work that had already been verified and confidently described.

1. **Test the logic before blaming the data, and the data before blaming the logic.** Failed in both
   directions: a junction table was proposed to fix reachability that already worked, and a
   comparator artifact was reported as dangling data. The structure here is consistently sounder
   than the population.
2. **Do not relabel an intermediate result and then reason from the label.** `data_capture_status =
   'pending'` means *no row in one of four extraction tables*. It was relabelled "never captured",
   then "the claim may not exist", and produced a check that condemned every published cell. Three
   small slides across three artifacts in under an hour, each defensible alone.
3. **Ask whether a "decision" is really two copies disagreeing.** ⚑7 looked like eleven values
   needing owner ratification. Most of it is `schemas/enums.py`, the test's allow-list, and the data
   holding three different versions of one vocabulary. **A synchronisation defect wearing a
   governance decision's clothes.** Check for other copies before escalating anything as a decision.
4. **A column holds one domain.** Where a value and its qualifying prose must coexist, pair the
   value with a `<column>_note` overflow instead of splitting at write time. Splitting by heuristic
   mis-handled 120 rows and destroyed a real standard identifier.
5. **A status column ships with its check, or it does not ship.** `citation_mining_status` shipped
   without a biconditional and was wrong from creation — 80 sources misreported, and nothing in the
   system could contradict it.
6. **Look before destroying.** A migration nulled four "placeholder" authors; two were recoverable
   from elsewhere in the same database, and the loss was then reported as a finding.
7. **Generate DDL, never hand-transcribe it.** Deriving `CREATE TABLE` from `sqlite_master` for
   migration 039 caught a defect a hand-written migration would have shipped: two columns carry
   trailing comments, and appending `REFERENCES` buried the clause inside the comment, so two of
   twelve keys would have silently not existed.
8. **Declare pointers; do not infer them from column names.** Name-matching invented
   `local_ref_id → citation_mining` and `subtype → item_population_links`, neither of which is a
   pointer. Noise gets a checker demoted, which is how this repo's advisory checks died.
9. **Mutation-test before registering.** Every check added here was verified by planting the
   violation it exists to catch. Two "passing" mutations turned out to be NOT NULL and UNIQUE
   failures proving nothing, and were only caught by reading the error text.

---

## 1. The verdict

| Proposal | Verdict | Decisive evidence |
|---|---|---|
| `governance/schema-map.yaml` as a new governance artifact | **REJECTED** | `governance/conceptual-model.md` **was** the schema map of its day — signed off 2026-04-26, now cites `data/sources/` (gone) and 531 sources against a live 863. **It rotted in three months.** `architecture/schema-reconciliation.md` exists *because* this project once had five parallel schema representations and had to collapse them. This would be number six. Violates CLAUDE.md §9 guardrail 3. |
| The ~110 lines of irreducible declaration inside it | **ADOPTED, rehoused** | The simulation caught all 7 known defects **plus 4 nobody had reported**. The content earns its place; the file does not. |
| `pipeline_stage: 1–12` node field | **REJECTED** | Unfalsifiable decoration. No stage column exists in any table; `evidence_sources` is written at stage 4 and read through 10. The comparator can never produce a stage finding. |
| Scalar `target_role: a–e` | **AMENDED to list-valued** | `slugs` serves roles a, b, d **and** e. `jurisdictional_values` is (c) and (e) simultaneously. A scalar forces a lie. |
| `constraint` and `check` as map fields | **REJECTED** | Both derivable. Storing them recreates `matrix_consistency`'s private-copy failure exactly. Non-derivable residue is one bit: `enforce: required \| waived`. |
| The **log** leg of the contract triple, universally applied | **REJECTED** | Census: populated logs would have caught **1 of 5** past incidents, helped with 1, been irrelevant to 3. **The checks leg is what four of the five actually needed.** |
| Three-tier artifact model | **ADOPTED as five tiers** | Eight artifact kinds fit none of the three. Needs **MECHANISM** (operative YAML, code, skills) and **DERIVED** (`parts/`, `site/`). |
| "No canonical claim from an information-only artifact" | **ADOPTED with a pointer exemption** | Unamended it flags 300+ rows, mostly *designed* pointers (`slugs.sl_path`, 212 cells), and dies of nagging. Scoped to value/authority citations: **~100 rows + 5 checks** — a finite list. |
| Universal triple coverage on all 112 edges | **REJECTED** | ~37 zero-leg edges sit on empty or frozen tables. Cover the spine's ~25; let the rest earn instrumentation when they earn rows. |

**The reframe that replaces the map:**

> **A declared foreign key *is* the authoritative schema map.** Intent and enforcement in one object,
> checked by SQLite on every write, forever, at zero maintenance cost. **13 such keys can be added
> today with zero orphans, in one migration.**

---

## 2. What the reviews established

### 2.1 The contract triple, measured

**112 in-DB edges: 61 declared FKs + 51 soft** (id columns, JSON lists, CSV, free-text keys, code-only joins).

| Legs | Edges | Note |
|---|---|---|
| 3 | **3** | **All three are self-edges of log tables.** Not one *content* edge — source→extraction, item→BPC, cell→governing evidence — has all three. |
| 2 | ~27 | mostly FK+check, no log |
| 1 | ~45 | bare FK (`foreign_keys=ON`; `foreign_key_check` clean) |
| 0 | ~37 | soft edges: no FK, no check, no log |

### 2.2 The log layer is under-*used*, not under-built (~85 / ~15)

Every pipeline stage the owner named already has its table. Coverage is the problem:

| Log | Rows | Lifespan | Coverage |
|---|---|---|---|
| `search_executions` | 84 | **3 days** (07-24 → 07-26) | **39 of 863 admissions — 4.5%** |
| `citation_mining` | 183 | 05-11 → 07-26 | **37 distinct sources; 826 sources have no row at all** |
| `supersession_check` | 134 | **one 77-minute burst**, 2026-05-25, never again | 15.4% |
| `item_audit_runs` | 87 | 05-08 → 05-09 | 92% of items, then **frozen 12 weeks** |
| `gap_mining` | **0** | — | **0%** |
| `pipeline_runs` · `url_verification_runs` | 7 · 6 | current | ~64% · ~100% — **the only living logs, and both are job-owned** |

The one genuinely missing log is per-source processing status — and even that is half-built:
`source_value_extractions.claim_type` supports `'absent'` and has **never been used** (distribution
today: `numerical` 4, `range` 4).

### 2.3 The tension no plan can dodge

Under migrations-only, **a log row is authored by the same session whose compliance it attests**, at
commit time, with self-reported timestamps (`search_executions.executed_at` is written, not observed).
R8's append-only check catches *deletion*, not *omission* — and omission is what happened 863−39 times.

Three possible homes, no fourth: **(a)** migrations — confessional, status quo; **(b)** job-owned
direct writers — one DR per table under DR-2026-05-28 §3; **(c)** a new hook-owned class — needs a DR.

**A live gap:** `url_verification_runs` is written directly by `verify_urls.py` but is **not on
DR-2026-05-28's exemption list by name** — the DR names the jobs and exempts only two *tables*. That
is a standing violation of the migrations-only rule that nothing currently catches.

### 2.4 Where the values actually live

**DB value layer ≈ 154 rows. Prose value layer ≈ 2 900 quantified values.** Roughly 19:1. The
flagship proof: **`2440` — the corridor best practice — appears in no canonical value field.** Grep
across all 63 tables finds it only inside `connections.description` (1) and `gaps.description` (3),
while it anchors `tier-system.md` §3 and `evidence-architecture.md` §8.1.

Ingestion of the prose corpus would be **~2 000–2 600 rows**, each requiring R10 re-retrieval,
because **70 of 102 BPCs are RETRACTED-PRE-REHAB.** You cannot honestly ingest retracted values.
**This is a research backlog wearing a data-entry costume**, and it is measured in quarters.

### 2.5 Defects surfaced by the reviews that no prior audit had reported

| Defect | Measured |
|---|---|
| `connection_targets.target` → items | **210 of 507 unresolved** ("All C-items", "BIO-01–BIO-05") |
| `citation_mining.connections_produced` | **namespace broken** — holds REF-IDs and local codes, not `con_id`s; 81 values resolve to nothing |
| `jurisdictional_values.spec_id` | **26 of 26 phantom** — `SPEC-00xx` ids matching no `items.item_code`; the DDL comment admits the target table does not exist |
| `evidence_population_match.source_ref` | **33 orphans**, free-text (`"Koontz et al. 2005"`) |
| `evidence_population_match.target_population` | **28 of 64 are prose, not codes** |
| `population_reclass` | **20 of 29** dangling on `canonical_code`; **14 of 29** on `population_code` |
| `evidence_sources.jurisdiction` | **202 rows** outside the 48-jurisdiction map |
| `source_value_extractions.root_id` | **3 of 3** point into `external_root_registry`, which has 0 rows |

### 2.6 Two corrections to earlier statements in this effort

**`graph_audit`'s 959 components do not mean the graph is fragmented.** It is **one component of
1 290 nodes (57%)** plus 953 singletons — mostly node kinds the builder emits no edges for at all
(313 gaps get zero edges by construction). It must not be used as a baseline.

**The 34 orphan prose citations are not a research backlog.** 30 are *aliases* — the same source
re-entered under a new REF id during the May migration. Only 2 are grey-never-entered and 2
unmatched. **About one session.** Chasing them exposed intra-DB duplication: the HIPI trial exists
three times (REF-00068 / 151 / 373).

---

## 3. The architecture, as decided

### 3.1 Five tiers

| Tier | Contents | Rule |
|---|---|---|
| **CANONICAL** | SQLite tables | The only source a *value* may be cited from. Written only by migration. |
| **MECHANISM** | operative YAML (`check-registry`, `pipeline-contract`, `research-contract`), `schemas/*.py`, `skills/` | Executable authority. Must be machine-read by something, and drift-gated against its consumer. |
| **NARRATIVE** | doctrine, DRs, session records, attestations | Authoritative for *reasoning*, never for values. Hash-bound. |
| **DERIVED** | `parts/`, `site/` | Regenerated; never hand-edited; never cited. |
| **INFORMATION-ONLY** | workplans, registers, audits, notes | Never read by a check, never rendered, never value-cited. |

Plus **UNMIGRATED-CANONICAL** as a tracked debt state, not a tier: prose holding values with a dated
ingestion target. Current membership: 88 BPCs, 38 FDRs, 13 conflict matrices, `project-standards.md`,
`standards-registry.md`, the 156-decision register.

### 3.2 The rule that replaces the tier taxonomy's enforcement

One operative rule in `references/project-standards.md`:

> **No check reads, and no renderer cites, a *value* from prose.** Pointer columns are exempt and
> must be declared as such. Prose holding values is debt, tracked with a lift condition.

Today's violations: ~100 DB rows (82 of them `citation_mining.notes` → `sessions/artifacts/*.json`),
**5 blocking checks** that read prose as authority (`attestation_presence`, `attestation_schema` →
skill-registry; `citation_mining_session` → `sessions/LATEST`; `validate_jurisdiction` →
standards-registry; `decision_capture` → project-standards), and ≥7 site pages embedding workplan paths.

### 3.3 Values in prose stay in prose — and get bound

The contested 10–15% of doctrine is *worked examples that carry values*. Tabulating them destroys the
pedagogy; leaving them unbound is how 2440 mm ended up canonical nowhere.

**`reasoning_doc_citations` already solves this** — it holds the value in prose and verifies it EXACT
against a source row. Extend that mechanism to doctrine rather than migrating doctrine into tables.

### 3.4 Where the declaration lives, since the map is rejected

| Content | Host |
|---|---|
| Node stage/role/tier, rival-vs-authoritative | Extend `graph_audit`'s existing `MISSION_CRITICAL` dict + a severity policy (~30 lines) |
| The 20 soft edges + `enforce: required\|waived` | Same host, as a declared edge table |
| Coverage invariants (~10) | Registry checks, one each, mutation-tested |
| Edge → check attribution | `check-registry.yaml` `basis:` repoint — **22 of 58 attachable today**, residual honest paperwork ~11 checks (19%) |
| Per-stage `tables:` | `pipeline-contract.yaml` — **and ratify it or kill it**; PROPOSED since 2026-07-13 |

---

## 4. Workstreams

### 4.0 Status, and what changed after this plan was written

| Item | Status | Link in the walk it serves |
|---|---|---|
| **W1** stop active harm | **DONE** (PR #78) | none — removed instructions that actively misled |
| **W5.1** declare soft edges as FKs | **DONE** — 12 of 13; `evidence_sources` deferred, traded for check A09 | every hop: 73 FKs, 0 orphans |
| **W5.2** per-source processing state | **DONE** — migration 040 + corrections | makes "unexamined" queryable at source grain |
| **041** paired value/prose overflow | **DONE** | prevents states masquerading as values |
| Checks A09, C06, C07, C08, C09 | **DONE**, all mutation-verified | binds each status to the rows it summarises |
| `scripts/audit/table_connectivity.py` | **BUILT**, not registered | measures the walk; register once its six missing-feature findings are resolved |
| W2 repair gates that cannot fire | open | — |
| W3 prune | open | — |
| W4 continuity | open | — |
| W5.3–5.5, W6, W7, W8 | open | — |

**Corrections to this plan's own diagnosis**, recorded rather than rewritten:

- **[CORRECTED] Stage 5 is a population problem, not a structural one.** This plan implied the
  cell→extraction link was missing and proposed a junction. It is not missing: `sve.ref_id` is a
  declared FK, locators exist (`source_section`, `file_anchor`, `claim_text`), and 4 of 14 cells
  already resolve to an extraction through existing IDs. The junction is withdrawn. What *is*
  missing is narrow: **`sve` has no `item_code`**, so extraction→specification resolves by
  text-matching `parameter`, the one fuzzy hop in an otherwise typed chain.
- **[CORRECTED] The "243 dangling languages" was a comparator artifact.** Language values were
  compared against `lang_jur_map`, a language×jurisdiction *mapping*, not a vocabulary. All 37
  distinct language values are ISO 639-1 shaped and clean.
- **[CORRECTED] `graph_audit`'s 959 components** are a builder artifact (one 1 290-node component
  plus 953 singletons, mostly node kinds emitted with no edges), not fragmentation.

### 4.0.1 New findings that outrank existing items **[NEW]**

| # | Finding | Why it outranks |
|---|---|---|
| **N1** | **`jurisdictional_values` has no `ref_id`.** 109 code values, none traceable to a source. Its `spec_id` is 26/26 phantom | This is the **only** home for the regulatory stratum's values, and T4–T6 is **314 of 863 sources (36%)**. Not one of five rival tables to tidy — the sole store for a third of the corpus, disconnected |
| **N2** | **No `rooms` table.** Stage 12's catalogue exists for case studies (0 rows) and not at all for rooms — yet `site/rooms/` holds 17 hand-built pages and `room_page.py` crashes on `no such table: room` | The only *structural* break in stages 1–12 |
| **N3** | **No `jurisdictions` / `languages` vocabulary.** 72 jurisdiction values with no canonical list; `UK` and `GB` both in use for one place; 8 compound values (`AU/NZ`, `US/AU/SE/UK`) cram several countries into one field | Jurisdiction is a first-class axis of the research-tracking table (a). Owner decisions taken 2026-08-02: **`UK` is canonical**; **countries are never lumped** — compounds split into separate rows; **`MULTI`/`Multi`/`colloquial` mean nothing** and are nulled; **`ISO` stays**, with other standards bodies such as UN, as a jurisdiction level of its own |
| **N4** | **`search_candidates` has no `admitted_ref_id`.** 4 ADMITTED rows record nothing about what they became | Stage 6's queue drains into a void; the loop back to stage 4 cannot be closed |
| **N5** | **No QC at cell grain.** `item_audit_runs` is per item, `supersession_check` per (slug, ref); neither carries a `cell_id` | "Was this best practice adversarially reviewed?" is unanswerable — stage 7 runs parallel to stage 10 rather than on it |
| **N6** | **55 of 59 sources cited by a synthesis cell are `data_capture_status='pending'`** | Two layers contradict each other: synthesis has consumed sources the capture status says were never touched. Needs a ruling, not a patch |
| **N7** | **7 tables hold data with no provenance anchor** — `connection_targets`, `supersession_check`, `pipeline_runs`, `url_verification_runs`, `data_migrations`, `db_meta`, `weighting_profile` | Cannot tell who wrote those rows or when — the work-performed flag has nowhere to hang |
| **N8** | `slugs.merged_into` permits self-reference and cycles; `test_db_integrity` crashes against a pre-040 DB (C06 unguarded) | Small, cheap, from the fifth adversarial pass |

**Revised priority.** N1 and N3 move ahead of the remaining W5 items: N1 because a third of the
corpus is unprovenanced, N3 because the owner decisions are already taken and it unblocks the
research-tracking axis. N2 is owner-gated with ⚑3. `sve.item_code`, N4 and N5 are three small
columns that together make stages 5–7 traceable to stage 10.

---

W1 is complete (PR #78). W2–W4 need no owner decision.

### W2 — Repair enforcement that cannot fire *(≈4 h)*

| Target | Defect | Fix |
|---|---|---|
| `doctrine_recheck` *(blocking)* | `--cross-ref` runs only pass 2.3, whose findings are all WARNING; exit 1 needs ERROR. Deleting a CANONICAL doc **exits 0** | drop the flag |
| `audit_evidence_metadata` | registered without `--strict`; returns 0 unconditionally | real fail condition |
| `matrix_consistency` | compares code against a transcription of the doctrine held **inside the check** | parse the document |
| `citation_mining_session` *(blocking)* | mutation escape: a source with no `source_slug_links` row is exempt entirely | closed by W6.1 |
| `validate_jurisdiction` | 55 warnings that never escalate; canonical-24 list predates the corpus; dead `data/sources` leg | refresh enum, retire leg |
| **`skills/` sweep** *(new)* | Two of two skills examined in W1 were comprehensively broken against the live schema. That is a sampling result | execute every query in all 61 skills; repoint or mark BROKEN |

**Rule:** a repair is not done until the original mutation has been re-run and the check watched going red.

### W3 — Prune *(≈2 h)*

Registry: **PRUNE** `validate_population`, `validate_temporal` (both vacuous — they scan directories
that have never existed). **MERGE** `citation_mining_backlog_t2` into `_t3`. **DEMOTE**
`citation_mining_backlog_t3`, `attestation_verdict`, `test_jurisdictional_divergence`.

Scripts: **64 files to `_archived/`** (mirror origin paths; never delete). Wave 1 = 21 files, zero
callers anywhere. Wave 2 = 37, historical references only. Wave 3 = 2, after the caller fix. Wave 4 =
4, owner-gated.

The `tests` CI job is 9 of 9 advisory — 21 s per run with no failure state. Promote or schedule it.

### W4 — Continuity *(≈3 h)*

Split `sessions/LATEST` into `LATEST` (continuity) and `LATEST-RESEARCH` (the mining gate's subject);
repoint `run_checks.py:494`. Rewrite the handoff at every session close and check that its named HEAD
is an ancestor of current HEAD. Enforce `YYYY-MM-DD-slug.md` in `workplan/`. Collapse three connection
registers to one. Close the `research-contract-baseline.json` self-amnesty (baseline increases fail).
Promote `research_contract_sync` to blocking. Drop `db_meta.schema_version` (11 vs `user_version` 38).

### W5 — Schema: make the handshakes into keys *(≈6 h)*

**W5.1 — the 13 clean FKs, one migration, zero backfill.** `evidence_source_authors.ref_id` ·
`evidence_sources.superseded_by_ref_id` · `source_value_extractions.slug` · `spec_value_probes.slug` ·
`supersession_check.slug` · `search_candidates.found_under_slug` · `.suggested_slug` ·
`reasoning_doc_citations.reasoning_doc_slug` · `term_item_links.item_code` · `item_axis_links.item_code` ·
`population_axis_map.population_code` · `slugs.merged_into` · `case_studies.slug`.
**All have zero orphans today.** Closes 13 zero-leg edges permanently. Highest value-per-unit-work in
the plan.

**W5.2 — the backlog migration that fixes the owner's stated complaint.** Insert explicit
`deferred`/`backlog` `citation_mining` rows for the **826 sources with no mining row**, and adopt
`source_value_extractions.claim_type='absent'` (schema-supported, **never used**). Cost ≈ 0.5 MB.
Effect: **"unexamined" becomes a queryable state**, so a logged-but-unscraped source stops being
indistinguishable from one that was read and had nothing. *No new column required.*

**W5.3 — junctions replacing JSON.** `evidence_cell_state.governing_refs` (63 values, feeds the site
via `v_best_practice`), `search_executions.admitted_ref_ids` (39). Defer `convergence_assessment`'s
five JSON columns and `connection_targets` until those tables are load-bearing.

**W5.4 — after backfill.** `jurisdictional_values.ref_id` · `item_bpc_links` from `bpc_source_slug`
(87 rows) · `population_reclass` (14–20) · `evidence_population_match.target_population` (28 prose →
codes) · `evidence_sources.jurisdiction` (202 outside the map). ~277 rows adjudicated.

**W5.5 — fix `citation_mining.connections_produced`** — the namespace is broken (holds REF-IDs, not
`con_id`s; 81 values resolve to nothing). Blocks any junction on that edge.

### W6 — Checks on the spine *(≈5 h)*

`source_orphan_audit` (65 sources, 46 tier 1–3, no topic link) · `bpc_citation_link_handshake`
(5 of 123 cited refs violate; the contract's `judgment/derivation-handshake` criterion, currently
INCOMPLETE) · `search_coverage_handshake` (coverage *claims* vs the search log) ·
`item_bpc_links` parity vs `items.bpc_source_slug` (3 vs 87 — **only a parity check catches a decree
nobody executed**) · connection PENDING age (23 rows since early May) · supersession staleness ·
promote `graph_audit`'s `orphan.uncited_source` from WARN to ERROR.

Promote `research_dod` to blocking — the R1–R15 contract has no blocking enforcement anywhere today.

**Every new check declares `min_items`, prints `EXAMINED: n`, and is mutation-tested before registration.**

### W7 — The red gate *(1 decision + ~1 h + research)*

**B-class = 111 rows across 11 unratified vocabulary values — one D-SCHEMA decision (⚑7), not
research.** Ratify 104 semantically real (`VERIFIED-2` 71, `DISPUTED` 7, `code` 16, `PARTIAL` 5,
`CLOSED-DECIDED` 2, …); normalise 7 (`grey_literature`→`grey`, `magazine_article`→`other`);
**investigate 4** (`high`, `medium` — junk from a foreign vocabulary, *not* ratified).

**C/G-class = 120 distinct rows of metadata backfill.** Research work under R10. Sequence C02 first
(105 rows: DOI present, outcome absent — `resolve-dois.yml` already exists to do it).

**Plus ~1 session:** reconcile the 30 alias REF-ids and the intra-DB duplicates (HIPI trial ×3).

### W8 — Close out

Ratify or kill `pipeline-contract.yaml` with per-stage `tables:` and a dated disposition on each of
its 6 null criteria. Extend `graph_audit` with the node/edge declaration and severity policy.
Repoint 22 `basis:` fields. One DR covering the architecture decision. Re-attest. Update
`tooling-register.md` and CLAUDE.md §7. Write the handoff naming the first research topic. **Stop.**

---

## 5. Sequencing

```
W2 ─┐
W3 ─┼─ independent, no decision, land as small PRs
W4 ─┘

W5.1 (13 FKs) ──────────────► highest value-per-work; no dependency
W5.2 (826 backlog rows) ────► fixes the stated complaint; no dependency
W5.5 ──► W5.3 (junctions) ──► W6 checks
⚑2 ────► W5.4 backfills

⚑7 ──► W7 B-class ──► W7 C/G-class ──► ⚑1 full protection ──► W8
```

**W5.1 and W5.2 are the two highest-leverage moves in the plan and neither needs a decision.**

---

## 6. Owner decisions ⚑

| # | Decision | Why yours |
|---|---|---|
| **⚑1** | Branch protection on `main` | 30 blocking controls are advisory in fact. **Carve out `DB integrity` until W7 completes.** |
| **⚑2** | Consolidate the five rival (c)-layer tables | D-SCHEMA. 167 rows across 5 tables against 863 sources |
| **⚑7** | Ratify the 11 vocabulary values | Takes four B-class checks green in one sitting |
| **⚑8** | **Resolve the logging tension (§2.3)** — migrations (confessional), job-owned (a DR per table), or a new hook-owned class. **No fourth option.** Also regularise `url_verification_runs`, which writes directly and is not on DR-2026-05-28's list | Any *mandatory* logging is meaningless until this is settled — "mandatory" currently means "self-reported", which is what already failed |
| **⚑9** | **Do the BPC value tables become rows, or stay bound prose?** Recommend: **bound prose** — extend `reasoning_doc_citations` to doctrine and BPC. Tabulating destroys the corridor-width synthesis, whose whole move is showing three populations mean three different physical variables | DG-NON. Trajectory |
| **⚑10** | Dated ingestion targets for UNMIGRATED-CANONICAL (88 BPCs, 38 FDRs, 13 matrices, 2 registers) — **quarters, not weeks**, and gated on BPC rehabilitation since 70 of 102 are retracted | DG-NON |
| ⚑3–⚑6 | `room_page.py` · `test_adjudication_integrity` · `test_generate_parts_4_2` (recommend keep + re-fixture) · `citation_mining_pipeline.py` | Wave 4 disposals |

---

## 7. Definition of done

- [ ] No blocking check is structurally incapable of exiting 1 — each **watched going red**
- [ ] No registry check passes over an empty set
- [ ] Every `scripts/` file is registry-referenced, imported by something live, or archived
- [ ] Every skill's queries execute against the live schema
- [ ] The 13 clean FKs exist; no spine edge is zero-leg
- [ ] `"unexamined"` is a queryable state for every source
- [ ] `governing_refs` is a junction with FKs, not a JSON string
- [ ] Every value cited by a renderer resolves to a canonical row, or to prose bound and verified EXACT
- [ ] `sessions/LATEST` and `LATEST-RESEARCH` are distinct and current; `workplan/` is machine-sortable
- [ ] `pipeline-contract.yaml` is ratified or retired; `pipeline_contract_audit` reports 0 INCOMPLETE
- [ ] `test_db_integrity` 35/35 and required in branch protection

---

## 8. Provenance

Every number: a command run against this clone on 2026-08-02. Backlog counts and enum values from
direct SQL with the allow-lists read from `scripts/tests/test_db_integrity.py:95–163`. Edge census,
log coverage, and orphan counts from `PRAGMA foreign_key_list`/`table_info` plus per-pair anti-joins.
Check verdicts from adversarial mutation in a scratch clone and scratch DB — the canonical repo and
DB were never written. `826` sources with no mining row, `claim_type` distribution, and
`connection_targets` 210/507 were re-derived independently of the reviews that first reported them.

**Corrections carried forward, since earlier drafts were built on them:** the `basis:` field measures
what a check *declares*, not what it *does* (by subject the registry is 59:41 pipeline, not mostly
paperwork). The registry is not the fat — 48 of 58 checks survive mutation. `graph_audit`'s 959
components are a builder artifact, not fragmentation. The distinct backlog is 120 rows, not 110. And
the schema map proposed in this session's earlier exchanges is rejected here on the evidence of this
project's own history.
