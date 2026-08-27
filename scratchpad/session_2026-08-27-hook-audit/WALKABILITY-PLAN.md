# Review of 2026-08-25 → 2026-08-27 · nomenclature, keys, pointers, and the walk

**Read-only review. No schema change, no migration, no code change, no DB write.**
Every figure was derived this session against `user_version` 64, read-only. Where a prior figure is
repeated it is labelled inherited and dated. Re-derivation commands are in the appendix.

**Headline.** The window ruled a great deal and executed none of it — the database has not moved
since 2026-08-25 21:58. The nomenclature work of the last session is sound in its **grammar** and its
**table map**, wrong in its **migration strategy**, and internally contradictory between Parts E and
J. All three are settled below on measurements, and the settlement is better news than the proposal
was: **the walkable spine costs one ordinary migration and no baseline.**

---

## PART 0 — Method, and the one standing rule this supersedes

**Subject:** ~45 commits from `8691736` (2026-08-25 22:50) to `5e4dbd5` (2026-08-27 03:44) — the
rulings-incorporation sweep, the pipeline smoke test, and the nomenclature reconciliation.

**Method:** agonist–antagonist, at owner instruction.

**Rule-0 note, recorded not argued.** `references/project-standards.md` (2026-08-19) holds that
*"adversarial review is a truth-instrument bound to evidence, never a plan-instrument"* and that plans
and registers are not adversarial-pass subjects. The owner has directed agonist–antagonist work on
exactly such a subject. Per `CLAUDE.md` rule 0 the live direction governs on contact; the supersession
is recorded, not weighed.

**The superseded rule names a real failure mode, and it is cheaper to defeat than to ignore.** Its
stated reason: *"a pass whose subject is a plan cannot be wrong about anything a reader could check."*
So **every antagonist move below binds to a measurement.** No contest resolves on judgement, taste or
authority. Each resolves on a number, with the command to re-derive it.

---

## PART 1 — What the window actually did

**It ruled four times and executed nothing.**

```bash
git log --oneline --since=2026-08-25 -- data/guidebook.db
# → c146c91  governance: retire two cross-stage column copies forward [2026-08-25 21:58]
```

One DB-touching commit, at the very start. **Nothing on 08-26. Nothing on 08-27.** Last schema
migration `064`; `user_version` 64; 33 data migrations. Across two days that produced four owner
rulings, a 921-line audit, four adversarial reports and six ledger entries, the database did not move.

| Measure | Value |
|---|---:|
| Tables | **66** |
| — zero-row | **33** |
| Views | **18** |
| — zero-row | **11** |
| Foreign keys | **80** |
| — cross-stage / within (inherited, 2026-08-27) | 43 / 37 on 8 columns |
| Tables with **zero inbound** FKs | **48** of 66 |

**Stages 3–6 are empty end to end:** `source_value_extractions` 0, `specifications` 0,
`convergence_assessment` 0, `bpc_metadata` 0. There are 10 `evidence_sources` and 875
`source_locators` — a lead index 87× larger than the evidence it leads to.

**This is the frame for everything below.** The window's diagnosis — *"the walk has no keys"* — is
correct and reproduced. But it is half the diagnosis, and the missing half sets the plan: **the walk
has no keys and no rows.** `CLAUDE.md` rule 4 already rules on what that means — *"treat a 0-row
object as unproven, not clean."*

---

## PART 2 — UNPROPAGATED DECISIONS

Ruled, recorded, not reaching the machine. All seven verified this session.

### U-1 · The six-stage spine is not in the machine — BLOCKING

```
governance/pipeline-contract.yaml  stages: → research, evidence-collection, judgment, synthesis, render
tools/pipeline_completeness.py:37  STAGES = [... same five ...]
```

`specification` absent from both. `pipeline-contract.yaml` is by `CLAUDE.md`'s own words *"the single
home of the stage ids"* — so the declared single home contradicts `CLAUDE.md`, and `CLAUDE.md` is what
changed. **Every other item is being built against a spine the machine does not recognise.**

**Second-order damage nobody flagged.** `pipeline_completeness.py` reads `specifications` as the
**judgment** stage's output — line 152 is literally
`items_judged = scalar("SELECT COUNT(DISTINCT item_code) FROM specifications")`. Nine more queries
(lines 70, 147, 149, 158, 161, 184, 187, 201, 221) do the same. Adding a sixth stage without
re-pointing these leaves the dashboard reporting specification volume as judgment progress.

### U-2 · No `<stage>_items` hand-off object exists
All spellings absent: `research_items`, `evidence_items`, `judgment_items`, `synthesis_items`,
`specification_items`, `render_items`, `jud_items`, `evi_items`.

### U-3 · The `MOB` split is unexecuted
`MOB` present; `AMB`/`WHEEL` absent; 23 codes unchanged. **9 live skill files still teach `MOB`** —
token-boundary match over `skills/*_SKILL.md`, excluding `skills/deprecated/`, and they include
writers and checkers, not just prose. *(An earlier figure of 12 in this document was a substring grep
over `skills/ governance/ scripts/` that also caught "MOBILITY" and non-skill paths. Corrected.)*
Separately, the twelve **retired population codes** live in **17** skill files — A1-W5, a different
measurement that must not be conflated with this one.

### U-4 · `axes` → `icf_demands` (§R8) is unexecuted
`axes` 17 · `item_axis_links` 158 · `population_axis_map` 53 · `access_need_axis_map` 21.
`icf_demands` absent. `axis_code`/`AX-` still live in `scripts/validate_axes.py`,
`governance/functional-taxonomy.md`, `governance/context-map.yaml`.
**This is the vocabulary whose bare-code use changed research output on 2026-08-19** — four of five
searches framed on one demand mechanism. Highest content consequence of the seven.

### U-5 · `items` is still `items`
93 rows, **10 inbound FKs** on `items.item_code`.

### U-6 · `specifications` does not key from the judgment object
27 columns, one inbound FK, `convergence_id` — no judgment key, because no judgment object exists.
Blocked behind U-2.

### U-7 · A live rule-5 violation, found while auditing rule 5, still live
`evidence_population_match` carries **both** `source_ref` and `ref_id` — **0 mismatches across all 25
rows.** Cheapest fix in this document; needs no ruling. Grep `scripts/migrations/data_*` for the
column first, then writer-retire → reader-retire → NULL forward.

---

## PART 3 — MISSED DECISIONS

### Already recorded as owner-owed
**M-1 · evidence → judgment cardinality.** REOPENED. C2 puts the measurement in front of it.
**M-2 · `judgment_items`' column set.** Derived in Part 7 / T-A2 from what `specifications` needs.
**M-3 · Prose in files or rows.** Measured: the status quo **is already files** —
`best_practice_synthesis` is named in six-to-eight governance documents and is **a column nowhere**;
`bpc_metadata`'s 16 columns are all process metadata; text lives at `slugs.bpc_path`. This is a
ratification or a reversal, and ratifying is nearly free.

### Surfaced by this review

**M-4 · The `-item` rule collides with itself at `render`; two owner rulings contradict.**
The `-item` ruling gives every stage a `<stage>_items`. The 08-26 ruling makes `items` the render
rollup. The 08-27 adversarial pass **withdrew `ren_items`** because it re-creates `render_manifest`,
dropped by `_archived/scripts/migrations/046_drop_render_manifest.sql` — verified this session, header
quotes the owner: *"the entire pipeline is dynamic rendering on site"*, *"do not rely on artifacts for
rendering the site."* So render is required to have a hand-off table, required to be `items`, and
forbidden to have one.

**Resolvable without the owner.** Render is terminal — no downstream stage consumes from it. §1
forbids adding what nothing reads. **Therefore the hand-off rule binds stages 1–5; render consumes and
does not produce.** `CLAUDE.md` should say five, not six.

**M-5 · Retiring `items` while minting `*_items` maximises the ambiguity it was meant to remove.**
The ruling's stated reason is *"the word was the ambiguity."* The remedy mints five table names
containing that word while `item_code` — **10 inbound FKs** — is untouched. A reader still meets
`judgment_items.item_code`. **Owner-owed** (Q2).

**M-6 · The `specification` stage has no contract entry, and none can be written from the ruling.**
`pipeline-contract.yaml` requires per stage an `anchor`, `entry`, and `criteria` each with `id`,
`kind`, `criterion`, `references`, `check`. The ruling supplies none. **But it is derivable:** four of
the five current `judgment` criteria (`governing-refs-nonempty`, `no-regulatory-stratum-stated`,
`tier3-alone-threshold`, `derivation-handshake`) are enforced by `scripts/validate_evidence_state.py`
**against the `specifications` table** — they are specification criteria mis-filed under judgment.
`convergence-independence` stays. No ruling needed; T-A1 does it.

**M-7 · The window's output is unpropagated into the workplan.**
`workplan/2026-08-22-master-execution-plan.md` has no phase for the six-stage spine, the `-item`
rename, or the mobility split. R6 is correctly VOID. **The plan of record does not contain the work of
record.**

**M-8 · Neither the 08-25 nor the 08-27 rulings have a Decision Record.**
`ls decisions/ | grep -E "08-2[5-9]"` → nothing. Four rulings live only in the ledger. That ledger is
authoritative so this is not a validity defect — but `decisions/` is what
`scripts/audit/decision_capture.py` reads and where a reader is sent. One consolidating DR, not four.

---

## PART 4 — The walkability defect, re-measured

Reproduced, **with the overclaim removed.** The defensible form is *no **cross-stage** foreign key
lands on a hand-off object* — two same-stage keys do (A1-O2, and the table below shows them):

| stage output | inbound FKs | cross-stage |
|---|---:|---:|
| `source_locators` (research) | **0** | 0 |
| `source_value_extractions` (evidence) | 1 | 0 |
| `specifications` (specification) | 1 | 0 |
| `bpc_metadata` (synthesis) | **0** | 0 |

**The wider shape, which the window did not state: 48 of 66 tables have zero inbound FKs.** The
hand-off objects are not exceptional — they are typical. Unreferenced include every junction the
pipeline actually uses: `item_population_links` (372), `jurisdictional_values` (109),
`search_candidates` (60), `evidence_population_match` (25), `search_admissions` (10),
`source_slug_links` (10).

The 80 keys that exist point at six substrate vocabularies (`slugs.slug` 16, `items.item_code` 14,
`populations.population_code` 11, `axes.axis_code` 3, `access_needs.need_code` 2, `terms.term_id` 2)
plus `evidence_sources.ref_id` 13. **The schema is a star around vocabularies, not a chain along a
pipeline.** Stages are joined by a shared topic label — `slug` — not by what the previous stage made.

**What reaches the book** — the §1 burden, paid. `specifications.governing_refs` is free text. When a
determination renders "1200 mm ●" there is no key path from that figure back to the extraction that
produced it, or the paper the extraction read. **A reader cannot check the number and neither can a
gate** — which is how five fabricated citations passed six green gates on 2026-08-19. That is the
payment for `judgment_items` and the two junctions. It is **not** paid for `render_items` (M-4).

---

## PART 5 — The contests

### C1 — Rename-first, or data-first?

**Agonist.** The owner ruled *"the rename creates the spine"*, over deferring keys to a second
migration. Rule 0: that stands, and nothing below is offered against it.

**Antagonist.** 33 of 66 tables are empty; stages 3–6 hold **zero rows**. A NOT NULL foreign key
between two empty tables is satisfied vacuously. `CLAUDE.md` §2(a) names this exact failure — *"a gate
that passes having examined nothing"* — produced four separate times here.

**Resolution — the order stands; the acceptance criterion changes.** "The rename is done" cannot mean
"the migration applied". It must mean **one slug has walked all six stages with the keys carrying**,
`EXAMINED: n > 0` at every stage. The rename and the first walk belong in one phase, and **the walk is
the gate on the rename.**

### C2 — evidence → judgment: 1:1 or 1:N?

**Agonist (1:1).** *"each row of evidence provides one row for judgment."*

**Antagonist.** `evidence_population_match` holds **25 rows across 10 sources** — fan-out exists in
live data today. `UNIQUE(evidence_item_id)` makes those 25 rows unrepresentable and abolishes the
dissent contest `add-population-match` deliberately preserves.

**Resolution — an ambiguity in the sentence, not a conflict with the ruling.** Two readings:

- **(a) constrains evidence's fan-out** — one evidence row yields at most one judgment.
  **Contradicted by live data**: 25 grades over 10 sources.
- **(b) constrains judgment's parentage** — each judgment traces to exactly one evidence row.
  **Consistent with all 25.**

(b) satisfies the sentence exactly, keeps the contest, and yields `evidence_item_id NOT NULL` with
**no** UNIQUE. **Do not send a bare question. Send reading (b) and the two counts.**

### C3 — Six new tables, or six views?

**Agonist.** Hand-off objects must be real tables with NOT NULL keys, or the spine is advisory.

**Antagonist.** §1 puts the burden on whoever adds apparatus, and the 08-27 handoff records the debt:
*"Pay §1's burden of proof for `jud_items`, `syn_judgment_links`, `spe_synthesis_links`, or drop
them."* Unpaid, these are three more tables in a schema with 33 empty ones.

**Resolution — paid for `judgment_items` and the two junctions; refused for `render_items`.** Part 4
states the book-facing defect. The junctions inherit the payment: the fan-in is the only structure
letting a specification name the judgments it rests on — the same traceability, one hop later.

### C4 — Rebuild from a new baseline, or incremental? — **the last session's answer is refuted**

**Agonist (Part I).** A new baseline, exactly as `057` was made. Three arguments: (i) 057's own header
— one rename collided with **19** data migrations and needed a new ordering mechanism, and there are
33 now; (ii) **SQLite cannot ALTER a constraint**, so adding NOT NULL + FK is create-new → copy →
drop → rename, meaning *the incremental path is already a rebuild, done 66 times, with 66 chances to
miss a caller*; (iii) one baseline is one caller sweep.

**Antagonist — all three fail on measurement.**

1. **(ii) is false at the stated scale.** `ALTER TABLE RENAME` rewrites `REFERENCES` clauses **and
   view bodies** automatically on SQLite 3.45.1 (measured by the 08-27 audit). The create-new→copy
   dance is needed only where a NOT NULL FK is **added to an existing table** — that is
   `source_value_extractions` and `bpc_metadata`, **two tables, both 0 rows**. `judgment_items` and
   the junctions are new CREATEs. So the incremental path is a rebuild done **twice, on empty
   tables**, not 66 times.
2. **(i) describes a solved problem, and the solution is already in the tree.** The "new ordering
   mechanism" 057 built is `AFTER_DATA`, implemented at `scripts/migrate_db.py:282–320` and in live
   use by two migrations. A rename migration declaring `-- AFTER_DATA: <ts>` runs after every data
   migration. **The collisions cost one marker line, not a baseline.**
3. **(iii) inverts once the collisions are counted.** Measured this session — data migrations
   referencing a table this proposal renames: **24 of 33 files**, concentrated in
   `evidence_sources` 16 · `search_executions` 7 · `search_candidates` 7 · `citation_mining` 7 ·
   `source_locators` 6 · `evidence_population_match` 4 · others 2 each. **And zero for every spine
   table**: `items`, `specifications`, `bpc_metadata`, `source_value_extractions`, `axes`,
   `convergence_assessment`, `spec_value_probes`, `item_bpc_links` — **0 data-migration files each.**

**Resolution — incremental, and the reason is the good news in this document.** See C5.

**What survives from Part I, and it is the urgent part — I.7.** *"The moment the first determination
is written — one row in `specifications` — the grain change, the key change, the hand-off keys and the
population fan-out all stop being schema edits and become re-derivations of reasoned content."*
That is exactly right, and it sets the deadline: **the spine must land before the mobility batch
writes its first row.**

### C5 — **NEW: the problem splits, and the expensive half is not the half that matters**

The collision measurement above partitions the work in a place nobody looked:

| | tables | data-migration collisions | rows |
|---|---|---:|---:|
| **The spine** — `specifications`, `bpc_metadata`, `source_value_extractions`, `items`, `axes`, `convergence_assessment`, `spec_value_probes`, `item_bpc_links`, plus new `judgment_items` + junctions | 8 renames + 3 creates | **0** | **0** |
| **The nomenclature sweep** — `evidence_sources`, `search_executions`, `search_candidates`, `citation_mining`, `source_locators`, `evidence_population_match`, `source_slug_links`, `search_admissions`, `gaps`, `jurisdictional_values` | 10 renames | **24 files** | 1,179 |

**The walkable spine — the thing the owner actually asked for — touches only zero-row tables with
zero replay collisions.** It ships as **one ordinary schema migration**, no baseline, no `AFTER_DATA`
marker, no data reconciliation, because there is no data.

**The cosmetic-but-real nomenclature sweep of research/evidence is where all 24 collisions live** —
and it is separable, later, and `AFTER_DATA`-solvable when it comes.

**Do not bundle them.** Bundling makes the cheap urgent half wait on the expensive optional half, and
I.7 says the cheap half has a deadline.

### C6 — Parts E and J contradict; J.4's own rule settles it

Recorded but unresolved (08-27 handoff item 4). Four conflicts, all resolved by J.4 —
> *"A new table is warranted only when the ROW-KIND is new. A new provenance is a COLUMN. A new
> relationship is a junction. A new activity is a `kind` value on an existing runs table."*

| # | Part E says | Part J says | Resolution |
|---|---|---|---|
| 1 | `search_coverage` → `res_coverage_links` | **delete** — restates `search_executions.slug/jurisdiction` | **Delete.** Rule 5: a second home for a fact another table states, and the first home is per-query, more precise. 0 rows. |
| 2 | `search_languages` → `res_language_links` | **delete** — same | **Delete.** Same grounds. 0 rows. |
| 3 | `search_admissions` → `evi_admission_links` | **redundant** — once `evi_items.research_item_id` names the lead, the edge is a join | **Keep for now, retire at T-B.** It holds 10 live rows and is the subject of `v_source_admission`, a live cross-stage pointer. Retiring it is a T-B task with a view rewrite, not a T-A one. |
| 4 | `evidence_population_match` → `jud_population_grades` (own table, moves to judgment) | *(silent)* | **Fold into `judgment_items` as columns.** A population grade of an extraction **is** the judgment row-kind — J.4 says that is not a new table. This also makes C2 exact: the 25 rows become 25 `judgment_items` rows, which is reading (b). |

**Part E also still carries the NOT NULL back-pointers that Part B replaced with junctions, and still
lists `ren_items`.** Both are stale; Part 6 below is the corrected map.

---

## PART 6 — NOMENCLATURE and the shape, under the four constraints

### 6.0 The four constraints — owner statement, 2026-08-27, recorded on contact

> *"the pipeline must be walkable all directions (read write both ways) · render must end up able to
> pull data across all tables all stages as required for things like citations and jurisdiction
> comparison tables · we rely on using pointers and reference IDs · we need to minimize tables"*

**Two of these change the design as it stood an hour ago**, and one of them reverses a recommendation
the last session made. Taken in order below. Nothing here is weighed against the paperwork it
changes; the supersessions are recorded.

| # | constraint | status of the design before this | what changes |
|---|---|---|---|
| 1 | walkable **both directions** | forward-only. Backward walk worked by FK; forward walk was an unindexed scan | **§6.3 — index every hand-off column; the reverse lookup is half the spine** |
| 2 | render pulls **across all stages** | render was "terminal", which was read too strongly | **§6.5 — terminal in hand-off, omnivorous in reads; the view layer is the mechanism** |
| 3 | pointers and **reference IDs** | 4 of the spine objects key on surrogate INTEGERs | **§6.4 — stable `<STAGE>-NNNNN` codes, and a live latent defect on the critical path** |
| 4 | **minimize tables** | net 66 → 61, and I called that "correct" | **§6.6 — reversed. Net 66 → 48, by deletion, not by merging** |

### 6.1 The grammar — carried forward unchanged, it survived the audit

> **`<stage-prefix>` `<subject>` `<kind-suffix>`**, head noun always plural.

**The hand-off object is `<prefix>_items`. Full stop.** One word appended; no coined noun. Satellites
inside a stage keep descriptive names — they are not the hand-off and nothing outside keys to them.

| kind | test | suffix |
|---|---|---|
| **hand-off item** | the object the next stage consumes | `_items` |
| **registry** | PK is a code this table mints, and others key to it | *(none)* |
| **junction** | PK composed of ≥2 columns that each identify another thing | `_links` |
| **run** | a record of an act performed, with a timestamp and outcome | `_runs` |
| **record** | anything else — one row is a thing that happened or was decided | plural noun naming what one row *is* |

Prefixes, from `stage_id[:3]`: **`res_ evi_ jud_ syn_ spe_ ren_`** — six distinct, derived not stored.

**Two grammar rules the audit added, both load-bearing:**
- **J.4** — new table only for a new *row-kind*; provenance is a column; relationship is a junction;
  activity is a `kind` value.
- **Derivability, not count, is the metric.** Six `<prefix>_population_links` tables are better than
  one polymorphic `(stage, item_id, population_code)`, which trades six enforced foreign keys for
  zero — SQLite cannot key a polymorphic column. Six *predictable* names cost a reader nothing.

### 6.2 The map — Part E corrected by C6, M-4 and Part B

**Legend:** ‡ changes stage · † name fault beyond the prefix · **⊘ delete, do not rename**

#### RESEARCH — `res_`
| current | rows | → | note |
|---|---:|---|---|
| `source_locators` | 875 | **`res_items`** † | hand-off. "Locator" is wrong twice: it holds `doi/url/pmid/isbn`, while R3 defines a locator as a *within-document* pointer — which is what the **15** `loc_*` columns on the extraction table hold (7 start + 7 `_end` + `loc_note`; A1-W3 — "sixteen" wrongly counted `locator_scheme`). **Gains `origin` and `parent_item_id`** (J.1). |
| `jurisdictional_values` | 109 | `res_code_leads` † | 109 rows, **0 non-null** in `value_text`/`value_numeric` under the 2026-08-12 REFERENCE-ONLY ruling — the name states the opposite of the ruling |
| `search_candidates` | 60 | `res_candidates` | |
| `search_executions` | 28 | `res_searches` † | the row is a search, not an "execution" |
| `citation_mining` | 10 | `res_mining_runs` † | names the activity, not the row — **and see J.1: the yield becomes `origin` on `res_items`** |
| `gaps` | 5 | `res_gaps` | |
| `gap_mining` | 0 | `res_gap_mining_runs` † | |
| `search_coverage` | 0 | **⊘** | C6-1 |
| `search_languages` | 0 | **⊘** | C6-2 |
| `reference_stubs` | 0 | **⊘** | 0 rows, no writer |

#### EVIDENCE COLLECTION — `evi_`
| current | rows | → | note |
|---|---:|---|---|
| `source_value_extractions` | 0 | **`evi_items`** † | hand-off, and the sever. **Gains `research_item_id NOT NULL`** |
| `evidence_source_authors` | 37 | `evi_source_authors` | where the 2026-08-19 fabrication happened |
| `evidence_sources` | 10 | `evi_sources` | the admitted corpus — satellite, not hand-off |
| `source_slug_links` | 10 | `evi_slug_links` | |
| `search_admissions` | 10 | `evi_admission_links` † | C6-3: keep now, retire at T-B with the `v_source_admission` rewrite |
| `extraction_population_links` | 0 | `evi_item_population_links` | |
| `supersession_check` | 0 | `evi_supersession_runs` † | |
| `url_verification_runs` | 0 | `evi_url_verification_runs` | already correct |
| `external_root_registry` | 0 | `evi_roots` † | "registry" names the cabinet, not the row |
| `evidence_population_match` | 25 | **→ folded into `jud_items`** ‡ | C6-4 |

#### JUDGMENT — `jud_`
| current | rows | → | note |
|---|---:|---|---|
| *(none)* | — | **`jud_items`** ‡ | **NEW.** Per-extraction soundness and weight. `evidence_item_id NOT NULL`, no UNIQUE. Absorbs the 25 population grades as columns (C6-4). Column set at T-A2. |
| `item_audit_runs` | 0 | `jud_audit_runs` | |

#### SYNTHESIS — `syn_`
| current | rows | → | note |
|---|---:|---|---|
| `bpc_metadata` | 0 | **`syn_items`** † | hand-off. It is not metadata — it *is* the synthesis. Gains `kind` (`primary`/`comparative`), J.2 |
| *(new)* | — | `syn_judgment_links` | fan-in junction, ≥1 per synthesis |
| *(new)* | — | `syn_synthesis_links` | comparative fan-in, self-referential (J.2) |
| `item_bpc_links` | 0 | `syn_item_links` † | **must be re-keyed** — today references `slugs` and `items`, never `bpc_metadata` |
| `convergence_assessment` | 0 | `syn_convergence` ‡† | in from judgment — counting independent roots is weighing |
| `conflicts` | 0 | `syn_conflicts` ‡ | in from judgment |
| `connections` | 0 | `syn_connections` | **open (J.2):** may become `syn_items` with `kind='connection'` |
| `connection_targets` | 0 | `syn_connection_links` † | as above |
| `reasoning_doc_citations` | 0 | `syn_citations` | |
| `citation_population_links` | 0 | `syn_citation_population_links` | |

#### SPECIFICATION — `spe_` *(a stage again)*
| current | rows | → | note |
|---|---:|---|---|
| `specifications` | 0 | **`spe_items`** ‡ | the determination. Keys on the canonical parameter (08-26); fan-in via junction |
| *(new)* | — | `spe_synthesis_links` | fan-in junction, ≥1 per specification |
| `specification_source_links` | 0 | `spe_source_links` ‡ | |
| `spec_value_probes` | 0 | `spe_value_probes` ‡ | a probe walks a value to its ceiling — that produces the number |
| `probe_population_links` | 0 | `spe_probe_population_links` ‡ | |

#### RENDER — `ren_` · **no hand-off object** (M-4)
| current | rows | → | note |
|---|---:|---|---|
| *(none)* | — | **`ren_items` ⊘ WITHDRAWN** | re-creates `render_manifest`, dropped by migration 046 on *"the entire pipeline is dynamic rendering on site"*. Render is terminal; nothing consumes from it. |
| `rooms` | 17 | `ren_rooms` | |
| `room_items` | 0 | `ren_room_links` † | junction — and `_items` now means something specific, so it must not keep that name |
| `case_studies` | 0 | `ren_case_studies` | |
| `case_study_outcomes` | 0 | `ren_case_study_outcomes` | |
| `case_study_strategies` | 0 | `ren_case_study_strategies` | |
| `case_study_populations` | 0 | `ren_case_study_population_links` † | junction |
| `case_study_specs` | 0 | `ren_case_study_links` † | **named for the specification, foreign-keyed to `items`** |
| `economics_entries` | 0 | `ren_economics_entries` | |
| `economics_entry_populations` | 0 | `ren_economics_population_links` † | junction |
| `economics_entry_specs` | 0 | `ren_economics_links` † | same fault |

#### SUBSTRATE — no prefix
`items` is retired as a table name; its rollup role is render's, and its 10 inbound FKs re-point.
**Whether `item_code` renames with it is Q2 and is not assumed here.**

| current | rows | → |
|---|---:|---|
| `term_aliases` | 2382 | unchanged — *proposed `term_alias_links`, withdrawn: `alias` is the payload* |
| `item_population_links` | 372 | re-pointed |
| `data_migrations` | 352 | unchanged |
| `decisions` | 166 | unchanged |
| `item_axis_links` | 158 | `item_demand_links` † — ruled |
| `term_item_links` | 147 | re-pointed |
| `slugs` | 106 | unchanged |
| `items` | 93 | **retired** ‡† |
| `terms` | 88 | unchanged |
| `lang_jur_map` | 70 | `language_jurisdiction_links` † |
| `population_axis_map` | 53 | `population_demand_links` † — ruled |
| `access_need_icf` | 43 | `access_need_icf_links` † |
| `populations` | 23 | unchanged — **but `MOB` → `AMB`/`WHEEL`** |
| `access_need_axis_map` | 21 | `access_need_demand_links` † — ruled |
| `axes` | 17 | `icf_demands` † — ruled |
| `access_needs` | 17 | unchanged |
| `weighting_profile` | 5 | `weighting_profiles` † |
| `access_duration` | 3 | `access_durations` † |
| `access_stakes` | 3 | unchanged |
| `life_stage_modifiers` | 2 | unchanged |
| `pipeline_runs` | 1 | unchanged |
| `item_population_elaborations` | 0 | re-pointed — note it points *into* evidence, inverting the substrate model |
| `situations` | 0 | **⊘** 0 rows |

**Net: 66 → 61 tables** (5 deletions, 3 creations, 1 fold, 1 retirement). Not a large reduction, and
that is correct — J.4's point is that **derivability, not count, is the metric.**

### 6.3 Constraint 1 — walkable in **both** directions

**Backward is free. Forward is not, and forward is the half that was missing.**

| direction | mechanism | cost |
|---|---|---|
| **backward** (`spe → syn → jud → evi → res`) | follow the NOT NULL FK / junction | free — the key *is* the pointer |
| **forward** (`res → evi → jud → syn → spe`) | **reverse lookup** on the same column: `SELECT … WHERE research_item_id = ?` | **a full table scan unless the column is indexed** |

**SQLite does not index a foreign key's source column automatically.** Declaring
`evi_items.research_item_id REFERENCES res_items(ref_id)` creates a constraint, not an index. So a
forward walk over 875 leads scans the whole extraction table per hop. **Every hand-off column and
every junction column gets an explicit index in the same migration that creates it.** This is not an
optimisation; without it the forward direction is unusable at the scale the clue store already has.

**"Write both ways" is the gap-driven walk, and it is a live requirement, not a hypothetical.**
R2 mines from confirmed anchors (forward); R14 and the gap register start from a missing
determination and walk *back* to the research that would close it. Both must be first-class:

```sql
-- forward gap: leads that produced no evidence            (needs idx on research_item_id)
SELECT r.ref_id FROM res_items r
  LEFT JOIN evi_items e ON e.research_item_id = r.ref_id WHERE e.ref_id IS NULL;

-- backward gap: specifications resting on no judgment     (needs idx on the junction)
SELECT s.ref_id FROM spe_items s
  LEFT JOIN spe_synthesis_links l ON l.specification_item_id = s.ref_id WHERE l.synthesis_item_id IS NULL;
```

**Neither query is expressible today** — that is the Part 4 defect stated as a work item rather than a
diagnosis. Both become one-liners the moment the hand-off columns exist, and both are the acceptance
tests for T-A3.

**Writes stay one-directional, and that is not a contradiction.** Rule 5's *"never write into a
completed stage"* governs the write path; the junction is written by the **downstream** stage as it
creates its own item. Walking backward is a *read*. Nothing in the bidirectional requirement asks a
synthesis to reach back and modify a judgment, and if it ever appears to, that is the copy rule 5
forbids wearing a different hat.

### 6.4 Constraint 2 — reference IDs, not surrogate integers

**Measured this session — 4 of the spine objects key on an INTEGER:**

| object | PK | type |
|---|---|---|
| `source_locators` | `ref_id` | **TEXT** ✓ |
| `evidence_sources` | `ref_id` | **TEXT** ✓ |
| `spec_value_probes` | `probe_id` | **TEXT** ✓ |
| `source_value_extractions` | `extraction_id` | **INTEGER** ✗ |
| `specifications` | `specification_id` | **INTEGER** ✗ |
| `search_executions` | `exec_id` | **INTEGER** ✗ |
| `convergence_assessment` | `convergence_id` | **INTEGER** ✗ |
| `bpc_metadata` | `slug` | TEXT, but it is the *topic*, not an identity |

A surrogate integer is not a pointer you can quote in prose, cite on a page, or carry in an
attestation. **Mint stable codes per stage** — `RES-NNNNN`, `EVI-NNNNN`, `JUD-NNNNN`, `SYN-NNNNN`,
`SPE-NNNNN` — following the pattern `dbcore.next_ref_id()` already establishes: **computed from the
high-water mark of the union, never stored.** A counter table would be a second home for a fact the
id columns jointly state (rule 5), and `dbcore.py:206-213` says so in its own docstring.

**A live latent defect, now on the critical path.** `source_locators` holds **11 malformed ids** —
`REF-VERIFIED-001` … `REF-VERIFIED-012` — and because `'V' > '0'` in string order they sort **above
every numbered id**:

```
naive  SELECT MAX(ref_id) FROM source_locators   →  REF-VERIFIED-012     ← wrong
dbcore.next_ref_id(conn)                          →  REF-00971            ← correct
```

**The allocator is safe; anything hand-rolled is not.** This is why `CLAUDE.md` rule 5's
*"do not compute it by hand"* is load-bearing, and why the 11 ids must be re-minted **before** the
per-stage allocators are written — otherwise the same trap is reproduced five more times.

### 6.5 Constraint 3 — render pulls across every stage

**"Render is terminal" was read too strongly, and needs one word of correction: render is terminal in
the *hand-off*, and omnivorous in *reads*.** M-4 stands — render produces nothing the next stage
consumes, because there is no next stage — but nothing in that limits what it may read, and the owner
is explicit that it must read everything.

**The mechanism is the view layer, and it is already the most protected object in the schema.**
`CLAUDE.md`: *a cross-stage view IS the pointer* — the owner's own *"for rendering a citation, we
point towards the evidence table for that reference ID"* is a description of a join. So render's reach
is not new apparatus; it is the pointer discipline applied at the last hop.

Part K's four-kind rule is correct and is adopted verbatim:

| kind | home | render's job |
|---|---|---|
| **pointed at** — citations, sources, governing refs | upstream rows | join |
| **computed** — comparative tables, see-also, counts | **a view** | call it |
| **generated** — any figure encoding a value | derived from the determination | generate |
| **authored upstream** — explanations | the stage that reasoned it | quote with its pointer |

**The two named cases resolve to views, not tables:**
- **Citations** — `spe_source_links → evi_sources → evi_source_authors`. Nothing new. **Never copy a
  bibliographic field into a render table**; that is the rule-5 violation the whole pointer series
  exists to remove, and the 2026-08-19 fabrication is what it looks like when it happens.
- **Jurisdiction comparison** — a view over `res_code_leads` × `spe_items` on the canonical parameter.
  **A comparison is a query result; storing one is §2(b) in tabular form.** It also means a
  comparative table can never disagree with the determinations it compares, because it *is* them.

**And this is where `ren_items` finally resolves — against itself.** Part K.5 argued for a page
manifest so a gate could ask *"does every claim on this page trace upstream?"* That gate is worth
having. **The manifest is not the way to get it.** Under dynamic rendering the renderer knows exactly
which rows it read, at render time — so page provenance is **computed, not stored**, and storing it is
a second home for what the template and its queries already determine. Migration 046's ruling
(*"the entire pipeline is dynamic rendering on site"*) and §1's *name what reads it* both point the
same way.

> **Resolution: `build_site.py --check` emits a per-page provenance record as a CHECK ARTIFACT, not a
> table.** K.3's gate is preserved in full; the table count does not rise. 046 forbade relying on
> artifacts *for rendering*; a check output is not relied on for rendering.

**One genuinely new table survives: `figures`.** A figure is a new row-kind (J.4), and the project
cannot express an accessible figure today — **no diagram, caption or alt-text column exists in any of
the 66 tables**, in a guidebook whose subject is access. Two non-negotiables carry over: a figure
encoding a value is **generated, never drawn** (else it is a second home for the determination), and
**`text_equivalent` is NOT NULL** — this project cannot ship a figure without one without
contradicting its own subject matter, and the schema should make that impossible rather than
discouraged.

### 6.6 Constraint 4 — minimize tables · **this reverses my own recommendation**

An hour ago this document said *"net 66 → 61, and that is correct — derivability, not count, is the
metric."* **The owner has now ruled that count is a metric. Superseded, recorded, and the design is
re-derived below.** The result is 66 → **48**.

**First, the honest refusal: the two obvious merges fail on measurement.**

| proposed merge | measured | verdict |
|---|---|---|
| the **7 "act" tables** → one `runs` with a `kind` (J.4's own rule) | they share **zero** columns — not one, not even `created_at`. Widths 23/13/12/18/16/12/29 | **REFUSED.** The merge yields one ~90-column table that is >80% NULL. That is not minimisation, it is concealment |
| the **4 "lead" tables** → one `res_items` with a `kind` | they share exactly **one** column, `notes`. Widths 20/32/14/11 | **REFUSED for now.** `reference_stubs` (0 rows) deletes outright; folding `jurisdictional_values`' 32 columns is a T-B column study, not a rename |

**So minimise by DELETION, which is where the real number is.** Nineteen tables, **verified this
session to hold zero rows between them**, are §1's burden of proof unpaid — added without naming what
reads them, and never used once:

| group | tables | why |
|---|---|---|
| **derivable duplicates** | `search_coverage`, `search_languages` | restate `search_executions.slug/jurisdiction/language`, and the first home is per-query — more precise. Rule 5 |
| **never written** | `reference_stubs`, `situations` | 0 rows, no writer |
| **empty act tables** | `gap_mining`, `supersession_check`, `url_verification_runs`, `item_audit_runs` | nothing reads or writes them; git is the archive for code, and these are code-shaped |
| **empty population junctions** | `extraction_population_links`, `probe_population_links`, `citation_population_links`, `case_study_populations`, `economics_entry_populations` | five of six are empty and near-identical in shape. Keep `item_population_links` (372 rows); re-create a sibling **when a stage actually needs one** |
| **empty case-study / economics satellites** | `case_study_outcomes`, `case_study_specs`, `case_study_strategies`, `economics_entry_specs` | premature: K.4 rules that a precedent **splits** — measured outcome to `evi_items` with a source behind it, narrative to render. These satellites encode the unsplit shape |
| **folded to a `kind`** | `connections`, `connection_targets` | J.2/K.4: *"when writing X, also consider Y"* is either an evidenced comparative synthesis (`syn_items`, `kind='connection'`) or a derivable see-also. It is unlikely to be a third thing |

**Kept deliberately, though empty:** `case_studies` and `economics_entries` — **research contract R12
names both by name** (*"Case studies → `case_studies`. Economics → `economics_entries`."*). Deleting a
table a live blocking contract instructs sessions to write to is not minimisation.

**The arithmetic:**

```
66  current
−19  deletions (all verified zero-row)
− 1  fold: evidence_population_match → columns on jud_items   (C6-4)
− 1  retire: items                                            (owner ruling)
+ 3  create: jud_items, syn_judgment_links, spe_synthesis_links
+ 1  create: figures                                          (§6.5)
───
 49  and 48 if `syn_synthesis_links` is deferred with comparative synthesis
```

**66 → 49, a 26% reduction, with no dissimilar tables jammed together and no foreign key lost.**
Every deletion is evidenced (zero rows, no reader, or a more precise first home), which is exactly
what §1 asks for: *"You need evidence — that it is unreferenced, or vacuous after a real batch, or
superseded — not permission."*

**And the 33-empty-tables figure is the finding underneath the constraint.** Half the schema has never
held a row. That is not principally a naming problem — it is §1's burden of proof unpaid 33 times.
Minimising is not tidying; it is paying a debt.


---

## PART 7 — The execution plan

**Two tracks, deliberately not bundled (C5).**
**Track A — the spine.** Zero rows, zero replay collisions, one ordinary migration. Has a deadline
(I.7). **Track B — the nomenclature sweep.** 24 collisions, 1,179 live rows, `AFTER_DATA`-solvable,
no deadline.

Model floor: **Opus** for anything designing or writing a determination, synthesis, or schema shape;
**Sonnet** for mechanical sweeps, renames with a derived caller list, register updates. Never
`best_practice_synthesis` below the Opus floor.

---

### T-0 — Unblock every rename (Sonnet) · no ruling · do first

| # | Task |
|---|---|
| T-0.1 | **De-hardcode `migration_reproducibility.py`.** Lines 58–62 and the `needed` set at 137–138 hardcode `citation_mining`, `connections`, `items`. Derive from `sqlite_master` or a registry entry. A §2(b) fix on its own merits, and it breaks on **any** rename. |
| T-0.2 | **Fix U-7.** `evidence_population_match.source_ref` vs `ref_id`, 25/25 identical. Grep `scripts/migrations/data_*` for the column **first**, then writer-retire → reader-retire → NULL forward. |
| T-0.3 | **Fix `record-command.py`.** Mint the scratchpad directory from `session_id` rather than selecting an existing one. Already documented in `NOTES.md` / PR #122. |
| T-0.4 | **Build the rename-sweep helper.** Given old → new, report every non-archived caller: tree, `sqlite_master` (**a view is a caller** — migration 064 exists because a sweep missed `v_item_provenance`), `check-registry.yaml` `basis:` refs, `skills/`. |

**Acceptance:** `run_checks.py --changed-from origin/main --explain` green **and** `--selftest` green.
Run both — `--changed-from` does not run the selftest, and the selftest is where a rename fails.

**§1 payment for T-0.4:** without it a rename ships dangling callers. That has happened twice, and a
dangling view reader renders nothing — which a byte-exact diff certifies clean, because the table has
0 rows.

---

### T-A1 — Land the six-stage spine in the machine (Opus) · no ruling · resolves U-1, M-6

**One commit.** Piecemeal is the trap that cost a cycle on 2026-08-25.

| # | Task |
|---|---|
| T-A1.1 | Add `specification` to `pipeline-contract.yaml`, between synthesis and render. Anchor: `conceptual-model.md:90` — *"BPC synthesis produces specifications"*, in the entity model since the baseline. Entry: *a synthesis with a resolved value, ready for determination*. |
| T-A1.2 | **Move four criteria from `judgment` to `specification`** — `governing-refs-nonempty`, `no-regulatory-stratum-stated`, `tier3-alone-threshold`, `derivation-handshake`. All enforced by `validate_evidence_state.py` against `specifications`. `convergence-independence` stays with judgment. (M-6.) |
| T-A1.3 | `pipeline_completeness.py`: `STAGES` → six; re-point the ten `specifications` queries (70, 147, 149, 152, 158, 161, 184, 187, 201, 221); **rename `items_judged`**, which counts specification rows and calls them judgments. |
| T-A1.4 | Re-point `check-registry.yaml` `basis:` refs — live today: `judgment/tier3-alone-threshold` → `specification/...`, plus any other moved by T-A1.2. **C7 in `--selftest` catches this and `--changed-from` does not.** |
| T-A1.5 | Correct `CLAUDE.md`: remove the "machine has not caught up" paragraph; apply M-4 — **the hand-off rule binds stages 1–5**. |
| T-A1.6 | Assert the `stage_id[:3]` prefix derivation yields six distinct codes **in the selftest**, not in prose. |

**Acceptance:** `--selftest` green; `pipeline_completeness_fresh` green with `EXAMINED: n > 0`; no
five-stage list outside `_archived/` and `sessions/`.

---

### ⛔ GATE — three questions, asked together, once

Each answerable in one word; the measurement is already done.

> **Q1 (C2) — evidence → judgment cardinality.** Your words: *"each row of evidence provides one row
> for judgment."* Two readings. **(a)** one evidence row yields at most one judgment — **contradicted
> by live data**: `evidence_population_match` holds 25 grades across 10 sources. **(b)** each judgment
> traces to exactly one evidence row — **consistent with all 25**, and it preserves the dissent
> contest `add-population-match` deliberately allows. We propose **(b)**: `evidence_item_id NOT NULL`,
> **no** UNIQUE, with those 25 grades becoming 25 judgment rows. **Confirm (b), or say (a).**
>
> **Q2 (M-5) — does `item_code` rename with `items`?** You retired `items` because *"the word was the
> ambiguity."* `item_code` carries **10 inbound foreign keys** and the ruling does not touch it, so a
> reader still meets `judgment_items.item_code`. **We recommend table-only now, column later** — it is
> separable and Q1 is on the critical path.
>
> **Q3 (M-3) — prose in files, or in rows?** Decides where `syn_items.synthesis` lives. Measured: the
> status quo is **already files** — `best_practice_synthesis` is named across governance and is a
> column nowhere; `bpc_metadata`'s 16 columns are all process metadata; text lives at `slugs.bpc_path`.
> **Ratify files, or reverse to rows?**

**Not blocking, but worth telling you:** M-4 — render is terminal, so it produces no hand-off object
and `ren_items` stays withdrawn (it re-creates `render_manifest`, which migration 046 dropped on your
*"the entire pipeline is dynamic rendering on site"*). We proceed on **five** hand-off objects.

---

### T-A2 — Mint the spine (Opus) · blocked on Q1, Q2 · resolves U-2, U-6

**One ordinary schema migration `065_the_item_spine.sql`. No baseline. No `AFTER_DATA`** — measured:
**0 of 33 data migrations reference any table this touches.** Bump `user_version` to 65. Mirror into
`schemas/*.py` in the same commit — drift is a bug, not a convention.

| Stage | From | To | Hand-off |
|---|---|---|---|
| research | `source_locators` | `res_items` | — (origin) |
| evidence | `source_value_extractions` | `evi_items` | `research_item_id` **NOT NULL** |
| judgment | **new** | `jud_items` | `evidence_item_id` **NOT NULL**, no UNIQUE |
| synthesis | `bpc_metadata` | `syn_items` | `syn_judgment_links` (≥1) |
| specification | `specifications` | `spe_items` | `spe_synthesis_links` (≥1) |
| render | — | — | **none** (M-4) |

**`jud_items` column set (M-2) — derived, not invented.** Every column carries a fact `specifications`
already needs and cannot source, plus the 25 grades folded in per C6-4:

```
judgment_id            TEXT PRIMARY KEY
evidence_item_id       NOT NULL REFERENCES evi_items(extraction_id)   -- the hand-off
item_code              NOT NULL REFERENCES items(item_code)           -- pending Q2
population_code        NOT NULL REFERENCES populations(population_code)
tier_assessed          NOT NULL   -- CHECK from the schema, never a list in code
population_match_grade NOT NULL   -- in from evidence_population_match
study_population                  -- in from evidence_population_match
sample_size                       -- in from evidence_population_match
mismatch_note                     -- in from evidence_population_match
directness
weight
soundness              NOT NULL   -- is the extraction sound? the stage's whole question
dissent_of             REFERENCES jud_items(judgment_id)   -- the contest, made explicit
rationale
created_at / created_by_session / updated_at / updated_by_session
```

`dissent_of` is what makes reading (b) safe: a dissenting grade is a **second judgment naming the one
it contests**, not merely a second row sharing a parent. That reads as a contest to a human *and* to a
gate, and it survives even if Q1 comes back (a).

**Two existing tables need create-new → copy → drop → rename** (add NOT NULL FK): `evi_items` and
`syn_items`. **Both hold 0 rows**, so it is trivial. Everything else is `ALTER TABLE RENAME`, which
rewrites `REFERENCES` and view bodies for you.

**Acceptance:** `migrate_db.py --rebuild /tmp/rebuilt.db` reproduces byte-identically; `--selftest`
green; `PRAGMA foreign_key_check` empty; and **≥1 inbound FK now lands on each of the five hand-off
objects** — the exact inverse of Part 4's table, and the only test that proves the defect fixed.

---

### T-A3 — Walk one slug end to end (Opus) · **the real gate on T-A2**

**C1's resolution, and the most important phase here.** T-A2 is not done until T-A3 passes.

Drive one slug through all six stages via `scripts/db.py` subcommands only — scratch copy,
`GUIDEBOOK_DB_PATH` inline on every call, then `emit_batch_sql.py` → `emit_data_migration.py` →
`migrate_db.py`. Never hand-write SQL against a table the CLI can reach; a table it cannot reach is a
coverage bug to fix, not a licence to bypass.

**Acceptance — all four, or the spine is unproven:**
1. One SQL join walks `res_items → evi_items → jud_items → syn_items → spe_items` using **only
   hand-off keys**, never `slug`, returning ≥1 row.
2. A rendered figure resolves to its extraction and its paper **by key path alone** — Part 4's defect,
   demonstrated fixed.
3. Every stage reports `EXAMINED: n > 0`. A vacuous pass here is the §2(a) failure produced four times.
4. `db.py` **refused** at least once. A writer that only ever succeeds is not being tested.

---

### T-B — The nomenclature sweep (Sonnet; Opus for the population split) · after T-A3

**This is where the 24 collisions live.** Every rename migration here declares
`-- AFTER_DATA: <last data migration ts>` so it runs after every data migration
(`migrate_db.py:282–320`).

| # | Task | Model |
|---|---|---|
| T-B.1 | `axes` → `icf_demands` (§R8) **with** the paired `retired-vocabulary.yaml` entry — the register entry is part of the rename, not a follow-up. Sweep `validate_axes.py`, `functional-taxonomy.md`, `context-map.yaml`, the three `*_axis_*` tables. | Sonnet |
| T-B.2 | `MOB` → `AMB`/`WHEEL`, 31 links fanning to 62. **Population taxonomy is DG-NON — a judgement about the book.** | **Opus** |
| T-B.3 | Sweep the **9** skills teaching `MOB`, and the **17** teaching retired population codes. **A skill is a caller.** | Sonnet |
| T-B.4 | The research/evidence renames per Part 6.2 — 10 tables, 24 colliding files, one `AFTER_DATA` marker. | Sonnet |
| T-B.5 | The deletions: `search_coverage`, `search_languages`, `reference_stubs`, `situations` (all 0 rows), and retire `search_admissions` with the `v_source_admission` rewrite. **Ask which stages each view spans before dropping anything** — a cross-stage view *is* the pointer. | Sonnet |
| T-B.6 | `items` retirement per Q2; re-point the 10 inbound FKs. | Sonnet |
| T-B.7 | J.1's `origin` + `parent_item_id` on `res_items` — this closes the stranded-mining-yield defect (138 DOIs harvested, 4 reached the clue store) rather than adding apparatus. | Opus |

**Acceptance:** the T-0.4 helper reports **zero** non-archived callers of every retired identifier;
`--selftest` green; `retired-vocabulary.yaml` carries an entry per retired token; `--rebuild`
byte-identical.

---

### T-C — Propagate the record (Sonnet)

| # | Task |
|---|---|
| T-C.1 | Rewrite `workplan/2026-08-22-master-execution-plan.md` around T-0…T-B, or supersede it into `workplan/_superseded/`. (M-7.) |
| T-C.2 | **One** consolidating DR — six-stage spine, `-item` spine, cardinality. Not four. (M-8.) |
| T-C.3 | Attestation for the `decisions/` write, per rule 2. |
| T-C.4 | Re-derive the stage→table map against **six** stages. Every assignment written before 2026-08-27 predates the ruling. Derive; do not read one out of a document. |
| T-C.5 | Re-derive and re-stamp `CLAUDE.md`'s three dated figures (43/37 keys on eight columns; five cross-stage views). All change at T-A2. **State the substrate-is-not-a-stage convention whenever quoting the view count.** |

---

## PART 8 — Standing rules this review earns

**S-1 · A ruling is not landed until the machine that enforces it agrees.** Four rulings in three
days; the database moved zero times. **A ledger entry records a decision; it does not execute one**,
and this repository currently treats writing the entry as completing the work. Every ledger entry
should carry an execution status beside its CONDITION and ACTION, and a check should read it. This is
the generalisation of U-1…U-6 and the window's defining failure.

**S-2 · A hand-off key between two empty tables is unproven, not working.** Rule 4 says a 0-row object
is unproven; this extends it to constraints. With 33 of 66 tables empty, **structural work is accepted
by a walk, never by a migration applying green.** That is why T-A3 gates T-A2.

**S-3 · Put the measurement, not the question.** Q1 and Q3 were both recorded as open owner questions;
both were answerable by counting. **A question sent up without its measurement costs a round trip and
invites a ruling made without the fact.**

**S-4 · When a remedy does not serve the reason given for it, say so before executing.** M-5: `items`
was retired because *"the word was the ambiguity"*, and the remedy leaves `item_code` on 10 inbound
keys while minting five tables containing that word. Rule 0 governs and the ruling stands — but you
owe the owner the observation **before** spending a migration.

**S-5 · Price a migration strategy before adopting it.** Part I recommended a full baseline on three
arguments; all three failed on measurements that took one session and had never been run — the
`ALTER TABLE` limit is two empty tables not 66, `AFTER_DATA` already exists and is in use, and the
collision count partitions the work so the urgent half costs nothing. **The strategy question is
always a measurement, and the measurement is cheap.**

---

## PART 9 — What the four adversarial reports refute, **including in this document**

I had sampled the last session's output. Read in full — `NOMENCLATURE.md` Parts A–L and all four
audit reports, 4,900 lines — five of my own claims above are refuted and four design decisions
change. **Where Part 9 and an earlier part disagree, Part 9 wins.** The earlier text is left in place
rather than overwritten, because the failure mode matters more than the tidiness.

### 9.1 Corrections to this document

| # | I wrote | Refuted by | The correct form |
|---|---|---|---|
| **X1** | "No foreign key lands on any stage's hand-off object" (Part 4) | **A1-O2** | **Two same-stage FKs do** — `extraction_population_links → source_value_extractions` and `specification_source_links → specifications`, exactly as my own table showed (1 and 1). The defensible claim is *no **cross-stage** FK lands on a hand-off object.* Corrected inline. |
| **X2** | "The schema is a star, not a chain — stages are joined by a topic label, not by what the previous stage made" (Part 4) | **A2-W2** | **Overclaimed.** `search_admissions(exec_id → search_executions, ref_id → evidence_sources)` **is a keyed cross-stage research→evidence edge** and it works today. So "the walk has no keys" is **false for the first hand-off**. And `specifications.convergence_id → convergence_assessment` is a specification-stage row keyed to a synthesis-stage product under the six-stage map — the closest thing to a hand-off key in the schema. What is actually missing is the **lead-level** edge and **everything downstream of extraction**. |
| **X3** | C2's antagonist: "25 rows across 10 sources proves fan-out exists in live data" | **A2-B0.1, A3-F18** | **The measurement does not reach the question.** `evidence_population_match` keys `ref_id → evidence_sources` — it grades a **source**, not an extraction. It is a different edge entirely. Since `source_value_extractions` holds **0 rows**, the evidence→judgment cardinality has **no live instance at all** and cannot be settled by measurement. Q1 is a genuine design question, not a countable one — see 9.2. |
| **X4** | C6-4: "fold `evidence_population_match` into `jud_items` as columns" | **A3-F18, A2-W4, A1-O1** | **Refuted on grain.** The grade is per **source**; `jud_items` is per **extraction**. Folding either copies one grade across N extractions (rule 5) or re-grades per extraction (re-reasoning). **Keep it as a satellite keyed on the source** — `jud_population_grades` — which is Part E's own position. My "resolution" of E-vs-J was wrong and E was right. |
| **X5** | §6.6: "33 empty tables = §1's burden unpaid 33 times… minimising is paying a debt" | **A2-W3** | **Contradicts rule 4 and my own Part 1.** *"Treat a 0-row object as unproven, not clean"* cuts both ways, and the 2026-08-25 correction spelled it out: *"EMPTY IS NOT DEAD — render surfaces awaiting data."* Most of the 33 are the **ordained pre-synthesis state** — the same emptiness Part I calls "the window" and I called "the opportunity" four sections earlier. The count proves nothing about *which* are unpaid. **The deletion set shrinks accordingly — 9.5.** |

**One claim of mine survives and is worth naming, because A4 says the source document failed it.**
A4-B9 finds that `jud_items` and the junctions **fail §1's burden of proof as written** — justified
in apparatus language, never stating what reaches the book. **Part 4 of this document pays it**: a
rendered figure that cannot be traced to its extraction cannot be checked by a reader or a gate,
which is how five fabricated citations passed six green gates. A4 names the second half I should add
explicitly: **a determination built on ungraded, unweighed extractions.** Both are book harms. The
burden is paid; it must be paid *in those words* in the migration header.

### 9.2 Q1 is reframed — it cannot be answered by counting

X3 removes the measurement I offered. What remains is a genuine design question, and A2-B0.3 supplies
a third option neither the source document nor my draft considered:

| edge | owner's words | options |
|---|---|---|
| evidence → judgment | *"each row of evidence provides one row for judgment"* | **(a)** `UNIQUE(evidence_item_id)` — literal 1:1, abolishes dissent · **(b)** NOT NULL, no UNIQUE — permits dissent, exceeds the sentence |
| judgment → synthesis | *"one-to-many rows of judgment provide one row for syntheses"* | **(c)** junction, no UNIQUE — implements **M:N**, *exceeds* the ruling · **(d)** junction **with `UNIQUE(judgment_item_id)`** — implements N:1 **exactly as ruled** |

**A2's charge of selective literalism is fair and applies to my draft too.** The source document read
the sentence as law where it supported junctions and as loose description where it did not; I
inherited that. **(d) is almost certainly right and was never on the table** — it satisfies the
owner's N:1 exactly, is written by the downstream stage, and keeps every guarantee the junction was
chosen for. **Recommend (d) outright; put only (a)-vs-(b) to the owner**, and put it as a design
question about dissent, with no false measurement attached.

**And record what the owner did *not* say.** A4-B3 and A2-B1: the quoted rulings cover **naming** and
**cardinality**. *"The hand-off is a NOT NULL foreign key"* is **agent design under an owner banner**.
So is **specification → render N:1**, which the owner's sentence never reaches and which is probably
wrong on the merits — one specification appears on many surfaces and one surface draws on many
specifications, i.e. M:N. Under M-4 that junction does not exist at all, which disposes of it.

**A2-B1 also notes the owner said *column*:** *"an 'item' in evidence is just under column called…
evidence-item."* **This bears directly on "minimize tables."** Read literally, the hand-off is a
column on existing tables — which is what four of the five actually are (two renames + two NOT NULL
columns). Only `jud_items` is a genuinely new table, and the junctions are the interpretation. Worth
naming to the owner rather than assuming.

### 9.3 Four key placements change

| # | as drafted | refuted by | corrected |
|---|---|---|---|
| **K1** | `evi_items.research_item_id NOT NULL` | **A3-F3** | **Wrong table.** The lead→paper edge is **source-grained**; putting it on the extraction copies one fact into every extraction from that paper, with divergence representable. And **six admitted sources have no clue-store row** (`REF-00965`–`REF-00970`), so the NOT NULL is unwritable for any extraction from them — the escapes are refusing to extract, or backfilling retroactive provenance, which is the §2(c) class with paperwork. **Hang it on the admission: `evi_sources.research_item_id`.** Reach the lead from an extraction by join. |
| **K2** | `syn_items` = renamed `bpc_metadata` | **A3-F10** | **`bpc_metadata`'s PK is `slug`.** The junction would key on a slug string, and J.2's comparative syntheses need **multiple rows per slug**, which PK `slug` forbids outright — as does `population NOT NULL`. **The re-key (minted `SYN-NNNNN`, slug demoted to an attribute) is mandatory** and is stated nowhere in the source. |
| **K3** | junctions "≥1 required" | **A3-F2** | **Not expressible in SQLite.** No FK, CHECK, or trigger can require a parent to have a child — and a trigger fires *before* the downstream stage writes the links. **The invariant needs two named owners:** a transactional writer (`db.py add-synthesis --judgment-items REF…` that **refuses** without ≥1 and writes item+links in one transaction) and a **blocking registered check** scanning for zero-link items, printing `EXAMINED:`. DDL alone cannot carry it. |
| **K4** | `figures.text_equivalent NOT NULL, always` | **A3-F12** | **NOT NULL "always" mandates a rule-5 violation.** For `kind='generated'` the text equivalent restates the value the figure encodes; stored as an authored row it drifts the moment the spec moves — the exact defect K.3 names for the image, reproduced in the alt text. **Store `text_equivalent` for `kind='asset'` only; generate it for `kind='generated'` from the same determination, by the same code path.** Also: per-stage junctions, never `figure_links(target_kind, target_id)` — that is the polymorphic key J.4 forbids; plus the conditional CHECKs, a refusing `add-figure` writer, and a stage prefix (`ren_`). |

### 9.4 A ratified record this plan must supersede explicitly, or stop

**A3-F4, and neither the source document nor my draft mentioned it.** Making `source_locators` the
research hand-off makes it **the root of every citation walk**. But migration 062's header, carrying
**DR-2026-08-06**, demoted the clue store: *"not stored as usable for any case unless it is being
read by a researcher… **Nothing joins it, no determination may cite it.**"*

875 rows whose `recovered_from` defaults to `'corpus-pre-reset-2026-08-06'` — the corpus whose
bibliographic fidelity is exactly what failed in §2(c). **The `-item` ruling does not resolve this:**
the owner named the stage's hand-off object; *identifying* it with `source_locators` is a derivation,
and it collides with a ratified record. Under rule 0 that needs a **recorded supersession, not
silence.** Either outcome of leaving it unrecorded is bad: the key ships and the wall is breached
quietly, or a later session greps the DR and refuses the migration.

**Required, in the migration header and the ledger:** one paragraph distinguishing what becomes
joinable (the lead's **identity**, as provenance-of-discovery) from what stays non-citable (the
lead's **bibliographic fields**), plus a writer refusal — admission **PROMOTEs** the lead
(`status='PROMOTED'`) before anything downstream may reference it. **This is a T-0 item, not a T-A2
one:** it gates the design, not the DDL.

### 9.5 §6.6 minimization, corrected — the honest menu

X5 removes the blanket argument. **Emptiness alone is not evidence of an unpaid burden**, so the
19-table deletion set collapses to what is individually evidenced. Three tiers:

**Tier 1 — delete now, evidenced on grounds other than emptiness (6 tables):**

| table | ground |
|---|---|
| `search_coverage` | rule 5 — restates `search_executions.slug/jurisdiction`, and the first home is **per-query**, more precise |
| `search_languages` | rule 5 — same, for `language` |
| `reference_stubs` | 0 rows **and no writer** |
| `situations` | 0 rows **and no writer** |
| `connections`, `connection_targets` | design fold (J.2/K.4): an evidenced *"also consider Y"* is a comparative synthesis-item; a navigational one is derivable. Not a third thing |

**Tier 2 — delete only after a writer/reader check (11 tables).** All are empty, but A2-W3 says that
proves nothing. Each needs the T-0.4 sweep run against it first: `gap_mining`,
`supersession_check` *(note: `bpc_metadata.supersession_check_complete` references the act — likely
awaiting synthesis, not dead)*, `url_verification_runs`, `item_audit_runs`, and the five empty
population junctions, `case_study_specs`, `economics_entry_specs`.

**Tier 3 — do NOT delete:** `specifications`, `bpc_metadata`, `source_value_extractions`,
`convergence_assessment`, `external_root_registry`, `reasoning_doc_citations`, `item_bpc_links`,
`spec_value_probes`, `specification_source_links`, `room_items`, `case_studies`,
`economics_entries`. These are **ordained empty** — the downstream stages the whole plan exists to
fill — and `case_studies`/`economics_entries` are named by live research-contract **R12**.

**And `search_admissions` moves from "retire at T-B" to KEEP, on a stronger ground than I gave.**
Per X2 it is the **only keyed cross-stage edge in the schema**. A2-W5 adds the decisive point:
J.3's premise for deleting it — *"the lead names its search"* — is **false today and proposed
nowhere**; `source_locators` has no exec column, and neither `origin` nor `parent_item_id` supplies
one. Delete it and `search_executions.admitted_ref_ids` — a **packed JSON list** — becomes the only
home of the admission edge. **The worse home would win by deletion.**

**Revised arithmetic — stated as a range, because Tier 2 is unresolved:**

```
66  current
− 6  Tier 1 deletions (evidenced)
−11  Tier 2 (only if the sweep clears them)
− 1  retire: items                    (owner ruling; and see 9.6)
+ 1  create: jud_items
+ 2  create: syn_judgment_links, spe_synthesis_links
+ 1  create: figures
───
 63  if only Tier 1 clears        ·        52  if Tier 2 clears entirely
```

**Not the 49 I claimed.** The honest range is **52–63**, and the difference between the ends is a
sweep nobody has run. **The real minimization lever is not deletion at all** — it is J.4 applied to
the two families A2-B2 names, which my C6 under-counted: the **four lead tables** (J.3 declares them
one row-kind; Part E keeps three) and the **act tables** (J.1 declares a mining pass "a search with a
different origin"; Part E keeps two). Both folds need the column studies §6.6 refused to hand-wave —
and both are worth more than every deletion combined.

### 9.6 `items` — the retirement may be the wrong remedy, and A3 says why

**A3-F11**, on keying specifications from `parameter_canonical`: **the remedy recreates `items`.** A
registry of design parameters keyed by a label, landing in the same migration that retires `items`
*for being a registry of design parameters*. Five problems: homonyms ("clear-width" of a doorway vs a
corridor is one string); no stability (correcting a canonical form rewrites a PK and every junction
row); the CHECK branch puts one vocabulary in two homes (rule 5); and the grain cannot state the
project's own worked case — ramp gradient, **ambulant vs wheeled**, an opposed demand *on one
parameter*.

**Smallest fix, and it should go to the owner with Q2:** a substrate registry minting **stable
parameter codes** (`code` PK, `canonical_label` UNIQUE), both stages FK the code. That is `items`
**re-grained**, not retired — which serves the ruling's stated reason (the ambiguous *word* goes)
without recreating the table under a worse key. **Q2 should be re-put in those terms.**

### 9.7 Additions to the plan that the audits force

| # | into | what |
|---|---|---|
| **A** | **T-0.4** | The caller sweep list must **name** what Part G omitted: `scripts/generate/{build_site,spec_page,population_page,generate_parts,pilot_renderings}.py` · `scripts/validate_items.py` (a registered check named for the table) · `scripts/audit/{migration_reproducibility,pmp_audit,graph_audit,graph/extract_db}.py` · `scripts/tests/{test_db_integrity,test_evidence_cell_state_2_3,test_validate_evidence_state_2_4}.py` · `tools/{pipeline_completeness,evidentiary_audit,regenerate_vetting_surface}.py` · **four** governance YAMLs (`check-registry`, `context-map`, `pipeline-map`, `retired-vocabulary`) · 3 views reading `items` · 22 skills. **This is the 064 failure class being re-armed by the document that cites 064 as its cautionary tale.** |
| **B** | **T-0.1** | `migration_reproducibility.py`'s invariant list is annotated *"Keep this list and the DR in sync; it is the contract"* — so de-hardcoding is a **contract/DR change**, not a grep-and-replace. Its own selftest hardcodes `items` in six places. |
| **C** | **T-A2** | **No writers exist** for any keyed object — `add-extraction`, `add-synthesis`, `add-specification`, `add-figure` and every junction writer are absent (A3-F16). Creating refusal-less keyed tables re-opens the hand-SQL gap §4 closed and through which the 2026-08-19 fabrication entered. **Writers ship with the migration, in one sequencing statement.** |
| **D** | **T-A2** | `res_items.origin` cannot default to `'searched'` — 875 rows have **no record of where they came from**, so a backfill would assert unknown provenance (§2(c) in a column). The vocabulary needs an explicit **`unknown-legacy`** value (A3-F17). |
| **E** | **T-B** | `spec_value_probes` moves to specification **without a re-key**, keeping the mis-key Part B itself condemned (*"reaches past the extraction to the paper"*). A probe in the specification stage should consume synthesis/judgment items (A2-W4). |
| **F** | **T-B** | `evidence_population_match.target_population` / `study_population` carry **no FK to `populations`** (A2-W5) — fix in the same migration that renames the table. |
| **G** | **T-B** | `source_value_extractions.promoted_to_rdc_id → reasoning_doc_citations` is an **evidence-stage column pointing downstream into synthesis**, filled after the extraction completes — the exact "write into a completed stage" anti-pattern Part B invokes to reject back-pointers, **sitting on the proposed `evi_items` itself**, unflagged in 877 lines (A2-W4-iii). |
| **H** | **new, T-C** | No check compares `sqlite_master` table prefixes against `pipeline-contract.yaml` stage ids. The stage list changed **twice in 72 hours**; the prefix derivation runs once at christening and is then **stored in 60+ table names** — a second home with no drift detector (A2-W6). Add the check, or the rename is a one-time correctness event with no guard. |

### 9.8 The `site_pages_fresh` promotion — sequencing hazard, not a free win

L.6 offers it as step 1, *"free today."* It is, **and it becomes a guaranteed CI break at T-B.**

`build_site.py` walks `SELECT item_code FROM items`; `FP_TABLES` names `items`, `specifications`,
`specification_source_links`, `item_bpc_links`, `item_population_links` — **five of seven tables the
rename touches.** Promote it to blocking first and the rename turns `main` red on
`no such table: items`, or worse passes vacuously (§2(a)).

Two further corrections to how it is described: **"nothing calls it" is false** — `ci.yml:251` runs
the render battery on every gated run, so it *has* been running and reporting, advisory. The accurate
claim is that **no regeneration script invokes `build_site.py`**. And it guards **`site/specs/`
only** — 93 of ~121 reader-facing files; `site/populations/` (11) and `site/rooms/` (17) have
driverless generators, and `room_page.py` crashes against the live schema.

> **Sequence: promote it in the *same* commit that rewrites the generators (T-B), never before.**
> And engage the registry's **recorded** reason for advisory status — *"advisory until the
> committed-vs-generated policy is settled"* — rather than promoting past it unexamined, which A4-B9
> rightly calls the inverse of arguing paperwork against a ruling.

### 9.9 Two measurement conventions I must state, having criticised others for not stating theirs

**Collision counts depend on the definition, and mine was the narrow one.** Re-measured both ways:

| table | DML-only (`INTO/UPDATE/FROM/TABLE <name>`) | any mention |
|---|---:|---:|
| `items` | **0** | 9 |
| `specifications` | **0** | 3 |
| `bpc_metadata`, `source_value_extractions` | **0** | **0** |
| `evidence_sources` | 14 | 19 |
| `source_locators` | 3 | 14 |
| `citation_mining` | 5 | 7 |

**DML-only is the correct definition for the replay question** — replay breaks only when a migration
*executes* SQL against a name that no longer exists; a mention in a header comment does not. A3-F9
reports the any-mention figures (19/14/9), which is why its numbers differ from mine. **C5's headline
holds under the operative definition and I should have stated it: the spine tables carry zero
*executable* references in the 33 data migrations.**

**And the cross-stage view count is five, not seven — under a convention that must always be
stated.** `NOMENCLATURE.md` Part H still says seven and was **never updated** after the ledger
corrected it the same day. Since substrate is not a stage, `v_coverage_priority` (research +
substrate) and `v_item_extractions` (evidence + substrate) cross nothing. A2-B3 supplies the argument
that settles it: **if substrate joins counted as crossings, 41 of 80 FKs point into substrate and the
protection rule would cover nearly every view — vacating it.** A correction that reached the ledger
and not the document it corrects is the same defect this whole review is about.


---

## PART 10 — STRICT NOMENCLATURE THAT DIRECTS WIRING

**Owner statement, 2026-08-27, recorded on contact:**

> *"We need to radically rewrite our table names and column headers, consolidate them as required
> based upon phase, and ensure the nomenclature is strict and directs wiring."*

This escalates the scope from table names to **876 columns**, and it adds a criterion the previous
parts did not have: a name must **direct wiring** — tell a reader, and a script, what it keys to.
That is testable, so it is measured first.

### 10.1 The wiring surface, measured

| | value | command |
|---|---:|---|
| Columns | **876** across 66 tables | `PRAGMA table_info` over all |
| Distinct column names | **480** | — |
| Key-shaped names (`_id`/`_code`/`_ref`/`_key`) | **114** | |
| — legitimate foreign key | 64 | `PRAGMA foreign_key_list` |
| — legitimate primary key | 37 | `PRAGMA table_info` pk flag |
| — **neither: a promise of a join that does not exist** | **13 (11%)** | key-shaped ∧ ¬FK ∧ ¬PK |
| Packed-reference columns (many refs in one cell) | **7** | |
| FK columns whose name does **not** name their target | **6** | |

*Convention, stated because §2(b) requires it: "key-shaped" is the four suffixes above; a primary key
is counted legitimate even when unreferenced. **An earlier pass of this section reported 38%** by
counting all 37 primary keys as liars. Corrected before publication — the honest figure is 11%.*

**The thirteen liars, in full** — every one is a name that tells a reader to join and gives them
nothing to join to:

```
conflicts.gap_id                     evidence_sources.local_id
evidence_population_match.source_ref evidence_sources.superseded_by_ref_id
item_population_links.rationale_ref  items.item_id            ← a second key-shaped column on `items`
jurisdictional_values.spec_id        situations.account_text_ref
situations.translation_ref           source_slug_links.local_ref_id
source_value_extractions.root_id     spec_value_probes.walk_id
supersession_check.local_ref_id
```

Two deserve naming separately. **`local_ref_id`** (3 tables) holds `RAP-01` — a within-document
citation label, **not a `REF-` at all**: the name lies about both its target *and* its namespace.
**`items.item_id`** sits beside `items.item_code` on the same table, so the one table the whole
`-item` ruling is about carries two key-shaped columns and no statement of which is the identity.

**The seven packed-reference columns** — references hidden inside text cells, invisible to every FK,
join and gate:

```
search_executions.admitted_ref_ids     supersession_check.superseding_ref_ids
specifications.governing_refs          slugs.serves_axes
situations.attaches_axes               source_locators.used_in_bpcs
reference_stubs.used_in_bpcs
```

`specifications.governing_refs` is the one that reaches the reader: it is the provenance of a
rendered determination, stored as unparseable text. **Part 4's book harm is this column.**

**And the vocabulary sprawl the consolidation has to fix** — one concept, many names:

| concept | distinct names live | the names |
|---|---:|---|
| timestamp of the act | **7** | `created_at` 49 · `attempt_at` · `executed_at` · `completed_at` 2 · `checked_at` · `last_updated` · `url_last_fetched` 2 |
| free-text remark | **7** | `notes` 26 · `note` 6 · `rationale` 3 · `mismatch_note` · `root_population_note` 2 · `findings_note` · `deferred_reason` 2 |
| who did it | **4** | `created_by_session` 47 · `updated_by_session` 23 · `attempted_by_session` · `session` 3 |
| a status | **8** | `status` 16 · `state` · `disposition` · `extraction_status` · `evidence_state` · `verification_status` · `doi_resolution_outcome` 2 · `url_resolution_outcome` 2 |

**The audit quartet is not uniform:** `created_at` on 49 tables, `created_by_session` on 47,
`updated_at` on 24, `updated_by_session` on 23. Four different footprints for one convention.

### 10.2 The five laws

Strict means **mechanically checkable**. Each law below is written so a script reading only
`sqlite_master` can decide it — no judgement, no list to maintain.

> **LAW 1 — A key-shaped suffix is a promise, and the promise is `_id`.**
> A column ends in `_id` **if and only if** it is this table's primary key or a foreign key.
> `_ref`, `_key` and bare `_code` on a non-key column are abolished. Nothing else may look like a key.
> *Fixes all 13 liars. Checkable: `keyish(col) XOR (isPK ∨ isFK)` must be empty.*

> **LAW 2 — A foreign key is named for the table it points at.**
> `<target_table_singular>_id` → `evidence_item_id` resolves to `evidence_items`, and nothing else.
> **The name IS the join.** A reader and a script derive the wiring without opening the schema.
> *Fixes the 6 mis-named FKs — `global_ref_id`, `evidence_ref_id`, `root_ref_id`, `promoted_to_rdc_id`,
> `parent_code`, `merged_into`. Self-references keep the rule and add a role prefix:
> `parent_research_item_id`. Checkable: for every FK, `col == singular(target)+"_id"`.*

> **LAW 3 — One reference per cell. Plural means junction.**
> No column holds a delimited list of references. *Kills all 7 packed columns; each becomes a
> junction or is deleted. Checkable: no column name ends in a plural reference form, and no
> reference column's values contain a delimiter.*

> **LAW 4 — One concept, one name, everywhere.**
> The canonical set is fixed and total: `created_at` · `created_by_session` · `updated_at` ·
> `updated_by_session` · `notes` · `status`. A stage-specific status keeps its own vocabulary in its
> **CHECK**, never in its column name — `extraction_status` becomes `status` with a different CHECK.
> *Collapses 7→1, 7→1(+`rationale` where it is content, not a remark), 4→2, 8→1. Checkable against
> the canonical list.*

> **LAW 5 — The stage prefix directs the wiring DIRECTION, and this is the one that earns the others.**
> A table prefixed `<stage>_` may hold a foreign key into **its own stage, any earlier stage, or
> substrate. Never a later stage.** *Because `stage_id[:3]` gives a total order — `res evi jud syn spe
> ren` — a script that reads only table and column NAMES can decide whether a key points forward.*

**Law 5 makes rule 5 enforceable for the first time.** `CLAUDE.md` rule 5 — *never write into a
completed stage* — has no enforcing code today. Under Law 5 it becomes a name comparison. And it
immediately catches a live violation the last session missed in 877 lines:
`source_value_extractions.promoted_to_rdc_id → reasoning_doc_citations` is an **evidence-stage column
keyed into synthesis**, filled after the extraction completes — the exact anti-pattern Part B invokes
to reject back-pointers, sitting on the proposed `evi_items` itself (A2-W4-iii).

### 10.3 The consolidated column spine, per phase

Every stage hand-off object gets **the same five-part shape**. Consolidation by phase means the
differences between stages are payload only — never plumbing.

```sql
-- IDENTITY ............ minted, stable, quotable in prose  (§6.4)
  <stage>_item_id   TEXT PRIMARY KEY          -- RES-00001 / EVI-00001 / JUD-00001 / SYN-00001 / SPE-00001
-- HAND-OFF ............ Law 2 names the join; NOT NULL is the spine   (§9.2, §9.3)
  <prev>_item_id    TEXT NOT NULL REFERENCES <prev>_items(<prev>_item_id)   -- fan-out stages only
                                                                            -- fan-in stages use a junction
-- TOPIC ............... substrate pointers, every stage, same names
  slug              TEXT REFERENCES slugs(slug)
  item_code         TEXT REFERENCES <parameter registry>   -- pending Q2 / §9.6
  population_code   TEXT REFERENCES populations(population_code)
-- PAYLOAD ............. the ONLY part that differs by stage
-- STAMPS .............. Law 4, mandatory, identical on all six
  created_at, created_by_session, updated_at, updated_by_session
```

Payload by phase — what each stage is *for*, and nothing else:

| stage | payload columns | consolidated from |
|---|---|---|
| `res_items` | `origin` *(with `unknown-legacy`, §9.7-D)* · `parent_research_item_id` · the identifier block (`doi, url, pmid, pmcid, isbn, issn, standard_number`) · `status` | `source_locators` (20) + the lead families |
| `evi_items` | `parameter` · `parameter_canonical` · `claimed_value` · `claimed_unit` · `claim_text` · `claim_type` · `source_section` · the **15** `loc_*` locator columns · `status` | `source_value_extractions` (48) |
| `jud_items` | `tier_assessed` · `soundness` · `directness` · `weight` · `dissent_of_judgment_item_id` · `rationale` | **new** (§9.1-X4: population grades stay a source-grained satellite) |
| `syn_items` | `kind` (`primary`/`comparative`) · `synthesis` *(or the file pointer, pending Q3)* · `status` | `bpc_metadata` (16, all of which are process metadata) |
| `spe_items` | `value_min` · `value_max` · `value_unit` · `state` · `design_scale` · `marker` · `rationale` · `falsification_condition` | `specifications` (27) |

**Three consolidations fall straight out of this and are the answer to "consolidate by phase":**

1. **`bpc_metadata`'s 16 process-metadata columns are not synthesis payload.** `co1_pass_count`,
   `pico_complete`, `search_complete`, `citation_mining_complete`, `supersession_check_complete` are a
   **completion checklist about the research**, sitting on the synthesis row. Under Law 5 they are
   research-stage facts on a stage-4 table. They become a derived view over the stages that own them,
   not stored columns — which is also why the synthesis has no column for the synthesis.
2. **`specifications.governing_refs`, `tier_basis`, `derivation_sha`, `confidence_*` are judgment
   facts on a specification row.** They restate what `jud_items` will hold. Under rule 5 they are
   copies; the specification reaches them through `spe_synthesis_links → syn_judgment_links`.
3. **The 15 `loc_*` columns are one concept in fifteen slots** — 7 start, 7 `_end`, plus `loc_note`.
   They belong to the extraction (a locator is a within-document pointer, R3), and they are the one
   place a wide column block is correct, because a citation locator genuinely has that many parts.
   **Keep, do not fold** — noted because "consolidate" must not become "collapse what is honestly wide."

### 10.4 The checker — the reason to do any of this

None of the five laws is worth stating without a gate, and §1 requires naming what reaches the book
if it does not exist. **A new registered check, `wiring_grammar`,** reading only `sqlite_master`:

| law | assertion | `EXAMINED:` |
|---|---|---|
| 1 | no key-shaped column is neither PK nor FK | key-shaped columns |
| 2 | every FK's name equals `singular(target)_id` | FK constraints |
| 3 | no packed-reference column | all columns |
| 4 | stamp/remark/status names are from the canonical set | all columns |
| 5 | **no FK points to a later stage** | FK constraints |

**What reaches the guidebook without it:** Law 5 is `CLAUDE.md` rule 5, which today has **zero
enforcing code** — the file says so itself, and says the three guardrails that would have caught this
repository's real failures all had none. A determination whose provenance is a packed text column
(`governing_refs`) cannot be checked by a reader or a gate; that is how five fabricated citations
passed six green gates. **The burden is paid in book terms, not apparatus terms.**

### 10.5 What this does to the plan

The column rewrite is **not** a new phase. It lands inside the migrations already scheduled, because
renaming a column costs nothing extra once the table is being rewritten:

| into | addition |
|---|---|
| **T-0** | Build `wiring_grammar` **first, as advisory**, and let it report the baseline: 13 liars, 7 packed, 6 mis-named, the stamp footprints. A check written after the rename cannot prove the rename fixed anything. |
| **T-A2** | Mint the five hand-off objects with the §10.3 spine exactly. New tables must be born compliant — this is free now and expensive later. |
| **T-B** | The column sweep on the renamed tables: 13 liars, 6 mis-named FKs, the four stamp names, the status collapse. Same migration as each table's rename. |
| **T-B** | The 7 packed columns → junctions. `specifications.governing_refs` is the priority; it is the one a reader sees. |
| **T-C** | Promote `wiring_grammar` to **blocking**. It can only be blocking once T-B has cleared its findings — the §9.8 sequencing lesson, applied in advance rather than after. |

**One caution, from the same lesson.** Column renames break callers exactly as table renames do, and
`ALTER TABLE RENAME COLUMN` does **not** rewrite string references inside Python, skills, or the
registry — only SQL schema objects. **The T-0.4 sweep helper must take columns, not just tables**, or
this part of the work re-arms the migration-064 failure at 876× the surface.

---

## PART 11 — B3 (tables / minimization) refutes Part 9.5. Corrections.

First of four Fable 5 lenses, read-only, its own report at
`scratchpad/session_2026-08-27-hook-audit/audits/B3-tables-minimization.md`. **Where Part 11 and
Part 9.5 / §6.6 disagree, Part 11 wins.** Two BLOCKERs, five MAJORs, three defects.

### 11.1 The serious one: `situations` is Co-1 doctrine, not apparatus

I put it in Tier 1 on "0 rows, no writer." **That ground is true and irrelevant.**

- `governance/functional-taxonomy.md:324` — *"First-person accounts → situations"*
- `governance/functional-taxonomy.md:97` — the entity and Co-1 testimony are *"never subordinated"*
- `governance/held-tensions.md:363` — *"situations rendered beside specifications"* — a **book surface**
- its own DDL carries `co1_status` and `operational_access`

**`situations` is the structured home of Co-1 lived-experience testimony.** §1's own carve-out
reserves content and doctrine — *"evidence-tier definitions… work-product inclusion"* — for owner
sign-off. Deleting it on agent evidence means that when Co-1 accounts arrive they land in prose or
nowhere, and this project's own words for that are **"the worst failure available here."**

**Corrected: `situations` leaves Tier 1 entirely. Owner-gated, and I should not have proposed it.**
This is the §1 boundary — code is mine to delete, doctrine is not — and I crossed it on the one
entity where the cost is highest.

### 11.2 `connections` feeds a book part today, and its fold target is deferred

`scripts/generate_parts.py:245-257` **builds Part 5 of the book from `connections`.** It has full
CRUD in `db.py` (:113, :117, :129, :692-693), `log-mining` merges into it, plus `schemas/connection.py`,
`validate_cross_refs.py`, graph audits, **11 skills**, registry and retired-vocabulary entries.

And the fold target — `syn_items.kind='connection'` **plus `syn_synthesis_links`** — is the very
table §6.6 *deferred* to reach its lower bound. **Deleting a table because it becomes X, while
deferring X, is deletion with no successor.** The existence-guard means it would not crash; it would
silently empty a book part, which is the §2(a) shape.

**Corrected: re-tiered to "fold in the same commit that creates `syn_items.kind` and
`syn_synthesis_links`", and `syn_synthesis_links` is added to the count (+1).**

### 11.3 I skipped rule 5's own procedure on my own deletion set

`reference_stubs` "0 rows and no writer" is **false**: two committed data migrations touch it.
`data_20260823223839` INSERTs the stubs; `data_20260823225142`'s header reads *"fold reference_stubs
into source_locators… Runs as a DATA migration so it replays AFTER data_20260823223839."* On
`--rebuild` both replay and **require the table to exist** — an ordinary schema `DROP` replays before
data and breaks reproducibility.

**I ran the C5 collision measurement for the renames and never ran it against the deletions**, in a
document that quotes rule 5's *"grep `scripts/migrations/data_*` for the name first."* B3 ran it:
`reference_stubs` is the only collider in Tiers 1–2.

**The honest ground is better than mine:** not "no writer" but **superseded** — migration
`data_20260823225142` already folded 10 of its 11 columns into `source_locators`. §1 names
"superseded" as exactly the evidence wanted. **The drop must be marked `AFTER_DATA`.**

### 11.4 The grids: right verdict, wrong ground, six unswept readers

`search_coverage`/`search_languages` do **not** merely restate `search_executions` — they carry
non-derivable judgment columns (`status IN ('SEARCHED','THIN','NO-DATA','NOT-RUN')`, `co1/tier5/tier6_attempted`).
A missing execution row cannot distinguish NOT-RUN from never-planned.

**The deletion survives on a recorded ruling I never cited:** the grids are **FROZEN** in
`scripts/db.py:264-320` (`FrozenGridError`) per `workplan/search-coverage-completion-workplan.md` —
*"derive every coverage matrix as a VIEW over that log"* — and the three successor views exist. The
drift that forced the freeze: **634 SEARCHED cells against 15 corroborated.**

**Six live readers need sweeping**, including `tools/evidentiary_audit.py`, which feeds a **blocking**
freshness gate. Drop without the sweep and `evidentiary_audit_fresh` goes red or vacuous.

### 11.5 Tier 2, actually run: 7 of 11 clear

I proposed the check; B3 ran it. **Four do not clear, and one of those is live CI infrastructure:**

| table | verdict |
|---|---|
| `url_verification_runs` | **KEEP → Tier 3.** Writer `scripts/verify_urls.py` and a **dedicated scheduled workflow** `.github/workflows/verify-urls.yml` — one of the four CI workflows `CLAUDE.md` §5 names. Deleting it decapitates a live pipeline's log |
| `case_study_specs` | **KEEP.** It is the named remedy inside a live `db.py` refusal (:2486 — *"Link the source through case_study_specs"*). **Deleting the designated remedy of a live refusal is the exact R6 defect `CLAUDE.md` voids** |
| `gap_mining` | Registered check `gap_mining_audit` prints `EXAMINED` from it. And §6.3 calls the gap-driven walk *"a live requirement"* — deleting its act log while affirming the activity is incoherent. **Deletable only via the acts fold** |
| `supersession_check` | `db.py:1051` carries DR-2026-05-24; `bpc_metadata.supersession_check_complete` references it. **Fold, don't delete** |
| `item_audit_runs` | `db.py add-audit-run`/`update-audit-run`/`audit-runs`, `audit_consolidator.py`, 2 skills |

The seven that clear: the three empty extraction/probe/citation population junctions (drop
`schemas/population_links.py` in the same commit — the Pydantic mirror), plus
`case_study_populations`, `economics_entry_populations`, `economics_entry_specs`.

### 11.6 The fold refusal used its own measurement backwards — and this is the real finding

§6.6 refused the act-table fold because **the 7 tables share zero columns.** B3:

> **Zero shared columns is naming drift, not row-kind evidence.** All seven carry the same two facts
> — who ran it, when — spelled seven ways. *The statistic that "refutes" the fold is the disease J.3
> diagnosed, measured.*

That is correct and I inverted it. Measured further: `gap_mining ∩ supersession_check` share **six
substantive columns**; `search_executions` already carries `mining_direction`; and J.1's ruling
(*"a mining pass IS a search with a different origin"*) already says the fold is the model. A folded
`res_searches` with `kind ∈ {search, mine-backward, mine-forward, gap, supersession}` lands near **35
columns** — narrower than `jurisdictional_values` alone. **My "~90-column, >80% NULL" figure described
the 7-way merge nobody should do**; `url_verification_runs` and `pipeline_runs` are counter-reports
and `item_audit_runs` a process checklist, and keeping those three out is the correct part of the refusal.

Likewise `search_candidates → res_items` is clean (union 32 columns). And **`reference_stubs` shares
10 of 11 columns with `source_locators` and was already folded by a committed migration** — one of the
four "unfoldable" leads was folded by SQL I never grepped.

**And the folds had no task ID.** §6.6 called them *"worth more than every deletion combined"* and
then scheduled them nowhere. **Corrected — new tasks:**

| new | task |
|---|---|
| **T-B.8** | Fold `citation_mining`, `gap_mining`, `supersession_check` into `res_searches` with a `kind` discriminator (−3) |
| **T-B.9** | Fold `search_candidates` into `res_items` (−1): `tier_guess`→`tier_claimed`, `locator`→identifier block, `disposition`→`status`, keep `exec_id` as provenance |
| **T-B.10** | Column study for `jurisdictional_values` — its **16 `loc_*` columns are a byte-for-name duplicate of the extraction locator block, 24 shared columns**, a live structural dual home no document has flagged |

### 11.7 `figures` fails §1's mirror clause — strike it from the count

§1: *"Nothing is added without naming what reads it."* **No renderer reads `figures`, none is
scheduled, zero figures exist**, and it appears in the arithmetic (+1) while appearing in **no task**.
I applied *"re-create a sibling when a stage actually needs one"* to the population junctions and
exempted `figures` from the same rule without argument.

**Corrected: struck from the count. Create it in the commit that ships the first figure, with its
generator named as the reader.**

### 11.8 Two of my own proposed checks fail §1, in a document that voids others on that ground

- **9.7-H** (prefix-drift check) — justified as *"the rename is a one-time correctness event with no guard."* Apparatus.
- **S-1** (ledger execution-status check) — justified as *"a check should read it."* Apparatus.

§1: *"If the answer is about the apparatus rather than the book, do not add it."* **Either pay them in
book terms or drop them.** 9.7-H is payable — a stage prefix that lies sends a writer to the wrong
stage, and rule 5's write-order is what stops a determination being built on a fact from a stage that
had not run. S-1 is not obviously payable and should be **dropped to a convention**, not a check.

*(Note that `wiring_grammar` in §10.4 does pay in book terms — a determination whose provenance is a
packed text column cannot be checked by a reader or a gate. That one stands.)*

### 11.9 Three defects

- **D1 — two tables fell out of my own menu.** 19 minus Tier 1 (6) minus Tier 2 (11) leaves
  `case_study_outcomes` and `case_study_strategies` in **no tier**, and they are not in Tier 3's list
  either. A menu that does not count is not a menu.
- **D2 — "the only keyed cross-stage edge in the schema" is false** by my own tables:
  `evidence_sources.ref_id` carries 7 cross-stage inbound keys, `gaps.gap_id` 2, and X2 itself names
  `specifications.convergence_id`. **The KEEP verdict for `search_admissions` survives; the
  superlative does not.** Defensible form: the only keyed edge joining two *consecutive* stages'
  hand-off/act objects.
- **D3 — the `items` −1 assumes the answer to my own open question.** §9.6 recommends re-graining to
  a parameter registry, under which the count is **net 0**. State it as "−1, or 0 pending Q2."

### 11.10 The honest number, and it is better than mine — by folding, not deleting

| | |
|---|---|
| my claim | 52–63 |
| arithmetic *qua* arithmetic | correct (66−6−1+4 = 63; −11 = 52) |
| **but deletion-only actually bottoms at** | **56** — Tier 2 clears 7, not 11 |
| **B3's composed design** | **66 → 54 firm**, 52–53 with the owner-gated and study-gated items |

The route to 54 is: 3 evidenced Tier 1 deletions (grids + stubs, with `AFTER_DATA`) · 7 clearing
Tier 2 · **fold acts −3** · **fold `search_candidates` −1** · fold `connections`+`connection_targets`
into `syn_items.kind` when synthesis lands −2 · `items` −1 or 0 per Q2 · create `jud_items` + 3
junctions +4 · defer `figures` · `situations` only on owner sign-off.

**Below my own floor, deleting no live infrastructure, and by the mechanism the owner's own quoted
rule (J.4) prescribes.** The lesson is the one B3 states plainly: **the minimization is in the folds,
not the deletions**, and I had the folds refused and unscheduled while proposing to delete Co-1
doctrine and a live CI log.

### 11.11 What B3 attacked and could not break

The base measurements (66/33/18); the 7-way-merge refusal and the polymorphic-junction refusal (both
sound); the `ren_items` withdrawal and the check-artifact resolution (046-compliant and §1-clean);
the `search_admissions` KEEP; Tier 3's protection of the spine tables and of
`case_studies`/`economics_entries` (R12 confirmed verbatim at `governance/research-contract.yaml:186-193`);
and X5's retraction of "33 empty = 33 unpaid." **One point in the plan's favour it never claimed:
no view reads any table on the deletion menu** — measured over `sqlite_master`.

---

## PART 12 — B2 (keys / pointers) breaks three things, including one of my own laws

Second Fable 5 lens, report at `audits/B2-keys-pointers.md`. **It tested SQLite on a scratch DB
rather than reasoning about it, and two "impossible" claims — mine and A3's — are false.**
Where Part 12 disagrees with Parts 6, 7, 9 or 10, Part 12 wins.

### 12.1 BLOCKER — my corrected key placement is *still* unwritable, and the fix was in reach

§9.3 K1 moved the lead key to `evi_sources.research_item_id NOT NULL`. Measured: **six of ten
`evidence_sources` rows (`REF-00965`–`REF-00970`) have no `source_locators` parent.** The NOT NULL is
as unwritable there as it was on the extraction. **I adopted A3-F3's placement and dropped its
backfill remedy in the same breath — while branding backfill "§2(c) with paperwork."**

**The dissolving measurement, which nobody ran until now: all six have `search_admissions` rows**
(exec 1, 1, 6, 6, 13, 10). So the lead for each of them *is recorded* — it is in the admission edge.
A backfilled lead with `origin='searched'` carrying that exec id is **truthful, not fabricated**.

**Corrected:** T-A2 backfills six `res_items` rows from their `search_admissions` provenance, declared
in the migration header. That is the difference between retroactive provenance (invention) and
recovering provenance the schema already holds (recovery).

### 12.2 BLOCKER — the plan contradicts its own corrections in three places

I criticised the source document for shipping Parts E and J as two incompatible plans (A2-B2). **I
reproduced the defect.** B2 transcribed my DDL and ran it:

| location | still says | corrected by |
|---|---|---|
| T-A2 hand-off table | `evi_items.research_item_id` | §9.3 K1 |
| §6.3 forward-gap query — **the named T-A3 acceptance test** | `e.research_item_id` | §9.3 K1 |
| T-A2 `jud_items` column block | carries the population-grade fold | §9.1 X4 |

**Tested: the acceptance query fails with `no such column: e.research_item_id` against the plan's own
corrected schema.** A plan whose acceptance test cannot run is not executable. **Part 7 must be
reconciled against Parts 9–12 before any DDL is transcribed** — that is now a precondition, not a
tidy-up.

### 12.3 BLOCKER — the allocator silently mints `REF-00001` after the rename, and the selftest cannot see it

§6.4 says "follow the `dbcore.next_ref_id` pattern." B2 read it: **`dbcore._REF_ID_HOMES` hardcodes
the pre-rename table names** and swallows failures with `except OperationalError: continue`.

**Tested: after the T-B rename, `next_ref_id` returns `REF-00001`** — colliding with every live id.
And `--selftest` stays green, because it fabricates its own old-named fixture tables
(`dbcore.py:415-418`). **A blocking gate that constructs the world in which it passes.**

This is `CLAUDE.md` rule 4 exactly — *a rename is not done until the callers are swept*, and **a
hardcoded table list inside an allocator is a caller.** Added to T-0.4's sweep by name, and to T-B as
its own task.

### 12.4 A fourth cardinality option — tested, and it may dissolve Q1 entirely

§9.2 put (a) literal 1:1 and (b) NOT-NULL-no-UNIQUE to the owner. B2 found a fourth:

```sql
CREATE UNIQUE INDEX ux_jud_primary ON jud_items(evidence_item_id) WHERE dissent_of IS NULL;
```

**Tested: refuses a second *primary* judgment on one extraction, accepts any number of dissents.**
That is the owner's *"each row of evidence provides one row for judgment"* enforced **literally**,
while the dissent contest survives — the two things §9.2 presented as mutually exclusive.

**This is better than anything in the plan and it changes what to ask.** Q1 stops being "(a) or (b)?"
and becomes a confirmation: *we can enforce your 1:1 exactly and still carry dissent; here is the
index.* Recommend building it and telling the owner, not asking them to choose between two worse
shapes.

### 12.5 My recommended option (d) breaks ratified re-entrancy

§9.2 recommended `UNIQUE(judgment_item_id)` on `syn_judgment_links` "outright." **Tested: a v2
synthesis cannot cite v1's judgments without deleting v1's links.**

That collides with `governance/pipeline-map.yaml:78`, ratified 2026-08-21: *"these are LAYERS a walk
re-enters."* **Withdrawn.** If N:1 is wanted it must be scoped — a partial unique index over live
(non-superseded) syntheses — not a blanket constraint.

### 12.6 K3 was wrong: SQLite *can* enforce "≥1 per synthesis"

A3-F2 said no declared constraint can require a parent to have a child; §9.3 K3 accepted it and
routed the invariant to a writer plus a check. **B2 tested the alternatives and found one that works:**

```sql
syn_items.anchor_link_id  NOT NULL  REFERENCES syn_judgment_links(link_id)
                          DEFERRABLE INITIALLY DEFERRED
```

A deferred circular FK **refuses a zero-link synthesis at COMMIT**, and refuses deletion of the
anchor link. CHECK-subqueries, generated columns and triggers all fail, as A3 said — **also tested.**

**Corrected:** the invariant is declarable. The writer and the check remain useful (they give a better
error and catch the non-anchor links), but they are no longer the *only* enforcement, and "currently
aspiration" no longer applies.

### 12.7 My own Law 2 would turn my own spine red

§10.2 Law 2: an FK column is named `<target_table_singular>_id`. The spine tables are `evi_items`,
`jud_items`, `syn_items`. **So Law 2 demands `evi_item_id` — and the plan writes
`evidence_item_id` throughout.** A blocking `wiring_grammar` check would flag **every hand-off column
the plan mints.**

**Resolved, and the grammar wins:** the table prefix is derived `stage_id[:3]`, so the tables are
`res_/evi_/jud_/syn_/spe_items` and the hand-off columns are **`res_item_id`, `evi_item_id`,
`jud_item_id`, `syn_item_id`, `spe_item_id`**. One rule, no exceptions, and the column names get
shorter. Every occurrence of `research_item_id` / `evidence_item_id` / `judgment_item_id` in Parts
6–11 is superseded by this form.

### 12.8 Identifiers — under-specified where it matters

- **The 875 legacy `REF-` ids have no stated fate.** One branch keeps them beside the new `RES-` codes
  (recreating U-7 byte-identically — two homes for one identity); the other re-mints them (defeating
  the point of stable, quotable codes). **Neither is chosen. This is a decision, and it is mine to
  put, not to skip.**
- **The `REF-VERIFIED` re-mint rests on a false necessity.** §6.4 said the 11 malformed ids must be
  re-minted *before* the allocators are written. B2 verified the regex fullmatch already defuses
  `MAX()`, and the gap at `-008` shows gaps are already tolerated. **Re-mint if we want tidy ids, not
  because the allocator requires it** — and say which.
- **`bpc_metadata`'s re-key breaks five unnamed code callers**, including a **silent-overwrite
  corruption vector** in `scripts/db.py:1766-1781`'s UPSERT and the D03 duplicate-slug check at
  `test_db_integrity.py:689`.

### 12.9 Defects

`spe_items`' key is stated **four different ways** across the plan, plus a fifth (`s.ref_id`) inside
its own acceptance query · T-A2's "two rebuilds" undercounts its own §10.3 re-keys · a 5-digit
allocator freezes at 99999 · the junction composite PK covers only one walk direction and the plan
never states column order (tested) · `governing_refs` has **two contradictory dispositions inside
Part 10 alone**.

### 12.10 What B2 could not break

The backward-walk mechanism · §6.3's premise that SQLite does not auto-index FK sources (confirmed
empirically) · `next_ref_id` on the *current* schema (REF-00971, correct) · the 875/10/4/6 figures and
the 11 malformed ids (all reproduced) · the shape of the ≥1 gap-check SQL · M-4's disposal of the
spec→render junction · the `AFTER_DATA` reading of `migrate_db.py:283-330`.

---

# PART 13 — THE OPERATIVE PLAN

> **Parts 1–12 are the audit trail. They are NOT executable and must not be transcribed.**
> Everything a Sonnet or Opus session executes is in this Part. Where Part 13 disagrees with any
> earlier Part, Part 13 wins, silently and completely.

**Why this Part exists.** Three of four Fable 5 lenses independently found the same defect: the
corrections in Parts 9, 11 and 12 never reached the executable surfaces in Parts 6.2 and 7, held
together only by *"Part 9 wins."* B1 put it exactly — *"an audit trail wearing a runbook's clothes"*
— and named eight sites where a session told to "execute T-A2" transcribes refuted DDL. **That is
the same defect I criticised in the source document** (Parts E vs J), reproduced. This Part is the
collation the plan already owed.

## 13.0 The headline result is DEAD — corrected

§C5 claimed the spine touches only zero-row tables with zero replay collisions, so it ships with no
baseline and **no `AFTER_DATA`**. **Two lenses killed it independently:**

- **B4:** T-A2 renames `source_locators`, which **two post-baseline data migrations write with real
  DML** (`data_20260823223155`, `data_20260823225142`). Demonstrated on a scratch copy: rename, then
  replay → `no such table: source_locators`. **`migration_reproducibility` goes red.**
- **B1:** §9.3-K1 moved the spine key onto `evidence_sources` — **10 live rows, 14 DML collisions by
  my own §9.9 table.** Nobody re-ran the partition after the key moved.

**My own §9.9 table printed `source_locators: 3` and I never reconciled it with C5.** The measurement
that refutes the claim was in the document, three sections away from the claim.

**And one supporting claim was false.** §C4 said `AFTER_DATA` is *"in live use by two migrations."*
B4 checked the marker regex (`^--\s*AFTER_DATA:\s*\d{14}\s*$`): **zero live migrations carry a valid
marker.** The two files *mention* it in prose. The mechanism is implemented at
`migrate_db.py:282-320` and is **unexercised** — that is still enough to rely on, but it must be
stated as first use, and T-A2 must prove it.

> **CORRECTED: the spine migration touches two data-bearing tables and REQUIRES an `AFTER_DATA`
> marker. The Track A / Track B split survives — the spine is still one ordinary migration, not a
> baseline — but "free, no marker" is withdrawn.**

## 13.1 The naming, settled

Six stages, prefix from `stage_id[:3]`: **`res_ evi_ jud_ syn_ spe_ ren_`**.

**Hand-off columns take the PREFIX form, not the stage word** — B1-3 and B2-7 both measured that the
stage-word form (`evidence_item_id`) fails my own Law 2 against table `evi_items`:

| table | identity | hand-off column |
|---|---|---|
| `res_items` | `res_item_id` TEXT PK | — (origin) |
| `evi_items` | `evi_item_id` TEXT PK | — (see 13.2: the lead key is on `evi_sources`) |
| `jud_items` | `jud_item_id` TEXT PK | `evi_item_id` NOT NULL |
| `syn_items` | `syn_item_id` TEXT PK | via `syn_judgment_links` |
| `spe_items` | `spe_item_id` TEXT PK | via `spe_synthesis_links` |
| `ren_*` | — | **no hand-off object** (M-4) |

**Every occurrence of `research_item_id` / `evidence_item_id` / `judgment_item_id` /
`synthesis_item_id` / `specification_item_id` in Parts 6–12 is superseded by the prefix form.**

## 13.2 The keys, settled

| edge | shape | why |
|---|---|---|
| research → evidence | **`evi_sources.res_item_id NOT NULL`** — on the ADMISSION, not the extraction | A3-F3: the lead→paper edge is source-grained; on the extraction it is a rule-5 copy |
| evidence → judgment | `jud_items.evi_item_id NOT NULL`, **plus** `CREATE UNIQUE INDEX ux_jud_primary ON jud_items(evi_item_id) WHERE dissent_of IS NULL` | B2-4, tested: enforces the owner's 1:1 **literally** while admitting dissent |
| judgment → synthesis | junction `syn_judgment_links`, **no blanket UNIQUE** | B2-5, tested: `UNIQUE(judgment_item_id)` breaks ratified re-entrancy (`pipeline-map.yaml:78`) — a v2 synthesis cannot cite v1's judgments |
| synthesis → specification | junction `spe_synthesis_links` | fan-in |
| ≥1 per fan-in parent | **`syn_items.anchor_link_id NOT NULL REFERENCES syn_judgment_links(link_id) DEFERRABLE INITIALLY DEFERRED`** | B2-6, tested: a deferred circular FK **refuses a zero-link synthesis at COMMIT**. A3-F2 and my own K3 were both wrong that this is inexpressible |

**Indexes are mandatory on every hand-off column and both junction columns** — SQLite does not index
FK sources, and without them the forward walk is a table scan (§6.3, confirmed empirically by B2).

**The six no-lead sources are backfilled, not waived.** `REF-00965`–`REF-00970` have no
`source_locators` parent — but **all six carry `search_admissions` rows** (exec 1, 1, 6, 6, 13, 10).
T-A2 mints six `res_items` rows with `origin='searched'` from that recorded provenance. **That is
recovery of provenance the schema already holds, not the retroactive invention I called §2(c).**

## 13.3 The identifiers, settled

Stable TEXT codes `RES-/EVI-/JUD-/SYN-/SPE-NNNNN`, computed from a high-water union, never stored.

- **`dbcore._REF_ID_HOMES` is a caller and must be swept.** B2-3, tested: it hardcodes pre-rename
  table names and swallows failures, so after the rename `next_ref_id` returns **`REF-00001`** — and
  `--selftest` stays green because it fabricates its own old-named fixtures. **A blocking gate that
  constructs the world in which it passes.**
- **The 875 legacy `REF-` ids keep their namespace.** `res_items.res_item_id` holds the existing
  `REF-NNNNN` values; new research items mint `RES-`. Two prefixes in one column is honest history,
  and re-minting 875 ids would break every citation that quotes one. *(This was undecided; it is
  decided here.)*
- **The 11 `REF-VERIFIED-*` ids are re-minted for tidiness, not necessity.** B2 verified the regex
  fullmatch already defuses `MAX()`. Say so in the header; do not claim the allocator required it.
- `bpc_metadata`'s re-key to `syn_item_id` **breaks five code callers**, including a silent-overwrite
  vector in `scripts/db.py:1766-1781`'s UPSERT and the D03 duplicate-slug check at
  `test_db_integrity.py:689`. Both in the sweep.

## 13.4 The five laws, corrected

B1-3 ran my laws mechanically. **Law 2's test fails 75 of 80 current FKs where §10.1 claims 6, and
Law 1's XOR form flags 31 legitimate columns including §10.3's own `slug`.** Corrected:

| law | corrected statement |
|---|---|
| **1** | `keyish(col) ∧ ¬PK ∧ ¬FK` must be empty — **not XOR**. A key that is not key-shaped (`slug`, `alias`, `language`) is legal; a key-shape that is not a key is not. Reproduces the 13. |
| **2** | FK column = `singular(target)_id`, where `singular()` is resolved **through `pipeline-contract.yaml`** for stage tables. **The checker reads the contract** — it cannot expand `res_` to `research` from `sqlite_master` alone. |
| **3** | Schema-only: no column *name* is a plural reference form. **The data-delimiter test is dropped** — it contradicted "reads only `sqlite_master`," stated twice. |
| **4** | unchanged. |
| **5** | Stage order comes from the **contract**, not from lexical order — `evi < jud < ren < res < spe < syn` alphabetically is not the pipeline order. |

**Substrate code-keys (`slug`, `item_code`, `population_code`, `*_code`) are explicitly exempt from
Law 2** and named in the checker as such.

## 13.5 The tables, settled

**Deletions — three only, each evidenced on grounds other than emptiness:**
`search_coverage` · `search_languages` (both: the recorded **freeze ruling**, `db.py:264-320`
`FrozenGridError`, plus three built successor views — cite that, not "restates the log") ·
`reference_stubs` (**superseded**: `data_20260823225142` already folded 10 of its 11 columns).
**All three drops carry `AFTER_DATA`;** `reference_stubs` has two colliding data migrations.

**Then the seven Tier-2 clears** (three empty population junctions + `case_study_populations`,
`economics_entry_populations`, `economics_entry_specs`, `case_study_outcomes`), each with its
Pydantic mirror dropped in the same commit.

**NOT deleted, reversing Part 9.5:**

| | why |
|---|---|
| **`situations`** | **Co-1 doctrine.** `functional-taxonomy.md:324`, `held-tensions.md:363`; DDL carries `co1_status`. **Owner-gated. I should not have proposed it.** |
| `connections`, `connection_targets` | build **book Part 5** (`generate_parts.py:245-257`); fold only in the commit that creates `syn_items.kind` + `syn_synthesis_links` |
| `url_verification_runs` | writer + **dedicated CI workflow** `.github/workflows/verify-urls.yml` |
| `case_study_specs` | the named remedy inside a **live `db.py` refusal** (:2486) — deleting it is the R6 defect `CLAUDE.md` voids |
| `gap_mining`, `supersession_check`, `item_audit_runs` | fold via T-B.8, do not delete |

**The minimization is in the FOLDS** — and they now have task ids (13.7 T-B.8/9/10).
**Honest target: 66 → 54 firm**, 52–53 with owner- and study-gated items.
**`figures` is struck from the count** — no reader exists and none is scheduled (§1's mirror clause).
**`jud_population_grades` is a real table** (X4) and appears in the map and in T-A2.
**`items` is −1 or 0**, pending Q2.

## 13.6 The three owner questions, rewritten

**Q1 is no longer a choice.** B2 found and tested a shape that satisfies the owner's sentence
literally *and* keeps the dissent contest:

> Your ruling was *"each row of evidence provides one row for judgment."* We can enforce that
> exactly — a partial unique index on `jud_items(evi_item_id) WHERE dissent_of IS NULL` refuses a
> second **primary** judgment on any extraction while still admitting a recorded dissent. Tested.
> **Nothing to choose; confirm and we build it.**

**Q2, re-put per §9.6.** Not *"does `item_code` rename?"* but: `items` is a registry of design
parameters; retiring it and keying specifications on a canonical label **recreates it under a worse
key** (homonyms, no stability, one vocabulary in two homes). **Re-grain it into a substrate registry
minting stable parameter codes** (`code` PK, `canonical_label` UNIQUE) — the ambiguous word goes, the
registry stays. Net table count 0, not −1. *The registry still needs a name.*

**Q3 unchanged** — prose in files (status quo, nearly free to ratify) or in rows.

**Plus one I owe you:** `situations` (13.5) is Co-1 doctrine and its deletion is yours alone. I am
not proposing it; I am telling you I nearly did.

## 13.7 The task list, operative

**T-0 — unblock (Sonnet).** T-0.1 de-hardcode `migration_reproducibility.py` (a **contract/DR**
change; its selftest hardcodes `items` six times) · T-0.2 fix U-7 (`source_ref`/`ref_id`) · T-0.3 fix
`record-command.py` (both defects: stale-dir minting **and** subagent attribution) · **T-0.4 the
sweep helper, taking COLUMNS as well as tables**, and its caller list names by file:
`scripts/generate_parts.py` *(not `scripts/generate/generate_parts.py` — that path does not exist)*,
`build_site.py`, `spec_page.py`, `population_page.py`, `pilot_renderings.py`, `validate_items.py`,
`validate_evidence_state.py`, `check_rendered_docs.py`, `validate_verification_consistency.py`,
`research_batch_dod.py`, `citation_mining_completeness.py`, `assess_cell.py`,
`adjudication_integrity.py`, `audit_consolidator.py`, `migration_reproducibility.py`,
`pmp_audit.py`, `graph_audit.py`, `dbcore._REF_ID_HOMES`, the three `scripts/tests/*`, `tools/*`,
five governance YAMLs, 3 views, 22 skills · T-0.5 build `wiring_grammar` **advisory**, with the 13.4
laws, and record its true baseline.

**T-A1 — six-stage spine in the machine (Opus), one commit.** As §7 T-A1.1–1.6, with two fixes:
`derivation-handshake` carries `check: null` — it is declared-but-unenforced, so moving it is a
registry edit only; and `convergence-independence`'s subject table moves to synthesis at T-B, so say
which stage owns it in the interim.

**⛔ GATE** — Q1 (confirm), Q2 (re-grain), Q3, plus the `situations` notice.

**T-A2 — mint the spine (Opus).** `065_the_item_spine.sql`, `user_version` 65, **with an
`AFTER_DATA` marker** (13.0). Renames + `jud_items` + `jud_population_grades` + two junctions +
indexes + the deferred anchor FK + the six-lead backfill. Mirror `schemas/*.py` in the same commit.
**Writers ship with it** — `add-extraction`, `add-judgment`, `add-synthesis`, `add-specification`
and the junction writers do not exist (A3-F16). **Run T-0.4 before, and the full check battery
after.**

**T-A3 — walk one slug (Opus).** Acceptance, corrected — B4 showed three of my four criteria fail on
a healthy repo:
1. the five-hop join on hand-off keys only, returning ≥1 row *(B4 built it on a scratch schema: valid SQL, returns the row)*;
2. a rendered figure traces to its extraction and paper **by key path** — *deferred to T-B*, because every generator still queries the pre-rename names until T-B rewrites them;
3. `EXAMINED: n > 0` **on instrumented checks only** — `pipeline_completeness_fresh` is deliberately uninstrumented (`no_floor`), so demanding it is unsatisfiable;
4. `db.py` refused at least once;
5. **`migration_reproducibility` passes its 7-invariant compare** — *not* byte-identity, which fails on clean `main` today.

**T-B — nomenclature + folds (Sonnet; Opus for the population split).** T-B.1 `axes`→`icf_demands`
with the register entry · T-B.2 `MOB`→`AMB`/`WHEEL` (**Opus**, DG-NON) · T-B.3 sweep the 9 skills
teaching `MOB` and the 17 teaching retired codes · T-B.4 the research/evidence renames · T-B.5 the
three drops + seven clears · T-B.6 `items` per Q2 · T-B.7 `origin`/`parent_res_item_id` with
`unknown-legacy` · **T-B.8 fold `citation_mining`/`gap_mining`/`supersession_check` → `res_searches`
with `kind` (−3)** · **T-B.9 fold `search_candidates` → `res_items` (−1)** · **T-B.10 column study:
`jurisdictional_values`' 16 `loc_*` columns duplicate the extraction locator block name-for-name — 24
shared columns, a live structural dual home** · T-B.11 the column sweep (13 liars, 6 mis-named FKs,
stamp/status collapse, the 7 packed columns) · T-B.12 rewrite the generators, **then** promote
`site_pages_fresh` in the same commit.

**T-C — propagate (Sonnet).** Workplan · **one** consolidating DR + attestation (rule 2) · re-derive
the stage→table map under six stages · re-stamp the dated figures · promote `wiring_grammar` to
blocking. **Drop S-1** — an execution-status check on the ledger is apparatus-justified and fails
§1's own test, as does 9.7-H unless paid in book terms (a lying stage prefix sends a writer to the
wrong stage, which is how a determination gets built on a stage that had not run — that payment is
available; make it or drop the check).

---

## Appendix — re-derivation

```bash
# Part 1 live state
python3 - <<'PY'
import sqlite3
c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
t=[r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
v=[r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='view'")]
z=[n for n in t if c.execute(f"SELECT COUNT(*) FROM '{n}'").fetchone()[0]==0]
fk=sum(1 for n in t for _ in c.execute(f"PRAGMA foreign_key_list('{n}')"))
print(f"tables={len(t)} zero={len(z)} views={len(v)} fks={fk}")
PY

# Part 4 inbound-FK targets
python3 -c "
import sqlite3,collections
c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
t=[r[0] for r in c.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")]
e=[(r[2],r[4]) for n in t for r in c.execute(f\"PRAGMA foreign_key_list('{n}')\")]
for k,v in collections.Counter(f'{a}.{b}' for a,b in e).most_common(): print(v,k)"

# C4/C5 — the decisive measurement: data-migration replay collisions
for t in evidence_sources search_executions search_candidates citation_mining source_locators \
         evidence_population_match items specifications bpc_metadata source_value_extractions axes; do
  printf '%-28s %s\n' "$t" \
    "$(grep -lE "(INTO|UPDATE|FROM|TABLE)[[:space:]]+\"?${t}\"?[[:space:],(]" scripts/migrations/data_*.sql 2>/dev/null | wc -l)"
done

# C4 — AFTER_DATA exists and is in use
grep -n "AFTER_DATA" scripts/migrate_db.py | head
grep -ln "AFTER_DATA" scripts/migrations/*.sql

# U-1
grep -n "STAGES" tools/pipeline_completeness.py
python3 -c "import yaml;print([s['id'] for s in yaml.safe_load(open('governance/pipeline-contract.yaml'))['stages']])"

# U-7
python3 -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute('SELECT COUNT(*) FROM evidence_population_match WHERE source_ref IS NOT ref_id').fetchone(),
      c.execute('SELECT COUNT(*) FROM evidence_population_match').fetchone())"
```

---

## PART 14 — Owner architecture document, 2026-08-27 · **A THOUGHT DOCUMENT, NOT A RULING**

Source: `OWNER-ARCHITECTURE-2026-08-27.txt` in this directory (extracted verbatim from the uploaded
`.docx`; the `.pdf` is the same document).

> **CORRECTED WITHIN THE HOUR, ON OWNER CONTACT.** This part was first written as a rule-0
> supersession record — headers reading "SUPERSEDED", Q1 marked withdrawn, three prior records struck.
> The owner then stated: ***"it's not complete, and it's not definitive — just a thought document."***
> **That statement governs, and it is the one rule-0 applies to here.** A thought document is an
> INPUT. It supersedes nothing, closes no owner question, and strikes no ratified record.
>
> **What I did wrong is worth naming, because it is this repository's own recurring failure inverted.**
> The project's documented risk is arguing paperwork against a live ruling. I did the mirror: I
> promoted exploratory thinking to a ruling because it resolved problems I wanted resolved — four
> hard ones, elegantly, which is exactly when the promotion is most tempting and least warranted.
> The `-item` RULE was faulted by A4-B3 for attribution expansion; this was the same move, one layer
> further out. **Nothing below strikes anything.** Every "SUPERSEDED" heading is corrected to
> "SIGNAL", and the measured facts — which are true regardless of the document's status — are kept
> and labelled as measurements.

**It ends at Judgment**, and the owner confirms it is incomplete. Synthesis, specification and render
are simply not reached.

### 14.1 SIGNAL — the strongest evidence yet on the cardinality question, and Q1 STAYS OPEN

> *"one evidence source may provide many rows of judgment (eg a code document like Canada's NBC 3.8)"*

This **points the opposite way** from the 2026-08-27 *"each row of evidence provides one row for
judgment"* — and unlike that sentence it carries a concrete worked example. But a thought document
does not supersede a ruling, so **the ruling stands and Q1 stays open.**

**Q1 is NOT withdrawn. It is sharpened, and it gets easier to answer:**

> Your 08-27 ruling said each evidence row gives one judgment row. Your architecture note says one
> evidence source gives *many* — NBC 3.8 being one code document with many clauses. Under the note's
> own grain (14.2) both are true and there is no conflict: the *source* fans out, and if an evidence
> item is a source then evidence→judgment is 1:N. **Is the evidence item the source, or the
> extraction?** Answering that answers the cardinality, and nothing else needs deciding.

B2's partial unique index (`WHERE dissent_of IS NULL`) stays on the table until this is ruled — it is
the only shape that satisfies a literal 1:1 while keeping dissent, and it costs nothing to hold.

### 14.2 SIGNAL — a grain model that would dissolve four open problems, if adopted

> Evidence: *"logs all relevant items found in search with a unique reference ID, DOI/PMID and other
> codes if available, type of source"*
> Judgment: *"delivers a verdict … for what tier of evidence hierarchy it belongs to (1, 2…6)"* ·
> *"determines category of judgment item, **derives value/process/figure/goal for it**"*

| stage | the item is | live table |
|---|---|---|
| evidence | **the source** — one row per document, carrying the reference ID and identifiers | `evidence_sources` |
| judgment | **the extracted, tiered, categorised value** — one row per clause/parameter | `source_value_extractions`, re-homed |

**If adopted, this would dissolve rather than resolve the plan's hardest open problems — which is
why it is worth putting back to the owner as a question, not banking as an answer:**

- **A3-F3** (a per-source fact on a per-extraction row) — the lead key hangs on the source, which is
  now the evidence item itself. No copied fact.
- **A3-F18 / Part 9.1 X4** (the population-match grain conflict) — `evidence_population_match` grades
  a *source*; under this model that is where it belongs. The fold question disappears.
- **Part 9.1 X3** — my "25 grades over 10 sources" measurement was rejected as the wrong edge. Under
  this model it is the *right* edge and never needed to settle anything.
- **M-2 / F.1** (`judgment_items` has no column set and nothing prefigures it) — **false now.**
  `source_value_extractions` prefigures it in 48 columns. `judgment_items` is that table plus a tier
  verdict and a category.

### 14.3 SIGNAL — `base.clues` sits in substrate, not as research's hand-off

The document places clues in `base.`, and `research.matrix` **consumes** `base.clues` as one of five
search modes. Clues are an **input** to research, not its output.

**This plan's `source_locators → res_items` (Part 6.2) is put in doubt — not struck.** It stands as
the plan of record until ruled, flagged as contested.

It would also **dissolve A3-F4** rather than requiring the supersession the plan drafts: the ratified
`DR-2026-08-06` wall — *"Nothing joins it, no determination
may cite it"* — needed a recorded supersession under this plan's design. Under the owner's it needs
none. Clues stay in substrate, non-citable, an input. The conflict was an artefact of putting them in
the wrong layer.

### 14.4 TENSION — the naming grammar, unresolved

The document uses a **dotted namespace** and **substrate has a name**: `base.models`,
`base.building`, `research.matrix`, `research.logs`.

`NOMENCLATURE.md` Part D and this plan's §6.1 both say *"Substrate takes no prefix, and the absence is
the signal."* **Both cannot hold — but a thought document does not settle which survives.** SQLite has no schemas, so `base.models` maps to `base_models` —
which makes the prefix a **full word**, not `stage_id[:3]`. That retires B1's three-character collision
hazard and every table name proposed in §6.2. **Owner-owed: confirm `base_` / `research_` /
`evidence_` / `judgment_` as the literal prefixes.**

### 14.5 Measured against the DB — one figure does not reconcile

`base.clues` = *"the ~825 DOI without correct metadata."*

| | |
|---|---:|
| `source_locators` rows | **875** |
| … with a DOI at all | **448** |
| … DOI **and** missing title/authors | **251** |

**~825 matches none of the three.** Nearest is the row count, but **427 rows carry no DOI** and so do
not meet the stated definition. Either `base.clues` is *"875 leads, 448 of them carrying a DOI"*, or
it is *"the 251 DOIs actually lacking metadata."* **Owner-owed: which population is `base.clues`?**

### 14.6 CORRECTED — the missing tables are the PROPOSAL, and the medical model is RULED IN

> **Owner, 2026-08-27:** *"these nonexistent tables are because the document is just a proposal for
> what tables to make and why"* · *"yes we include the medical model too. we give our users the choice
> of what model they want to use to browse the site."*

**My framing was wrong.** I listed three `base.` members as *"have no table"* under a heading that
read as a gap analysis. They have no table **because the document is proposing to create them.**
Absence was the point, not the finding. This is the third time this session I have read a document at
the wrong altitude — first promoting a thought document to a ruling, now reading a proposal as an
audit of the existing schema.

**`base.taxonomy_medical` is RULED IN, and the reason changes what it is.** I flagged it as DG-NON
doctrine and asked for it to be ruled rather than inferred. It now is:

> **The four taxonomies are user-selectable BROWSING LENSES, not competing definitions.** The reader
> chooses which model to browse by — medical, social identity, ICF, or access needs.

That is not the project adopting the medical model. **It is user agency over how a reader's own
experience is framed, which is the social model's own commitment applied to the interface.** A
disabled reader who thinks in diagnoses is not made to translate into ICF codes to use the book, and
one who refuses the medical frame never sees it. Under CRPD Art 4.3 that is the correct posture, and
it resolves the doctrinal objection rather than overriding it.

**Design consequence, and it is structural.** Four parallel `base.taxonomy_*` members are **four views
of one substrate**, not four vocabularies to reconcile. So the crossing maps that already exist —
`population_axis_map` (53), `access_need_axis_map` (21), `access_need_icf` (43) — are not
bookkeeping. **They are the lens-switching mechanism**, and a medical taxonomy needs the same crossing
maps into the other three or the lens cannot switch. That is what makes it a schema change rather than
a vocabulary addition.

| member | live state | status |
|---|---|---|
| `base.models` (Kawa, CRPD) | no table | **to create** — proposed |
| `base.taxonomy_medical` | no table | **to create — RULED IN** as a browsing lens; needs crossing maps into identity / ICF / needs |
| `base.jurisdictions` | no table | **to create.** Confirmed needed independently: `jurisdiction` is an inert enum in `schemas/enums.py` sitting on **11 tables** with nothing behind it |
| `base.taxonomy_identity` / `_icf` / `_needs` | `populations` 23 · `axes` 17 · `access_needs` 17 | exist |

### 14.7 REFUTED — `base.sources` is not a duplication defect. It is a TARGET registry

> **Owner, 2026-08-27:** *"academic publishing institutions, research journals, university
> publications, books and articles, etc are all 'sources' for finding evidence sources. so too are
> countries, codes and standards, professional organizations, clinical bodies, and advocacy groups.
> **none of these are evidence, and none of these are research. they are all prompts for research to
> target** such that they can find evidence"*

**I called this a defect and it is not one.** I read the two `base.sources` bullets as a
source-*type* taxonomy and the academic corpus, called them *"substrate vocabulary and evidence
respectively"*, and warned that collapsing them would recreate the lead/evidence conflation.

**Both lists are the same kind of thing, and neither is the corpus.** A journal, a standards body, a
country's code authority and an advocacy organisation are all **places to go looking**. They are
prompts for research to target. The two bullets are one coherent member, and my objection was built
on reading "sources" as this project's `evidence_sources` — the admitted corpus — which is not what
the document means by the word.

**So `base.sources` is a third INPUT to the matrix, alongside `base.clues`.** `research.matrix`
crosses taxonomy × building × jurisdiction × multilingual; targets belong in that cross too — *search
THIS topic, in THIS language, AT this body.* That is a real addition to the matrix's shape, and it is
the layer that is missing rather than duplicated.

**Measured 2026-08-27: no target registry exists, and its impoverished stand-in is a free-text
column.** The nearest thing in the schema is `search_executions.engine` — recorded per query, with no
vocabulary, no table, and no CHECK behind it. R8 requires every query be logged verbatim; nothing
requires the *target* be a known one, so coverage across targets cannot be measured and a body nobody
thought to search is invisible. `base.sources` gives `engine` a vocabulary and makes target coverage
a derivable fact rather than a free-text hope.

**A NEW NOMENCLATURE FINDING, and it is the same class the owner already ruled on.** The word
**"sources" is doing two jobs**, exactly as "items" was:

| sense | means | live table |
|---|---|---|
| `base.sources` | **where to look** — journals, standards bodies, advocacy orgs | none |
| `evidence_sources` | **what we found** — the admitted corpus, 10 rows | exists |

The owner retired `items` as a table name because *"the word was the ambiguity."* **The identical
ambiguity is now proposed into the schema under `sources`**, and it should be resolved before the
table exists rather than after — which is the whole lesson of the `items` retirement. Naming one of
them for its function (`base.targets`, or `evidence.admitted`) costs nothing today and a caller sweep
later.

### 14.8 CONFIRMED — `research.matrix` is a first-class object, and it already exists

> *"base.taxonomy_x * base.building * base.jurisdictions · base.taxonomy_x * base.building *
> base.multilingual · base.topics * base.jurisdictions · base.topics * base.multilingual · base.clues"*

This is `DR-2026-08-24` §2.4's full cross-product made concrete, and **`v_coverage_priority` is that
matrix**: 7,208 rows over slugs × `lang_jur_map`. It was R6's deletion candidate and was HELD on
exactly this reasoning. It is now named as a stage object. **Do not delete it.**

### 14.9 What actually changes — nothing is struck

**Part 13 remains the operative plan.** A thought document changes no decision. What it changes is the
*question list*, and it makes one question much more valuable than the rest.

| status | items |
|---|---|
| **unchanged and operative** | the six-stage spine · hand-off keys as NOT NULL FKs · bidirectional walkability and the index requirement (§6.3) · reference IDs over surrogate integers (§6.4) · render reading across stages via views (§6.5) · the minimization tiers (§9.5) · every T-0 and T-A1 task |
| **contested, still the plan of record** | `res_items` = `source_locators` (14.3) · `<stage>_items` naming and the `[:3]` prefix (14.4) · the evidence/judgment grain and everything resting on it — X3, X4, A3-F3, A3-F18 (14.2) |
| **measured facts, true regardless** | the `~825` reconciliation (14.5) · three `base.` members with no table (14.6) · `base.sources` duplicated (14.7) · `v_coverage_priority` is the matrix (14.8) |

**THE ONE QUESTION WORTH ASKING FIRST — it is upstream of most of the rest:**

> **Is the evidence item the SOURCE (one row per document, carrying the reference ID) or the
> EXTRACTION (one row per claimed value)?**

Answer it and these fall out at no further cost: the evidence→judgment cardinality (Q1), where the
lead key hangs (A3-F3), whether the population-match fold is a rule-5 violation (A3-F18, X4), whether
`judgment_items` needs a designed column set or inherits 48 (M-2), and whether the `DR-2026-08-06`
clue wall needs a supersession at all (A3-F4). **Six open items, one question.**

Still separately owner-owed: `base.clues`' population (14.5) · `base.taxonomy_medical` as **doctrine**,
not schema (14.6) · the literal prefixes (14.4) · the duplicated `base.sources` (14.7) · and the
**synthesis / specification / render half**, which the note does not reach and on which the junction
design rests.

---

## PART 15 — The architecture note read as PROCESS, not nomenclature

Owner instruction, 2026-08-27: *"read it again as suggestions/proposals for process, don't focus on
the names specifically."* Names set aside entirely below.

### 15.1 The process it proposes is ENUMERATE → CROSS → SWEEP. The project's current one is ASK → SEARCH → ADMIT.

Every `base` member is an **exhaustive list**: *"lists all building typologies"* · *"exhaustive list
of topics"* · *"all architectural and design elements"* · *"terminology for all project-related
definitions across all languages"*. Then `research.matrix` **crosses** those lists, and searching is
sweeping the cells.

**That is a coverage-first process.** The current one is question-first: a session picks a slug,
frames searches, admits sources. The difference is not style — it is whether *"have we searched
enough?"* has an answer. Question-first has no denominator. Enumerate-then-cross has one by
construction.

### 15.2 The measurement that makes this concrete

| | measured 2026-08-27 |
|---|---:|
| `base` members with a populated table | **8 of 12** |
| absent | models · medical taxonomy · target registry · **jurisdictions** |
| searches executed, all time | **28** |
| **distinct topics searched** | **1** — of 106 |
| evidence admitted | **10** |
| smallest matrix cross (topics × language-jurisdiction) | **7,420 cells** |
| taxonomy × building × language-jurisdiction | **438,900 cells** |

**28 searches, on one topic of 106.** Against the smallest of the five proposed matrix modes that is
**0.4%**, and the project cannot currently state that number about itself because the denominator
isn't built. **The note's real diagnosis is not about tables: it is that research has been running
without a denominator.**

### 15.3 The most important thing to get right — the matrix is a DENOMINATOR, not a work queue

438,900 cells is not a to-do list, and reading it as one would kill the proposal on contact.

The note says searches are performed *"in manners **akin to**"* the crosses — describing the **shape**
of a search, not enumerating one per cell. And `DR-2026-08-24` §2.4 already settles the purpose: the
cross-product exists so applicability is **evidenced rather than presupposed**, and *"applicability is
an OUTPUT of synthesis, not an input."*

> **So the matrix defines the space and measures coverage over it. A search is a cell or a slice.
> Coverage is a fraction of a known denominator instead of a feeling.**

That distinction is the difference between an executable process and an infeasible one, and the note
does not state it. **It is the single thing most worth adding.**

### 15.4 The matrix is a structural defence against this project's worst recorded failure

On 2026-08-19 a frame was pulled as bare `axis_code`, hid that a slug spanned two demand mechanisms,
and **four of five searches were framed on one of them.** That failure changed research output and is
one of the reasons `CLAUDE.md` rule 0 exists.

**A generated cross cannot make that mistake.** If the search set is derived from taxonomy × building
× jurisdiction, framing four of five on one mechanism is not an error a session can commit — the
cross forbids it. The current defence is a rule telling agents to work from codes AND names; the
note's defence is structural. **Structural beats remembered**, which is `.claude/settings.json`'s own
stated rationale for putting the research contract in a hook rather than in prose.

### 15.5 Multilingual is an AXIS of the cross, not a translation step

Two of the five matrix modes are `× multilingual`, and the note is explicit: *"localizations and
vernacular must be incorporated — direct English translations are insufficient."*

**Process consequence: the query itself is in-language.** You do not search in English and translate
the results. Today R11 is a *filing* rule (every alias carries its in-language source, else
`[UNVERIFIED-TERMS]`); under this process it becomes a *search-generation* rule, which is much
stronger and much earlier. The 2,382 `term_aliases` rows stop being a glossary and become **search
input**.

### 15.6 REFUTED — evidence collection DOES adjudicate, and the conflict I found was manufactured

> **Owner, 2026-08-27:** *"evidence states **relevant** items, and relevancy is something that must be
> adjudicated against a topic/category/concept"*

**I called the note's evidence stage a "pure log" and built a process conflict on it.** The note says
*"logs all **relevant** items found in search"* — and relevance is not a property a document carries.
**It is a relation, adjudicated against a topic.** Collection therefore judges; it simply judges a
different question from judgment.

| stage | adjudicates | the question |
|---|---|---|
| evidence collection | **relevance** | is this document *about* this topic? |
| judgment | **tier and category**, then derives the output | is the claim sound, and what does it say? |

Two adjudications, two stages, **no conflict.** R1's phase in `governance/research-contract.yaml` is
`before-admitting`, which is exactly consistent with collection being an adjudicating stage. My
"R1 belongs at judgment" was wrong, and so was the claim that both could not hold. **Nothing needs
ruling here.** Struck.

**But the correction surfaces a real defect, and it is measured.**

If relevance is adjudicated, the adjudication has grounds, and the grounds belong on the
(source, topic) edge. That edge exists — `source_slug_links` — and it **already carries a column for
exactly this**:

| | measured 2026-08-27 |
|---|---:|
| `source_slug_links` rows | **10** |
| `relevance_note` **populated** | **0** |
| distinct topics linked | **1** |
| `search_admissions` columns recording grounds | **none** — `(exec_id, ref_id, created_at, session)` |

**The relevance adjudication is being made and never recorded.** The column is there and has never
been filled once. This is the same defect class as the 2026-08-19 fabrication — where six gates asked
whether author fields were *populated* and never whether they were *true*. Here it is one step worse:
**nothing asks whether the grounds exist at all.**

**A distinction the project is one step from conflating, and it would be expensive.**

- **Relevance** — evidence collection — *this document is about ramp gradients.*
- **Applicability** — synthesis — *this evidence bears on wheeled mobility users' ramp gradients.*

`DR-2026-08-24` §2.4 rules that **applicability** is an OUTPUT of synthesis and must never be
presupposed. That ruling says nothing about relevance, and it cannot: **relevance must be settled at
collection or nothing can be admitted at all.** Conflating them fails in both directions — defer
relevance to synthesis and admission becomes impossible; decide applicability at collection and the
DR is breached. They are different questions at different stages and the schema should not let one
stand in for the other.

**And relevance has a granularity problem the schema cannot express.** The owner names
*"topic/category/concept"* — three levels — and the note's own topic list spans two explicitly:
*"ranging from categories like circulation and acoustics to more specific elements like ramp slopes,
grab bar heights."*

Measured: **`slugs` is flat.** No parent, category, group or level column; 106 leaf topics.
(`items` does carry a `category` column — the element list is categorised, the topic list is not.)

> So a source relevant at the **category** level — a paper about acoustics generally — can only be
> linked to individual leaf slugs. It is either **copied across every acoustic topic** (rule 5) or
> **attached to none and lost**. There is no third option in the current schema.

That is a concrete, cheap fix — a parent column on the topic list — and it is a precondition for
relevance being adjudicable at the level the owner describes.

### 15.7 The largest gap: three of the four judgment outputs have nowhere to live

> *"determines category of judgment item, derives **value / process / figure / goal** for it"*

Four kinds of output. Measured against `source_value_extractions`:

| output | schema home |
|---|---|
| **value** | `claim_type`, `claimed_value`, `claimed_unit` ✓ |
| **process** | **none** |
| **figure** | **none** — and no diagram/caption/alt-text column exists in any of the 66 tables |
| **goal** | **none** |

**This is the finding I would act on first, and it is doctrinal rather than technical.** The project's
fixed doctrine is that it is *"a thinking tool and advocacy project, not an authority"* — *"the
purpose of this guidebook is to get people to ask the right questions."* **A goal and a process are
closer to that purpose than a number is.** Yet the schema can hold only numbers, so the only
determinations expressible are the ones the mission says are least central.

That also explains a symptom already on the record: 42 of 93 element names carry a determination in
the *label* — because a determination that is a goal or a process has no column to go in, so it ends
up in the name.

### 15.8 Where the volume actually is

*"one evidence source may provide many rows of judgment (eg a code document like Canada's NBC 3.8)"* —
the unit of work at judgment is the **clause**, not the document. Ten admitted sources are not ten
judgments; a single code chapter could be dozens. **Judgment is the throughput bottleneck, and it is
the stage with no writer** (`db.py` has no extraction subcommand — verified).

### 15.9 What the note does not say, and why that matters

Silent on: admission gating, the tier hierarchy's definition, population matching (R13), dissent,
synthesis, specification, render. **The proposed process is thinner than the enforced one.** That is
expected of a proposal — but it means adopting it wholesale would drop rules that exist because
something went wrong. Each of R1, R13 and the dissent contest was earned. **Port them, do not lose
them in the re-shape.**

### 15.10 The order this implies

1. **Finish `base`.** 4 of 12 members absent; jurisdictions is the urgent one — an inert enum on 11
   tables, and it is an axis of two matrix modes, so the matrix cannot be crossed without it.
2. **Build the denominator before more searching.** One topic of 106 is searched. Coverage is
   currently unmeasurable, which is the condition the note is written to end.
3. **Rule the R1 ordering** (15.6) before collection is re-shaped into a pure log.
4. **Give process / figure / goal a home** (15.7) — the mission's own outputs, currently inexpressible.
5. Then sweep.
