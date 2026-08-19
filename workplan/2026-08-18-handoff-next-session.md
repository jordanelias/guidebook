# 2026-08-18 — Handoff to the next session

**Read this before you read anything else in `workplan/`.** It is the current entry point. It
supersedes `sessions/handoff-next-session.md`, which CLAUDE.md §10 already warns is not a pointer and
may be stale.

**What this session produced:** four workplan proposals, six owner rulings folded into them, and a
Fable 5 adversarial pass that overturned four claims those documents made. Merged to `main` as
`6175c5c` (PR #106). **Nothing is executed.** No schema change, no DB write, no migration.
`PRAGMA user_version` is unchanged at 60.

**What you are picking up:** a frame that is decided but unbuilt, a cull plan with one phase blocked,
and a research restart that cannot begin until the frame lands. The next act is a single D-SCHEMA
migration. §6 gives the order.

---

## 0. The one thing most likely to waste your session

**Do not re-derive the frame.** It went through six owner rulings and an adversarial pass in one day.
The decisions in §2 are settled and were paid for. If something in them looks wrong, §5 lists what is
genuinely still open — check there first, because the alternative you are about to propose has
probably already been proposed, tested and withdrawn.

**Three proposals were withdrawn during this session, all for the same reason.** Each fixed the shape
of a determination before data existed to shape it:

| Withdrawn | Why |
|---|---|
| Re-key `specifications` to `(item_code, population_code)` → keep as is | items are being removed |
| Re-key `specifications` to `(slug, lens_type, lens_code)` | presumes the determination's shape is knowable now |
| Accept `languages` repetition across standards rows | country-level attributes multiplied; normalise instead |

If your instinct is to give `specifications` a key, read §9 of the frame proposal first.

---

## 1. Orientation in sixty seconds

The **Accessible Built Environments Guidebook** — a reference on architecture, accessibility and
built-environment standards centred on disabled people. Pre-launch, single author, governance
apparatus elaborate and real, **synthesized content essentially unpopulated**.

The project is post-**clean-room reset** (DR-2026-08-06): it proceeds *"as though no research has been
performed."* The frame stays, the corpus is demoted to reference. **Research resuming does not restore
the reset rows** — DR-2026-08-06 §4.1, and both this session's cull plan and its critique got that
wrong before being corrected.

Live state, verified 2026-08-18 (**re-derive before relying on any of it** — CLAUDE.md's standing
instruction, and these will drift):

| | |
|---|---|
| `PRAGMA user_version` | **60** |
| Doctrine SHA | **`0f2f525`** (`git rev-parse HEAD:governance/mission-and-epistemics.md \| cut -c1-7`) |
| Tables | 66, of which **43 are empty** |
| `sessions/LATEST` | `session_2026-08-16-ladder-and-vocabulary-sweeps.md` |
| `sessions/LATEST-RESEARCH` | `session_2026-07-26-energy-conservation-rest-points-seating-b3.md` |

**The two pointers mean different things and both must be maintained.** `LATEST` is continuity;
`LATEST-RESEARCH` is the subject of the *blocking* `citation_mining_session` gate. They are three
weeks apart right now, which is legitimate — no research session has closed since. **If you close a
research session, update the research pointer**, or you will point a blocking gate at a session that
did no research, which is the exact failure the split was created to prevent.

---

## 2. The six owner rulings — standing decisions, do not relitigate

All are DG-NON (owner-only). They were given across one session and are recorded in
`workplan/2026-08-18-research-frame-proposal.md`.

### R1 — `items × populations` is dead as a frame
Item codes (`E-08`, `A-03`) bias research at this stage. **93 `items` rows are archived, not deleted.**
Item names with their determinations stripped become **research slugs**.

The strip is manual, not mechanical — a regex smuggles the bias through in words instead of numbers.
`A-03 Acoustic Door (STC ≥35) at All Sensitive Space Boundaries` regex-strips to
`acoustic-door-at-all-sensitive-space-boundaries`, and *"at All Sensitive Space Boundaries"* is still
an answer. **28 of 93 carry a numeric determination; 23 of 93 carry a prescriptive condition clause.**

**Zero of the 93 stripped names match an existing slug exactly.** 106 + 93 = 199 topics, no dedup.

### R2 — three lenses, three theoretical approaches, three tables
**Disability populations** · **ICF functional demands** · **access needs**. These are not one taxonomy
seen three ways; they demand different thinking about how to design for accessibility, which is why
all three are researched against the slugs. **They stay separate tables and are never reconciled.**

### R3 — "axes" is a bad coined term; use ICF codes directly
The 17 coined axes collapse 46 ICF codes and are non-disjoint. Replace with ICF codes carrying their
own names (`b770 Gait Pattern Functions`). `axes` and `item_axis_links` are retired;
`population_axis_map` is re-derived mechanically as population↔ICF.

### R4 — jurisdictions become a real table, including the country itself
One row per geo-political scope, plus a **`research_bodies`** table for the searchable entities within
it: **the country generically**, standards bodies, government departments, **NGOs, advocacy
organisations and leading municipalities**.

**`acronym` and `full_name` are two separate columns, never one.** Searching German sources needs
*Deutsches Institut für Normung* as well as *DIN*. This matters more for advocacy bodies, whose full
names are usually non-English (*Organización Nacional de Ciegos Españoles*).

### R5 — five prioritised jurisdiction buckets
| Bucket | Members |
|---|---|
| **1** | UN · ISO · CA · US · UK · DE · NO · SE · JP · AU |
| **2** | EU · SG · NZ · IE · FR · ES · PT · FI · NL · KR |
| **3** | BR · CN · IT · DK · CH · MX · AT · BE · CO · CL |
| **4** | BD · EG · ET · GH · ID · IN · KE · NG · TZ · ZA |
| **5** | AR · CR · CY · EC · GT · MA · PE · PH · TH · UY |

**Verified exact partition:** 50 slots, 50 unique, identical to `lang_jur_map` (48) plus ISO and UN.
Nothing over-covered, nothing unbucketed. **This settles the jurisdiction-scope question (open owner
decision #6) at the 48-scope**, not the 27-code enum.

Primary-language cost: **6 → +5 → +3 → +5 → 0**. Bucket 5 adds no new language capability.

*The 10/10 split of buckets 4 and 5 is an authored proposal, not the owner's words. The DR must state
its criterion and mark it as proposed.*

### R6 — the PROVISIONAL gate no longer waits for the Global South
`governance/jurisdiction-philosophy.md` §2.3 is amended. **This is a genuine D-DOCT amendment and
needs a DR** — unlike R5, which is only a fill order.

**Only the first conjunct falls.** §2.3 has two: all-jurisdictions-recorded, and Co-1 ≥9 languages.
Buckets 1–3 supply 14 primary languages, so **the ≥9-language floor survives and is clearable.**

Replacement wording, pinned:

> A BPC entry is PROVISIONAL until every jurisdiction in **buckets 1–3** is recorded, AND the Co-1
> pass covers ≥9 languages. An entry may declare a narrower scope only on an explicit owner ruling,
> and states the buckets it covers on its face.

**The disclosure clause is an author's proposal, not the owner's ruling.** Keep them separate in the
DR. Fable upheld it as defensible doctrine but the distinction is load-bearing.

---

## 3. The corrected record — do not inherit these numbers

**Four claims made in this session's own documents were overturned by the Fable 5 pass.** They are
struck in place at each site, but a fast reader will re-absorb them. **The corrected values:**

| Claim as originally written | Corrected |
|---|---|
| "web + manual = 49 of 84 — **58%** of search effort was general web search" | **All 19 `manual` rows are deferrals, not searches.** 65 executed searches; web = 30 = **46%** |
| "nothing could compare the two [register vs practice]" | **False.** Every deferral states its reason: no alias vocabulary for HI, AR, ID, SW, BN |
| "the exotic-caller inventory is complete" (cull §6.1) | **False.** `skills/item-audit-pipeline_SKILL.md:252` invokes `scripts/audit_consolidator.py`, which Phase 4a culls |
| "the next commit touching that file turns a blocking gate red" (cull §2 item 0.7) | **False.** Rule resolution runs under `attestation_evidence` (advisory); the blocking gate is jsonschema-only and passes |
| "Canada is not in `lang_jur_map` with both en and fr — a gap" | **False.** Both PRIMARY rows exist since 2026-07-24 |
| "`slugs` carries MERGED/`merged_into` **built for** the dedup" | Columns exist; **three rows have ever used them** |
| "e150, e155, e240" as the e-code set | **Ten** e-codes: e115, e120, e125, e1251, e150, e155, e240, e250, e260, e340 |
| ICF dimension = 46 codes | **46 is wrong.** Interim floor **51** — see §5 |
| "84 rows characterise the research phase" | They cover **three days**. `search_coverage` holds 4,960 rows, 634 `SEARCHED`, with no execution log |

**Three of these share one shape: a count read without reading the rows it counted.** The 58%, the
Canada claim, and the merge machinery. Each was correct as arithmetic and wrong as a claim. That is
CLAUDE.md §10's *"a gate reporting zero may have examined zero"* — committed by an author rather than
a gate, three times in one document. **Assume it is still present somewhere in these files.**

---

## 4. Verified facts you do not need to re-derive

Established this session by direct query or file read. Schema facts are stable; **counts are not —
re-run them.**

**The extraction layer already supports record-then-bucket.** This is why R1 is cheap:
- `source_value_extractions.parameter` is **`TEXT NOT NULL`** — free text, no pre-declared vocabulary.
- `parameter_canonical` is **nullable** — bucketing is a separate, later act.
- `v_value_independence` groups by **`COALESCE(parameter_canonical, parameter)`**, *not* `item_code`.
- `item_code` survives as one nullable column among 48 on that table. Nothing groups on it.

**Staging needs no new schema.** `search_coverage` is `PRIMARY KEY (slug, jurisdiction)` with `status`
in `SEARCHED / THIN / NO-DATA / NOT-RUN`. **`NOT-RUN` is the bucket marker.** It also carries
`co1_attempted`, `tier5_attempted`, `tier6_attempted` as separate flags.

**The registers you would otherwise invent already exist in prose**, in
`skills/multilingual-research_SKILL.md`:
- Step 2a — per-jurisdiction codes/instruments, ~30 jurisdictions.
- Step 2b — beyond-code / Tier 5 bodies. **This is the NGO and advocacy register** (Habinteg, Rick
  Hansen Foundation, Procap, ONCE, IBDD, Invalidiliitto, CCS Disability Action, EDF, CEUD/NDA, KDA)
  and it already contains a municipality row: `KR | Seoul Universal Design Guidelines 2022`.
- Step 3 — a **21-database register** with language coverage and run priority, plus a regional table
  (AJOL, LILACS, SciELO, EMRO, WPRIM, IndMED).

**Seeding caveats, both found by Fable:** the skill declares its own scope as **"46 jurisdictions"** —
a *fourth* count the "12/27/48" landscape missed — and **omits AT and CY**, both bucket members, and
has no UN row. And seeding "from Steps 2a/2b" would transcribe the Seoul row that §11.4 defers.
**Exclude `body_type = 'municipality'` from the seed and reconcile the 46 against the 50 first.**

**Live counts, 2026-08-18:**

| Table | Rows | | Table | Rows |
|---|---|---|---|---|
| `slugs` | 106 (80 ACTIVE, 23 STUB, 3 MERGED) | | `items` | 93 |
| `populations` | 23 | | `axes` | 17 |
| `access_needs` | 17 | | `item_axis_links` | 158 |
| `access_need_icf` | 43 (15 codes: 5 b/d + 10 e) | | `population_axis_map` | 53 |
| `terms` | 88 | | `jurisdictional_values` | 109 |
| `term_aliases` | 2,382 | | `lang_jur_map` | 70 |
| `term_item_links` | 147 | | `decisions` | 163 |

**Zero rows, correctly:** `specifications`, `evidence_sources`, `search_coverage`,
`search_executions`, `source_value_extractions`, `gaps`. These are provisioned and empty because of
the reset. **That is the right state, not a defect.**

**Two data inconsistencies to fix before any foreign key is created:**
1. `jurisdictional_values` stores **`GB` on 20 rows** while `validate_jurisdiction.py` §4.1 lists `GB`
   as an **ERROR** and the enum mandates `UK`.
2. **UN** exists in no store — not the enum, not `lang_jur_map`, not `jurisdictional_values`. CRPD
   appears in **18 governance files and 0 value rows.** UN issues obligations, not dimensions; give it
   `kind = international` and note that it yields no measurements.

---

## 5. What is still open

**Genuinely undecided. Do not treat these as settled, and do not invent answers for them silently.**

| # | Question | Status |
|---|---|---|
| **O1** | **The ICF expansion.** 46 is wrong — `access_need_icf` names five `b`/`d` codes outside the axes' union (b164, b765, d510, d540, d550), which means **the entire d5 self-care chapter is absent** from a built-environment guidebook's demand lens. Washing, toileting, dressing. Interim floor **51**. | **Method decided, execution open.** Chapter-level enumeration from the source ICF classification, owner-ratified. Do not inherit the axes' selection. |
| **O2** | **The slug queue order.** Fable settled the *rule*: importance is circular before searching, so order by **readiness** — (a) does the alias vocabulary exist, since R11 hard-gates non-English search, (b) do leads already exist. **R1 already fixes lens order** (Co-1/T2/Co-2 first), so this is a slug queue, not a two-dimensional one. | **Adopting readiness over importance is a trajectory call — owner, DG-NON.** |
| **O3** | **Stage 6 has no mechanism at all.** Cross-examining consolidated buckets to derive categories has no table, view, script or protocol. It is where the guidebook's structure would be *discovered*. | **Deliberately not designed.** Its shape depends on what the buckets look like — designing it now repeats the withdrawn-proposal error in §0. |
| **O4** | **Municipality selection.** What makes a municipality "leading" enough to include. No external list ranks cities by accessibility practice. | **Deferred until buckets 1–2 are under way**, when the literature will have named them. That is a finding, not a guess. |
| **O5** | **Does `slugs` need a type column** once item-derived topics join? `corridor-clear-width` and `mobility-built-environment` may not be the same kind of research unit. | Open. Merging them silently may be the next umbrella error. |

---

## 6. The execution sequence

Gates are real. **Steps 1–2 are owner acts and nothing downstream should start without them.**

| # | Step | Gate |
|---|---|---|
| 1 | Ratify the five-bucket fill order (R5) | owner — **D-OP**; `jurisdiction-philosophy.md` §1.2 untouched |
| 2 | **Amend `jurisdiction-philosophy.md` §2.3** per R6 — PROVISIONAL gates on buckets 1–3, ≥9-language floor retained. **Keep the owner's ruling and the disclosure proposal as separate clauses.** | owner, **DG-NON — a real D-DOCT amendment, needs a DR** |
| 3 | Settle O1 (the ICF expansion method) | owner, DG-NON |
| 4 | Fix `GB` → `UK` in `jurisdictional_values` (20 rows) | one data migration, **before any FK exists** |
| 5 | Build `icf_codes`, `jurisdictions`, `research_bodies`, `research_indexes`, `research_index_coverage`; add `jurisdictions.bucket`; make `search_executions.engine` an **FK**; rename `term_item_links` → `term_slug_links` | **D-SCHEMA, one migration.** Mirror every change in `schemas/*.py` — drift is a CI-caught bug |
| 6 | Seed `research_bodies` and `research_indexes` from the skill's Steps 2a/2b/3 — **excluding municipalities, after reconciling the skill's 46 against the 50** | transcription, not authorship |
| 7 | Convert 93 items → slugs **by hand**; dedup 199 → *n*. Run the dedup as *"is this a real research question?"*, not only *"does this duplicate?"* | research judgment |
| 8 | Expand `population_axis_map` → population↔ICF; retire `axes` and `item_axis_links`; **archive `items` to `_archived/`, do not delete** | same migration batch |
| 9 | Seed `search_coverage` `NOT-RUN` for bucket 1; seed `research_index_coverage` likewise | D-OP, no new schema |
| 10 | First research batch | **R1–R15 DoD gate**: `python3 scripts/audit/research_batch_dod.py --session <id>` |
| — | *Stage 6 and `specifications` are **not** in this sequence* | O3 — no mechanism, no input |

**The first-batch acceptance criterion is not "one determination exists."** Deferring stages 6–7 means
no determination can be recorded until substantial research is done. Therefore:

- **`table_connectivity`'s "fully-evidenced walk" metric cannot move, and zero is the correct
  reading.** Anything treating it as a completion signal will misreport.
- The criterion is: **one consolidation bucket holds ≥2 independent roots**, with every search logged
  per R8 *including its empties*.
- **Add root-registration validity to the DoD alongside the threshold.** PR #103's P1 finding stands:
  no FK, CHECK or audit enforces root registration, so a typo in a root id silently *under*-counts
  independence, and two rows pointing at the same unregistered root can pass.

### 6.1 The cull plan is independent, and Phase 4a is blocked

`workplan/2026-08-18-cull-execution-plan.md` does not block any of the above. **But do not execute
Phase 4a as written** — it culls `scripts/audit_consolidator.py`, which
`skills/item-audit-pipeline_SKILL.md:252` invokes as Step 8, "always runs last."

**The defect is the method, not the one file.** A caller written in skill prose is invisible to a
call-graph by construction, so the whole 4a set was selected by a blind instrument. **Re-audit 4a for
prose callers before touching it.**

Fable's verdict on the cull's value, which is the owner's actual question: it is *not*
furniture-rearranging — `workplan/` and the search surface are where sessions get hurt. But measured
against *"minimize code infrastructure"*: **only ~5,000 of ~101,300 lines are code (~14% of the
35,444-line executable surface), it retires zero active registered checks, and no phase routes from
the 65-check reality to the plan's own 9-check minimum.** §0.3's "recovery plan before Phase 5"
survives as the single highest-value item.

---

## 7. Traps — every one of these was hit or nearly hit this session

1. **Read the rows, not just the count.** Three overturned claims came from counting without opening
   what was counted. `COUNT(*)` is a hypothesis.
2. **Truncated reads produce false findings.** Two near-misses: a regex that dropped a DDL line nearly
   produced a false HIGH finding about a missing CHECK constraint, and a broken `sed` range nearly
   produced a false claim that all 48 skills were unregistered. **Confirm against raw source before
   committing to a number.**
3. **Searching for one thing and reporting the absence of another.** A `grep` for a check *name*
   returned zero, and the conclusion drawn was that the *behaviour* was absent. It was not.
4. **Do not invent ID namespaces.** Eight namespaces and ~100 identifiers were coined across two days
   and then used in conversation as if shared. The owner could not follow them. **Name things by their
   path and their words.**
5. **`main` is branch-protected and can carry pre-existing failures.** Before assuming a red check is
   yours, read the actual run. `retired_vocabulary` is currently advisory-red with 70 occurrences,
   none from this session's files.
6. **The root `.ignore` hides frozen directories from ripgrep**, not from `git grep`, `grep -r`, or
   any Python tool. "No matches" is not "not present." Confirm with `ls` or Glob.
7. **Never schedule self-check-ins.** Standing owner instruction, given emphatically.
8. **Migrations only.** Never hand-edit `data/guidebook.db`. The blocking gate compares only
   `user_version` and `COUNT(*)` on six tables, so an `UPDATE` passes untouched — **the rule is
   absolute even though the enforcement is not.**

---

## 8. Where to read, in order

| For | Read |
|---|---|
| The frame, and every correction to it | `workplan/2026-08-18-research-frame-proposal.md` — **§13 is the Fable pass** |
| The cull, and what is blocked | `workplan/2026-08-18-cull-execution-plan.md` — **§14 is the Fable pass** |
| How research resumes | `workplan/2026-08-18-research-restart-plan.md` |
| Model-substitution debt and its discharge | `workplan/2026-08-18-model-substitution-log.md` §4e |
| Why the corpus was reset | `decisions/DR-2026-08-06-*` — **§4.1 especially** |
| The jurisdiction doctrine being amended | `governance/jurisdiction-philosophy.md` §1.2, §1.3, §2.3 |
| Evidence tiers and markers | `governance/tier-system.md` (operative), `governance/evidence-architecture.md` |
| Current operative rules | `references/project-standards.md` (append-only, usually ahead of the PI) |
| Repo mechanics, gates, gotchas | `CLAUDE.md` |

---

## 9. One note on process

The model-substitution log required the Opus substitute to produce a **PART 3** marking every verdict
MECHANICAL or JUDGMENT. **Fable found no PART 3 exists anywhere in the repository.** The artifact its
own terms required was never delivered, and the log recorded the debt as owed without recording that
its form was missing.

That is this repository's signature failure — an obligation discharged in name — occurring *inside the
mechanism built to prevent it*. The standing rule is now amended to require a committed path.

**If you accept work from a substitute model, check that the required artifact exists before you
record the debt as owed.** A log that reads as compliance is worse than no log.
