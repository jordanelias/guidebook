# Infrastructure remediation brief — agonist/antagonist execution plan

**Derived read-only from `jordanelias/guidebook` @ `origin/main` = `be25c89`, 2026-09-16.**
Authoring model: Fable 5.1, read-only. **No repository state was changed to produce this.**
Executing models: Opus 5 / Sonnet 5 / Haiku 4.5, assigned per item.

> **Every figure in this brief was derived by running the check, reading the script, or
> querying the DB read-only in this session. Nothing is quoted from documentation.**
> Where a documented claim and the live repository disagree, this brief says so and the
> live repository wins — that is CLAUDE.md rule 7 applied to this brief itself.

---

## 0. How to use this document

This brief is **not** a task list to burn down. It is a set of paired briefs. Each work
item ships with an **agonist** (build the fix) and an **antagonist** (break the fix), and
an item is not done until the antagonist has tried and failed to break it *and said so in
writing*.

**Read before starting anything:**

```
CLAUDE.md                                            rules 0-8, §3 spine, §5 failure modes
governance/check-registry.yaml                       the only inventory of checks
governance/pipeline-contract.yaml                    stages: and criteria
decisions/DR-2026-08-19-research-restart-operative-instrument.md
references/project-standards.md                      tail = latest owner rulings
```

**Run before starting anything:**

```
bash .claude/hooks/ensure-deps.sh            # a fresh container has no pydantic
python3 scripts/run_checks.py --all          # your baseline; keep the output
python3 scripts/run_checks.py --selftest     # MUST stay PASS through every change
```

**Baseline as measured 2026-09-16 on `be25c89` (reproduce this before you trust any delta):**

| | |
|---|---|
| `--all` | **PASS** — 54 green, 8 nothing-in-scope, 8 advisory failures, **0 blocking failures** |
| `--selftest` | **PASS** |
| `--changed-from origin/main` | PASS, 7 green, 1 advisory failure |
| schema | `PRAGMA user_version` = 84; 28 numbered migrations; 71 data migrations |
| registry | 70 active checks, 5 quarantined; 37/70 carry a real floor; 21/70 declare no authority |
| contract | 7 of 34 criteria claimed by no check |

---

## 1. The handshake: what it is and how it is enforced

The instruction is to make a **top-down holistic** pass and a **bottom-up granular** pass
meet. In this repository those two directions have concrete, checkable homes:

```
   TOP-DOWN                                              BOTTOM-UP
   ────────                                              ─────────
   CLAUDE.md rule (Layer 0)                              a row in data/guidebook.db
        │                                                     │
   governance/pipeline-contract.yaml criterion                 a line in a tracked file
        │                                                     │
   check-registry.yaml entry: basis: <stage>/<criterion>       a check's EXAMINED count
        │                                                     │
        └──────────────► THE HANDSHAKE ◄─────────────────────┘
```

**The handshake rule, stated so it can be enforced:**

> A work item is only complete when you can name, in one sentence each:
> **(a)** the contract criterion or CLAUDE.md rule it serves *(top-down)*, and
> **(b)** the specific rows or lines whose state changed, and the `EXAMINED` count that
> proves the check looked at them *(bottom-up)*,
> and **(c)** the two are the same fact viewed from opposite ends.

Where (c) fails, you have either apparatus serving no rule (CLAUDE.md §8 refuses it) or a
rule with no mechanism (Layer 1 states what nothing enforces). **Both are reportable
findings in their own right — do not quietly pick a side.**

**Failure mode this is designed to prevent.** The repository has produced "a gate that
passes having examined nothing" four separate times (CLAUDE.md §5a). The inverse is now
the live risk: a gate that examines plenty while its *registry metadata* asserts the
subject is empty. B3 below shows that has already happened, measured.

---

## 2. Model assignment policy

| Tier | Use for | Items |
|---|---|---|
| **Haiku 4.5** | Mechanical enumeration, grep sweeps, file classification against a *stated* rule, collecting line numbers. Never a judgement call. | A3-scan, A7-scan, B-inventory |
| **Sonnet 5** | Implementation against a settled design; test authoring; migration drafting; sweeps where the rule is already decided. | A1-impl, A2-impl, A3-apply, A7, C1-impl |
| **Opus 5** | Anything turning on doctrine, supersession, whether a fix is legitimate at all, or where "fixing" could falsify a record. **All antagonist roles on judgement items.** | A1-design, A2-policy, A4, A5, A6, A8, B1, B2, B5, C1-design, C2 |

**Hard floor:** `best_practice_synthesis` is Opus-only (CLAUDE.md §6). None of this work
writes one; if an item drifts into writing one, stop and re-scope.

**Assignment is per *task*, not per item.** A1 splits: Opus designs the writer's refusal
boundary, Sonnet implements it, Opus antagonises it.

---

## 3. Agonist / antagonist protocol

### Roles

**AGONIST** — builds the fix. Owns: root-cause diagnosis, the change, its tests, and the
before/after check output. Must state assumptions as `[ASSUMPTION: … — basis]`.

**ANTAGONIST** — a *separate agent instance* whose success condition is breaking the
agonist's work. Never the same context. Owns: adversarial re-derivation from primitives,
fault injection, and a written verdict.

### Rules of engagement

1. **The antagonist never reads the agonist's reasoning before forming its own.** It reads
   the diff and the repository, re-derives the claim independently, *then* reads the
   agonist's rationale to find what it assumed.
2. **The antagonist must attempt at least one fault injection** — a deliberately wrong row,
   file or value that the fix claims to catch — on a scratch copy of the DB
   (`cp data/guidebook.db $SCRATCH`, `GUIDEBOOK_DB_PATH` inline on every call). A check
   that stays green under fault injection has not been shown to work.
3. **"Survived" is a legitimate verdict.** An antagonist that fails to break sound work
   reports `SURVIVED` and says what it tried. Manufacturing a finding to look diligent is
   a worse failure than finding nothing. Equally, `SURVIVED` asserted without a recorded
   attempt is a sham and must be treated as incomplete.
4. **Disagreements escalate, they do not average.** If agonist and antagonist disagree on
   doctrine, neither wins by seniority: record both readings and put the question to the
   owner. CLAUDE.md rule 0 — a live owner statement supersedes; an agent's reading does not.
5. **Neither role may relax a check to make it pass.** Never skip, disable, quarantine, or
   loosen a gate to reach green. If a check is genuinely wrong, that is a finding with
   evidence, argued on its own terms, not a silent edit.

### Required artefacts per item

```
AGONIST REPORT
  CRITERION      : <contract criterion / CLAUDE.md rule>       ← top-down half
  SUBJECT        : <tables/rows/files touched, with counts>    ← bottom-up half
  HANDSHAKE      : <one sentence tying them together>
  ROOT CAUSE     : <why it was wrong, not just what was wrong>
  CHANGE         : <files, and why each>
  BEFORE / AFTER : <verbatim check output, both>
  EXAMINED        : <n before> → <n after>     (a drop in EXAMINED is a red flag)
  ASSUMPTIONS    : [ASSUMPTION: …]
  NOT DONE       : <anything in scope deliberately left, and why>

ANTAGONIST VERDICT
  INDEPENDENT DERIVATION : <what I computed myself, before reading the agonist>
  FAULT INJECTED         : <the wrong thing I planted, and what the check did>
  ATTACKS TRIED          : <list, including the ones that failed>
  VERDICT                : BROKEN | WEAKENED | SURVIVED
  RESIDUAL RISK          : <what I could not test, and why>
```

---

## 4. Global invariants — violating any of these fails the item regardless of outcome

1. **Migrations only.** Never write `data/guidebook.db` directly.
   `scripts/emit_data_migration.py` → `scripts/migrate_db.py`. Append-only; fix forward.
2. **`--selftest` must be PASS after every change.** `--changed-from` does not run it and
   the selftest is where a rename fails. Run it explicitly.
3. **A rename is not done until callers are swept**, and *a view is a caller, so is a skill,
   so is the check registry, so is `schemas/*.py`*. Grep `sqlite_master` as well as the tree.
   **Treat a 0-row object as unproven, not clean.**
4. **Never write the same fact into a second table.** Point, do not copy. A parity check is
   not a fix.
5. **Derive it, or name who judged it.** Do not replace one curated list with another
   curated list. If the machine can compute it, it must.
6. **Never write a bibliographic field from memory when a payload is in hand** (§5c).
7. **Adding apparatus carries the burden of proof; removing it does not.** Before adding a
   check, script or table, state what wrong thing reaches *the guidebook* if it does not
   exist. If the answer is about the apparatus, do not add it.
8. **Commit format:** `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp from
   `date -u '+%Y-%m-%d %H:%M'`. Use `governance` when no project skill fits.
9. **Attestation** is required for any change touching `references/bpc-reasoning/`,
   `references/connection-reasoning/`, `decisions/` or `sessions/`.

### 4.1 NO HARD-CODING — the invariant that governs every item in this brief

Most of the defects below can be made to "pass" by writing a number, a name or a path into
a file. **Every such fix is a regression**, because it converts a visible failure into an
invisible one that goes stale silently. CLAUDE.md rule 8 states the general form; this
section states how it is enforced on *this* programme.

**The test, applied to every change before it is proposed:**

> Could this value be **wrong tomorrow** without anything going red?
> If yes, it is hard-coded, whatever its shape — a literal, a list, a map, a glob, a
> threshold, a `min_items`, or a sentence in a document.

**The five shapes hard-coding takes here. All five are already present in this repository.**

| Shape | Live example | Why it rots |
|---|---|---|
| **Threshold literal** | `test_verification_pipeline` G01–G03: `≥50`, `≥30`, `≥100` | Written for a corpus that no longer exists (A5) |
| **Curated map** | `validate_pydantic_schemas.MODEL_TABLE_MAP` | Cannot distinguish "deliberately unmapped" from "nobody updated it" (A2) |
| **Curated floor** | `min_items: 1` on `site_pages_fresh` | Asserts a corpus state that is not true (A6) |
| **Curated exemption** | `exempt_paths`, `[RETIRED-VOCAB-OK]` | Widens silently; exempts more than it was written for (A3) |
| **Prose count** | `no_floor` reasons asserting "all four tables are 0 rows" | **Already false** — see B3 |

**Rules that follow, and they are not negotiable:**

1. **Never replace a curated list with another curated list.** If the fix for a stale list
   is a fresher list, the fix is wrong. Derive the set, and move the **burden of proof to
   the exclusions** — the shape rule 8 records for `dbcore.writable_tables(conn)`.
2. **Every exclusion, exemption or waiver must be individually falsifiable and must carry a
   dead-entry detector.** `retired_vocabulary_audit.py` already has one
   (`DEAD EXEMPTIONS: n exempt_paths entr(ies) name a path that does not exist`, currently 0).
   Any new exclusion set you introduce needs the equivalent, or you have built the next
   `WRITABLE_TABLES`.
3. **Never pin a threshold to today's measurement.** Setting G01 from `≥50` to `≥5` because
   the corpus is 5 is the same defect with a newer date. Express it as a ratio, derive it
   from the population it describes, or retire it.
4. **A count in prose must be generated or stamped.** CLAUDE.md rule 7. This applies to the
   commit message, the PR body, the check's own output, and **this brief** — see §11, which
   gives the regenerating command for every figure quoted here.
5. **A vocabulary comes from the column's own CHECK**, never a parallel list.
   `dbcore.check_values()` is the mechanism; `argparse choices=` duplicating a CHECK is
   listed in CLAUDE.md rule 8 as an outstanding violation — do not add a thirteenth.
6. **Paths, table names and stage ids are derived, not typed.** The stage ids live in
   `governance/pipeline-contract.yaml`'s `stages:` and nowhere else; `claude_md_spine`
   (blocking) enforces the one rendering of them. Never spell them out a second time.

**Antagonist standing instruction:** on *every* item, grep the agonist's diff for literals
before anything else —

```
git diff origin/main -- <paths> | grep -nE '^\+.*([0-9]{2,}|\[[^]]*"[a-z_]+"[^]]*\]|\{[^}]*:[^}]*\})'
```

— and for each hit demand the answer to the test above. **A literal that the agonist cannot
justify against that test is a `BROKEN` verdict on its own**, even if the check went green.

---

# PHASE A — the eight infrastructure defects

Ordered by dependency, not severity. A1 and A2 are independent and may run in parallel;
A5/A6 must wait on the Phase-B framing decision in B-SPINE because they may not be
defects at all.

---

## A1 — `source_locators_integrity`: 31 mismatched titles, blocked on a missing writer

**Level:** advisory · **Basis:** `evidence/locator-title-matches-identifier` · **EXAMINED:** 550

### Measured state

```
title-bearing rows: 550   titles embedding a doi: 48   mismatched: 31   unprovable: 17
```

Sample of the failure shape (verbatim):

```
[FAIL] REF-00002: doi=10.1111/jar.70142 but its TITLE embeds 10.1515/dx-2020-0005
[FAIL] REF-00004: doi=10.1108/02632770810849463 but its TITLE embeds 10.1044/0161-1461(2004/017
[NOTE] REF-00003: title embeds 10.3766/jaaa.15096 and the row carries no doi — nothing to compare
```

The check names its own blocker:

> REPAIR IS BLOCKED ON A WRITER, NOT ON A DECISION: db.py cannot set
> `source_locators.title`. It needs a `correct-locator` that reads the title from a
> persisted retrieval payload and takes no value flag, the way `correct-source` does.

### Context the executing agent must have

`source_locators` holds **893 rows: 880 `REFERENCE-ONLY` + 13 `RETIRED`**, and **zero of
them tie to a live `evidence_sources` row** (verified by query this session). This is the
prior-version bibliographic stash, not evidence.

**Why it still matters** (the CLAUDE.md §8 test — what wrong thing reaches the *guidebook*):
research contract **R9** says *pre-check the DOI; if it exists, cross-file the existing
ref_id, never duplicate.* A stash row whose title describes a different work than its DOI
will hand a future admission the **wrong title for the right DOI**. That is §5c — a
bibliographic field asserted from something other than the bytes — arriving through the
back door.

### The model to copy: `scripts/db.py:3085-3130`

`correct_source` is exactly the right shape and its docstring states the principle:

> There is deliberately no way to pass a value. … the argument names WHICH field to take
> from the payload, and the payload supplies WHAT. Fabricating a bibliographic field
> through this path requires forging the retrieval log first.

Its field boundary is not taste: `_CORRECTABLE` is *"EXACTLY what `retrieval_log
--verify-authors` can prove against a payload. A field the verifier cannot check is a
field this writer must not touch."* `_payload_for(ref_id, doi, log_session)` resolves via
`retrieval_log._logged_payloads()` + `_index_by_doi()` and **refuses** when nothing is logged.

### AGONIST brief — Opus (design) → Sonnet (implement)

**Opus, design first and write it down before any code:**

1. Decide the `_LOCATOR_CORRECTABLE` boundary. `title` is in scope. Argue explicitly
   whether `pub_year`, `authors` or `tier_claimed` belong — each must pass the same test:
   *can `retrieval_log` prove it against a payload?* If not, it must not be writable here.
2. Decide the refusal set. At minimum it must refuse: (a) no payload for this DOI in the
   named log session; (b) a row with no `doi` (there is nothing to resolve a payload by);
   (c) any attempt to pass a literal value.
3. **Decide the `status='RETIRED'` question.** 13 rows are tombstones under the 2026-09-16
   ruling that *a RETIRED tombstone is not a live DOI claim.* Does `correct-locator` touch
   them? Argue it; do not default.

**Sonnet, implement:**

4. Add `correct-locator` to `scripts/db.py` mirroring `correct_source`'s structure,
   subcommand registration (~`:1039`) and dispatch (~`:2197`).
5. Add a `scripts/tests/` test proving the three refusals fire.
6. Do **not** run it over the corpus yet — that is step 7, and it is gated.

**Then, the repair itself (Sonnet, on a scratch DB first):**

7. The 31 mismatched rows need **payloads that do not yet exist**. These are prior-version
   imports; `_payload_for` will refuse on nearly all of them. So the repair is:
   re-retrieve each DOI via `retrieval_log.fetch` → payload lands under `retrieval-log/`
   → `correct-locator --title` reads it. **Expect refusals; a refusal here is the writer
   working, not a bug to route around.**
8. Emit as a data migration. Never hand-write SQL against this table.

### The 17 "unprovable" rows — read this twice

These rows have a DOI **embedded in the title** and **no `doi` column value**.

> **TRAP — do not backfill `source_locators.doi` from the DOI embedded in its own title.**
> The check compares title-embedded-DOI against the `doi` column. Copying one into the
> other makes every row agree **by construction**, proving nothing, and converts a FAIL
> into a silent pass. That is CLAUDE.md §5a — *a gate that passes having examined nothing* —
> manufactured deliberately. The embedded DOI is as likely to be the contaminant as the truth.

Correct handling: resolve the embedded DOI against Crossref **independently**, compare the
returned title to the stored title, and only then decide whether the row's identity is the
embedded DOI or whether the title is foreign matter. If it cannot be resolved, the row
stays `[NOTE]` — *"suspect not proven"* is the honest state.

### ANTAGONIST brief — Opus

- Re-derive the 31/17 split yourself from `source_locators` before reading the fix.
- **Fault injection (mandatory):** on a scratch DB, plant a row whose title embeds a DOI
  matching its `doi` column but whose title text is otherwise a different paper. Does the
  check catch it? If not, the check tests *identifier agreement*, not *"the title describes
  a different work"* as it claims — report that as a finding against the check's own text.
- Attempt to write a title through `correct-locator` **without** a payload. It must refuse.
- Attempt to pass a literal title value by any route (flag, env var, config). Any success
  is `BROKEN`.
- Verify the repair migration replays: `scripts/migrate_db.py --rebuild /tmp/rebuilt.db`.
- Check `EXAMINED` did not fall. A drop from 550 means rows left the subject set — ask why.

**DONE WHEN:** `correct-locator` exists with proven refusals; mismatched count is reduced
with every change traceable to a logged payload; remaining rows are `[NOTE]` with a stated
reason; `EXAMINED` still 550; antagonist verdict recorded.

---

## A2 — `validate_pydantic_schemas`: 243 drift findings, and a curated map that CLAUDE.md already names

**Level:** advisory · **EXAMINED:** 20 · **Discovered:** 68 models, 20 mapped, 57/77 tables unmapped

### This is not 243 bugs. It is four classes.

Derived by reading the full output this session:

| Class | Shape | Example | Correct treatment |
|---|---|---|---|
| **A — audit columns** | `created_at`, `created_by_session`, `updated_at`, `updated_by_session` reported DB-only on nearly every model | `slug.Slug`, `decision.Decision` (these are their *only* drift) | **One systematic exclusion**, not N fixes. These are infrastructure columns no Pydantic entity models. |
| **B — abandoned mirrors** | Model never updated after a schema reform | `evidence_source.EvidenceSource`: DB has ~80 columns absent from Pydantic; Pydantic declares `title`, `year`, `used_in_slugs` which **do not exist in the DB** | Rebuild or retire the model. Pydantic-only fields that name no column are the dangerous half. |
| **C — models for dead tables** | Table empty/retired | `item.Item` (`items` = 0 rows), `conflict.Conflict`, `bpc_metadata.BPCMetadata` | **CLAUDE.md §8: deleting is as cheap as adding.** Argue deletion first. |
| **D — a missed rename sweep** | Pydantic kept the old names | `population.Population` declares `code`, `label`, `definition`; DB has `population_code`, `display_name`, `description` | **This is a CLAUDE.md rule 4 violation**: `schemas/*.py` is a caller and the sweep missed it. Fix and record. |

**Class D is the finding that matters most** — it is evidence that a past rename was
declared done while a caller still named the old columns, which is the exact defect
rule 4 exists to prevent and migration 064 was written to correct.

### The second defect, already named by Layer 0

CLAUDE.md rule 8 lists this script's `MODEL_TABLE_MAP` among the **known outstanding
violations** of *derive it, or name who judged it*. The script's own docstring concedes it:

> `MODEL_TABLE_MAP` is a curated, versioned mapping (same convention as `claims_docket.py`'s
> `TRIGGERS` / `EXTRA_RULE_IDS`)

**And the map is already blind in the direction the rule predicts:** 57 of 77 live tables
have no mapped model. The map cannot tell "deliberately unmapped" from "nobody updated the
map" — which is precisely how `dbcore.WRITABLE_TABLES` went blind eight times.

### AGONIST brief — Opus (policy) → Sonnet (sweep)

**Opus, decide and document the direction-of-drift policy the script says is "separate,
future work".** For each class above, state the rule:

- Class A → a declared, named exclusion set with a stated reason (not a silent skip).
- Class B → model rebuilt from `PRAGMA table_info`, or model deleted. Pick per model, argue it.
- Class C → deletion is the default; state what reads the model before keeping it (§8:
  *"nothing is added without naming what reads it"* — an unread model is the same defect).
- Class D → fix, and open the question of what *else* that rename missed.

**Opus, then attack the map itself.** Derivation candidate: a model maps to a table when
its snake_cased class name matches a live table name, **with an explicit, reasoned
exclusion list carrying the burden of proof** — exactly the shape rule 8 describes for
`dbcore.writable_tables(conn)`: *"it is now derived, and the burden of proof moved to the
exclusions."* The two deliberate non-mappings (`schemas.room.*`, `schemas.specification.Specification`)
are already documented with evidence and become the seed of that exclusion set.

**Sonnet, implement** the policy and the derivation. Do not hand-maintain a second list.

### ANTAGONIST brief — Opus

- **Fault injection (mandatory):** add a column to a scratch DB table and confirm the audit
  reports it. Then add a *model field naming no column* and confirm it is reported too —
  the Pydantic-only direction is the one that silently lies.
- **The decisive test:** create a new table on a scratch DB and confirm the *derived* map
  notices there is no model, rather than silently omitting it the way the curated map does.
- Verify `derived_not_curated_audit` (blocking) still passes and that you have not merely
  moved the curation somewhere it does not look.
- Challenge every Class-C deletion: does anything import it? `grep -rn "from schemas" scripts/`.

**DONE WHEN:** policy documented; map derived with reasoned exclusions; Class D fixed and
its rename gap reported; drift count reduced *by class* with each class's disposition
stated; `derived_not_curated_audit` still green.

---

## A3 — `retired_vocabulary`: 62 occurrences, most of which must NOT be edited

**Level:** advisory · **EXAMINED:** 26 register entries

### Measured breakdown (from the audit output this session)

| Entry | Token | Count |
|---|---|---|
| RV-001 | `applicable_groups` | 2 |  [RETIRED-VOCAB-OK]
| RV-012 | `UNVERIFIED-1` | 13 |  [RETIRED-VOCAB-OK]
| RV-016 | `VERIFIED-WITH-CORRECTION` | 37 |  [RETIRED-VOCAB-OK]

### Why "fix the text" is wrong for most of these

The hits land in three very different kinds of file, and **the audit's own remedy sentence
offers all three treatments** — *"Fix the text, or … add the path to that entry's
`exempt_paths`, or append `[RETIRED-VOCAB-OK]` to the line."*

1. **Frozen session records** — `scratchpad/pr-131-project-status-overview/inert-inventory.md`,
   `scratchpad/session_2026-08-25-pipeline-smoke-test-mobility/…`. These are the historical
   record of what was true then. **Editing them falsifies history.** The `inert-inventory.md`
   hit is especially instructive: it is a *report about retired vocabulary* that trips the
   retired-vocabulary audit — a textbook licensed mention.
2. **Bibliographic data files** — `references/tier{1,2,3}-verified-sources.json`,
   `references/co1-verified-sources.json` carry `"status": "VERIFIED-WITH-CORRECTION"`,  [RETIRED-VOCAB-OK]
   a value retired by DR-2026-08-04 (D-0157) and migrated in the DB by
   `data_20260804164915`. **The DB was migrated and these JSON mirrors were not.** That is
   both a rule-4 caller sweep miss *and* a rule-5 question: why do these files hold a
   second copy of source status at all?
3. **Live prose** — `references/bpc/…`, `references/methodology/…`. Genuine wrong answers
   waiting for whoever greps next. These are the real fixes.
4. **`governance/project-instructions-v10_14.md`** — §7 of CLAUDE.md says PI versioning is
   intentional and the live PI *legitimately lags doctrine*. **Verify these two hits are
   even real** before touching: the reported lines do not visibly contain the token and the
   audit truncates lines at display width, so this may be a reporting artefact or a false
   positive. Confirm with `grep -n 'UNVERIFIED-1' governance/project-instructions-v10_14.md`.  [RETIRED-VOCAB-OK]

### AGONIST brief — Haiku (enumerate) → Opus (classify) → Sonnet (apply)

**Haiku:** produce the complete occurrence list — file, line, token, and the full line
untruncated. No judgement. Output a table.

**Opus:** classify every occurrence into `FIX-TEXT` / `LICENSED-MENTION` /
`FROZEN-RECORD` / `FALSE-POSITIVE` / `DATA-MIGRATION-OWED`, with a one-line reason each.
The class-2 JSON files need a separate decision: migrate the value, or establish that these
files are themselves superseded by the DB and should be retired under §8.

**Sonnet:** apply — text fixes for `FIX-TEXT`, `[RETIRED-VOCAB-OK]` for `LICENSED-MENTION`,
`exempt_paths` entries for `FROZEN-RECORD`.

> **Note the audit has a dead-exemption detector** (`DEAD EXEMPTIONS: n exempt_paths
> entr(ies) name a path that does not exist`). It reported `0 dead exemption(s)` this
> session. Keep it at 0 — an exemption pointing at a deleted path is the same rot one level up.

### ANTAGONIST brief — Opus

- **Every `exempt_paths` addition is an attack surface.** For each one, ask: does this glob
  exempt more than the frozen record it was written for? `_archived/**` is legitimate;
  `references/**` would be a hole.
- **Fault injection:** plant the retired token in a genuinely live file and confirm the
  audit still catches it after the exemption sweep. If exemptions have widened enough to
  swallow it, the fix has disarmed the check.
- Challenge every `LICENSED-MENTION`: a mention is licensed when the text is *about* the
  retirement. A sentence that *uses* the term to mean the thing is not licensed however
  historical its file.
- Verify the class-2 JSON decision against rule 5 — if those files duplicate DB state, the
  fix may be deletion, not migration.

**DONE WHEN:** every occurrence classified with a reason; live-surface uses fixed;
exemptions narrow and justified; dead exemptions still 0; fault injection still caught.

---

## A4 — `validate_reasoning`: the only real reasoning document fails 15 ways, over a corpus that no longer exists

**Level:** advisory · **EXAMINED:** 3 (2 templates skipped, 1 real doc)

### Measured state

`references/bpc-reasoning/room-acoustic-performance.md` fails on:

```
Missing required header field: **BPC file**, **BPC population**, **Generated**
Status 'PILOT' not in ['COMPLETE', 'DRAFT', 'OPUS-PENDING']
Missing required section: A. Evidence inventory, A.1, A.2, A.3, A.4, A.5,
                          B. Per-parameter reasoning, C, D, E, F
```

This is not a document that drifted from the template. **It predates the template
entirely** — status `PILOT` is not in the current vocabulary at all.

### The fact that decides this item

**The corpus this document reasons over no longer exists.** Derived this session:
`room-acoustic-performance` has **28 `search_executions` across batches 01–03** but
**0 `source_slug_links`, 0 `source_value_extractions`, 0 live `evidence_sources`**. Its
four open gaps record why — `GAP-B01-001`: *all five batch-1 admissions had FABRICATED
author lists*; `GAP-B02-001`: *batch 2 admitted five sources on metadata alone, no full
text read.*

**So "bring it to template" would mean re-rendering reasoning over evidence that was
withdrawn for fabrication.** That is the §5c failure mode with extra steps.

### AGONIST brief — Opus only. This is a judgement item.

Three candidate dispositions — argue all three, pick one, record the warrant:

1. **Archive it.** `_archived/` is the right home for retired reader-facing content (§8).
   Its corpus is gone; the document is a record of superseded reasoning.
   **Cost:** `validate_reasoning` then examines only templates and becomes vacuous —
   you trade a FAIL for a NOTHING-IN-SCOPE. Phase B must then classify it (see B-SPINE).
2. **Rebuild to template.** Only defensible if the reasoning can be re-derived from
   evidence that still stands. **It cannot** — there is none. Effectively excluded, but
   say so explicitly rather than skipping it.
3. **Mark as superseded in place** with a header the validator recognises.
   Requires extending the status vocabulary — which is apparatus added to preserve a
   document whose evidence was withdrawn. Apply the §8 test before proposing it.

**Whichever is chosen: this touches `references/bpc-reasoning/`, so it REQUIRES an
attestation** (`attestations/<slug>.json` against `schemas/attestation.schema.json`,
CLAUDE.md rule 2). That is also the natural way to give Phase B's changeset-scoped
attestation gates a real subject — see B2.

### ANTAGONIST brief — Opus

- Verify the corpus claim independently. If *any* live evidence reaches this slug, option 2
  reopens and the agonist's premise collapses.
- If archiving: confirm nothing live links to the document — `grep -rn "room-acoustic-performance" references/ governance/ scripts/ decisions/`, and check `.ignore` does not hide a caller (`grep -r` and `git grep` see through `.ignore`; the Grep tool does not).
- **Report the vacuity trade explicitly.** An agonist that archives the file and reports
  "validate_reasoning no longer fails" has converted a visible failure into an invisible
  one. That is a `WEAKENED` verdict unless Phase B handles it.
- Verify the attestation exists, validates, and that its free text says something true —
  **no gate reads attestation free text for meaning** (CLAUDE.md rule 2), so the antagonist
  is the only reader.

**DONE WHEN:** disposition chosen with a written warrant; attestation present and true;
vacuity consequence stated and routed to Phase B; antagonist verdict recorded.

---

## A5 — `test_verification_pipeline`: 3 failures that are corpus assertions wearing a unit test's clothes

**Level:** advisory · **Basis:** `hygiene` · 15/18 pass

### Measured state — and the pattern is unmistakable

```
[✓] A01–A02  schema columns present
[✓] B01–B03  CrossRef field population
[✓] C01–C03  author list / ORCID handling
[✓] D01–D02  crossref_doi_lookup success and transient-403
[✓] E01–E02  Phase-4 candidate selection
[✓] F01–F02  metadata_quality promotion
[✗] G01: Live DB has language populated on ≥50 sources after Phase 4 production run
[✗] G02: Live DB has ORCID populated on ≥30 authors (was 0)
[✗] G03: COMPLETE metadata count ≥ 100 (was 67 pre-V1.2)
[✓] G04: Most recent pipeline_runs record includes Phase 4 metrics
```

**Every unit test passes. Every failure is a G-series assertion about live-corpus scale.**

The live corpus is **5 `evidence_sources`** (derived this session). The thresholds ≥50,
≥30, ≥100 were written against a corpus that the **2026-09-13 owner ruling deliberately
destroyed** — *"all the circulation rows that have been produced are not able to be
trusted, so we have to redo them all from the start"*, executed by
`data_20260913040739_2026-09-13-clear-circulation-corpus.sql` (229 rows).

### The diagnosis

These three assertions **cannot pass until the corpus is ~20× its current size**, and
nothing in the remediation programme will make that happen. They are therefore
**red by construction** — the exact property CLAUDE.md rule 6 identifies as corrosive:

> a check that is red by construction teaches its reader to ignore it

A tooling test whose subject is the production corpus is a category error: it conflates
*"does the enrichment code work"* (A–F, all green) with *"has enrichment been run at scale"*
(G01–G03), and the second question does not belong in `scripts/tests/`.

### AGONIST brief — Opus. Do not "fix" this by growing the corpus.

1. **Separate the two subjects.** A–F and G04 are unit/integration tests of the pipeline
   code. G01–G03 are corpus-state assertions. Decide where each belongs.
2. For G01–G03, choose and argue:
   - **Retire them** (§8: removing apparatus does not need permission, only evidence —
     and "asserts a corpus size the owner deliberately abandoned" is evidence), **or**
   - **Re-express them as ratios or as derived thresholds** — e.g. *"of sources with a DOI
     and a logged payload, ≥X% carry `language`"* — so the assertion scales with the corpus
     instead of assuming one. This is rule 8 applied to a test: derive the threshold,
     never hand-write it.
3. **Do not** set the thresholds to the current numbers. That is hand-curating a figure the
   schema can compute, and it will go stale on the next batch exactly as these did.

### ANTAGONIST brief — Opus

- **The trap to test for:** did the agonist make G01–G03 pass by lowering a constant? Check
  the diff for literal numbers. A threshold of `>= 5` is the same defect as `>= 50`, only
  newly wrong instead of anciently wrong.
- **Fault injection:** if the agonist re-expressed G01–G03 as ratios, break the pipeline on
  a scratch DB (blank every `language`) and confirm the test goes red. A ratio test over a
  5-row corpus may be statistically vacuous — if 1 row can swing it, say so.
- If tests were retired: confirm nothing else covered that behaviour, and that the retirement
  is recorded in the commit per §8.
- Confirm `research_dod_selftest` and `run_checks --selftest` still pass.

**DONE WHEN:** unit and corpus subjects separated; G01–G03 retired or derived, never
re-pinned to a literal; the test is green for a reason that survives the next batch.

---

## A6 — `site_pages_fresh`: 0 pages, and the vacuity guard already caught it

**Level:** advisory · **EXAMINED:** 0 · floor: `min_items: 1`

### Measured state

```
FRESH: 0 page(s) match a fresh render.
EXAMINED: 0
VACUITY GUARD: examined 0 item(s), below the declared minimum of 1
```

`site/` contains only `assets/`. The render stage has no output. Derived this session:
**0 determinations at `state='stated'`** — both `specifications` rows are `pending`, and
one is retired-and-superseded.

### The diagnosis — and why this is the cleanest handshake example in the brief

`render` is the last stage of the spine
(`base → research → evidence → judgment → synthesis → specification → render`).
**A render surface with nothing on it is the correct downstream consequence of a
specification stage with nothing determined.** The check is not broken; it is reporting the
truth about the corpus.

**But it carries `min_items: 1`, which asserts the opposite** — that at least one page
*should* exist. The registry metadata and the corpus disagree, and the metadata is the
thing that is wrong.

This is the mirror image of B3's finding, and the two must be fixed by the same mechanism.

### AGONIST brief — Opus

1. Establish whether *any* page is legitimately buildable today. Read
   `scripts/generate/build_site.py` and determine what it renders from. If pages can be
   built from base vocabulary alone, the 0 is a real defect — build them.
2. If pages require determinations, then `min_items: 1` is a false claim about the corpus.
   Convert it to a `no_floor` with an **honest, falsifiable reason** in the register's own
   idiom — and crucially, **with a stated ratchet trigger**, the way `medical_lens_integrity`
   does: *"RATCHET TO `min_items: 1` in the same change that writes the first …"*.
3. **Do not generate placeholder pages to satisfy the floor.** That manufactures a subject
   so a gate can examine it — §5a inverted, and it puts fabricated surface into the book.

### ANTAGONIST brief — Opus

- Verify claim (1) independently by reading the builder, not by trusting the agonist.
- If converted to `no_floor`: is the reason **falsifiable**? A reason that cannot ever be
  checked is a permanent excuse. Does it name the exact condition that ratchets it back?
- Confirm the change does not make the render stage unmonitored — what still fails if the
  builder itself breaks?
- `pipeline_completeness_fresh` and `evidentiary_audit_fresh` are **blocking** and currently
  PASS. Confirm they are not passing vacuously for the same reason.

**DONE WHEN:** buildability established from the builder's code; floor matches reality; a
ratchet trigger is stated; no placeholder content was created.

---

## A7 — `validate_schema_cross_check`: one lead live, absent from the archive

**Level:** advisory · **EXAMINED:** 84

### Measured state

```
Cross-entity provenance: 83 archived lead(s), 84 live
Cross-entity integrity: 1 issues
  in research_code_leads, absent from the archive: INT / Ramp gradient ceiling — retrieve the clause value
```

The delta is exactly **one row: batch 08's new lead**, created 2026-09-16.

Note also: `ENTITY_REGISTRY declares no entity type, so there is no YAML entity corpus to
validate` — 0 of the 84 examined subjects are entity files. The check is doing only half
of what its name implies.

### AGONIST brief — Sonnet (Haiku may do the enumeration)

1. Read `scripts/validate_schema.py --cross-check` and determine what "the archive" is and
   **what is supposed to keep it in step**. Is archiving a manual step a batch owes, or an
   automated mirror that failed to fire?
2. If manual and owed: perform it for this row, and **report the process gap** — a manual
   sync step that a research batch can forget will forget again. That is a rule-8 candidate.
3. If automated: find why it did not run for batch 08.
4. Separately report the empty `ENTITY_REGISTRY` to Phase B — a check examining 84 subjects
   of which 0 are its nominal primary subject is half-vacuous and the registry does not say so.

### ANTAGONIST brief — Sonnet, escalate to Opus if (2)

- **Fault injection:** add a second unarchived lead on a scratch DB; confirm the count goes
  to 2 and the row is named.
- If the agonist archived the row by hand, ask the structural question: what stops the 85th
  lead from recurring this? A fix that resolves one row and leaves the mechanism is a
  `WEAKENED` verdict.
- Confirm the archive is not simply a second copy of live state — **rule 5**: if the archive
  duplicates `research_code_leads`, the parity check between them *"is not a fix — it makes
  a dual home survivable, therefore permanent."* This is the sharpest question on this item.

**DONE WHEN:** the row is reconciled *and* the mechanism that let it drift is named; the
rule-5 question about archive-as-duplicate is answered on the record.

---

## A8 — `research_protocol_audit`: REF-00987 lacks `search_queries_used`

**Level:** advisory · **EXAMINED:** 21 · 1 issue

### Measured state

```
[CHECK 8] Verified citations lacking search_queries_used: 1
  ⚠ REF-00987: 2010 ADA Standards for Accessible Design
```

### The reason this is an Opus item and not a one-line backfill

**CHECK 7, immediately above it, refuses the analogous backfill in its own output** — and
the reasoning transfers:

> (1 further source admitted by searches logged before 2026-09-03, when db.py did not yet
> refuse a log-search without a prior. `search_executions` is append-only under R8 and
> `amend-search` cannot write this column, so no sanctioned path can ever clear them.
> **NOT counted as issues, and NOT to be backfilled: a prior written now would be a
> reconstruction, which is the artefact this field exists to prevent.**)

REF-00987 is named under **both** checks. CHECK 7 declines to count it; CHECK 8 counts it.

**The question the agonist must answer:** is `search_queries_used` a *record of what was
done* (in which case writing it now is the same reconstruction CHECK 7 forbids) or a
*derivable pointer* (in which case it should not be a hand-written column at all — rule 5
says point, do not copy, and `search_executions` already holds the queries)?

REF-00987 was admitted at `2026-09-16 05:44` by the batch-08 session via
`verified_by_tool='retrieval_log.fetch'`, and the session's searches **are** in
`search_executions`. So the data exists; the question is whether the column should hold a
copy of it.

### AGONIST brief — Opus

1. Determine whether `search_queries_used` duplicates `search_executions.query_text`
   reachable by the shared session/ref pointer. **If it does, this is a rule-5 violation and
   the fix is to retire the column, not to fill it** — writer-retire, reader-retire, NULL
   forward, per rule 5's stated sequence. First check `grep scripts/migrations/data_*` — a
   column a committed data migration INSERTs can never simply be dropped.
2. If it is genuinely independent, decide whether a sanctioned writer exists and whether
   writing it now is a record or a reconstruction. **Apply CHECK 7's own standard.**
3. Whichever way: CHECK 7 and CHECK 8 currently treat the same source differently. That
   inconsistency is itself a finding — report it even if REF-00987 is resolved.

### ANTAGONIST brief — Opus

- **The core attack:** if the agonist backfilled the column, demand the evidence that the
  value is a record rather than a reconstruction. "The queries are in the DB so I copied
  them" is a rule-5 violation dressed as a repair.
- Verify the `data_*` migration grep was actually run before any drop was proposed.
- Confirm `research_batch_dod.py --session session_2026-09-16-research-batch-08-ramp-gradient`
  stays **COMPLIANT on all 19 rules** — it is today; any change that breaks it is `BROKEN`.
- Test the CHECK 7 / CHECK 8 inconsistency independently: construct the case where one
  counts and the other does not, and confirm the agonist's account of why.

**DONE WHEN:** the record-vs-reconstruction question is answered on the record; the
CHECK 7/8 inconsistency is reported; batch-08 DoD still COMPLIANT.

---

# PHASE B — the blocking-and-vacuous gates

Run **after** Phase A. Several Phase-A outcomes change what a gate's correct zero-state is
(A4 may make `validate_reasoning` vacuous; A6 may convert a floor). Starting Phase B first
means re-doing it.

## B-SPINE — the finding that reframes this whole phase

`run_checks.py` reports and escalates:

```
NOTHING-IN-SCOPE (8): validate_verification_consistency, attestation_presence,
  attestation_schema, attestation_verdict, population_integrity_audit, pmp_audit,
  reasoning_doc_citations_audit, medical_lens_integrity
  BLOCKING and vacuous (3): validate_verification_consistency, attestation_presence,
  attestation_schema — a gate that examined nothing gated nothing.
```

**Reading the registry's own `no_floor` declarations shows these eight are not one
phenomenon. They are four, and only two are problems.**

| Kind | Meaning | Checks | Is it a defect? |
|---|---|---|---|
| **CHANGESET** | Scoped to `HEAD~1..HEAD` by design; 0 means this commit touched no such path | `attestation_presence`, `attestation_schema`, `attestation_verdict` | **No.** Correct on every non-synthesis commit, i.e. most commits, forever |
| **CORPUS-EMPTY (true)** | The table really is 0 rows | `population_integrity_audit`, `pmp_audit`, `reasoning_doc_citations_audit` | No, but the ratchet is owed |
| **CORPUS-EMPTY (stale)** | Reason asserts empty; **the corpus is not empty** | `research_protocol_audit` (advisory, so not in the blocking-3) | **Yes — the metadata is false** |
| **VOCABULARY OWED** | Rows are owed by a ruling, not absent by nature | `medical_lens_integrity` | Yes — work is owed |

**So the "BLOCKING and vacuous (3)" escalation is two-thirds false alarm.**
`attestation_presence` and `attestation_schema` are changeset-scoped; their registry notes
say so explicitly — *"a floor would fail every non-synthesis commit"*. Escalating them
every time a non-synthesis commit lands trains the reader to ignore the escalation, which
is CLAUDE.md rule 6's stated corrosion mechanism applied to `run_checks` itself.

### B-SPINE agonist brief — Opus

1. **Give the zero-state a derived kind, not a prose reason.** Add a declared field to the
   registry — e.g. `empty_kind: changeset | corpus | vocabulary_owed` — and have
   `run_checks.py` report each kind separately. **Do not hard-code a list of check ids** into
   the reporter; read the kind from each check's own entry (§4.1 rule 6).
2. **Escalate only what is genuinely anomalous:** a `corpus` check whose subject is *not*
   empty (stale metadata), and a `vocabulary_owed` check past its ratchet trigger.
   A `changeset` zero on a commit out of scope is normal output, not an alarm.
3. Apply CLAUDE.md §8 before adding anything: *what wrong thing reaches the guidebook if
   this does not exist?* **Answer, and it is a strong one:** a blocking gate that examined
   nothing while its metadata says "empty by decision" is how an entire defect class passes
   unnoticed — §5a records four occurrences. A false-alarm channel is how that goes unread.

### B-SPINE antagonist brief — Opus

- **Fault injection:** make a commit that *does* touch `references/bpc-reasoning/` without an
  attestation. `attestation_presence` must go RED, not NOTHING-IN-SCOPE. If it does not, the
  changeset classification has disarmed a blocking gate and the verdict is `BROKEN`.
- Confirm no check id is hard-coded in the reporter. Grep the diff for string literals
  naming checks.
- Confirm `--selftest` C5/C7/C8 still pass and that a new registry field did not break
  C8's floor/no_floor exclusivity rules.

---

## B1 — `validate_verification_consistency` (BLOCKING, vacuous): the reason is wrong, the count is right

**Measured:** `EXAMINED: 0`. The check counts `stated`/`provisional` rows in `specifications`.

**Its `no_floor` reason says:**

> the `specifications` table is genuinely unpopulated pre-Phase-E, not a broken sweep

**Derived this session: `specifications` holds 2 rows.** Both are `state='pending'`, and one
is retired-and-superseded. So `EXAMINED: 0` is arithmetically correct — no `stated` or
`provisional` row exists — but **the stated reason is false**: the table is populated.

**This matters because the two facts have different futures.** "Table unpopulated" resolves
when any row lands; "no row has reached `stated`" resolves only when a determination
survives adjudication. A reader acting on the first will think the gate is live when it is
not.

**AGONIST (Opus):** rewrite the reason to say what is actually true, and state the ratchet
trigger in the idiom `medical_lens_integrity` already uses — *"RATCHET TO `min_items: 1` in
the same change that writes the first `stated` determination."* **Do not write a number.**

**ANTAGONIST (Opus):** verify the rewritten reason is falsifiable by query, and that the
ratchet trigger names a condition a script could evaluate rather than a date or a phase name.
Then ask the harder question: **should a blocking gate over determinations have gone this
long with no subject?** Report it either way.

---

## B2 — the attestation trio: not defects, and A4 will give them a subject

`attestation_presence` / `attestation_schema` / `attestation_verdict` are changeset-scoped
(`adherence_log_audit.py --base/--head`). 128 attestation files exist on disk; the checks
look only at the diff.

**No fix is owed here.** Two actions:

1. Fold them into B-SPINE's `changeset` kind so they stop being escalated.
2. **A4 is the natural live test.** Whichever disposition A4 takes, it touches
   `references/bpc-reasoning/` and therefore *owes an attestation*. Run the trio on that
   commit: `attestation_presence` and `attestation_schema` must both go from
   NOTHING-IN-SCOPE to a real examination. **If they do not, that is a live blocking-gate
   failure and it outranks everything else in this brief.**

**ANTAGONIST (Opus):** do not accept A4's attestation as proof the gates work until you
have also confirmed the *negative* case — remove the attestation on a scratch branch and
confirm `attestation_presence` fails. Note CLAUDE.md rule 2: **no gate reads the free text
for meaning**, so read it yourself and say whether it is true.

---

## B3 — `research_protocol_audit`: the proof case that `no_floor` reasons go stale

**Its `no_floor` reason asserts:**

> EXAMINED sums COUNT(*) over the four source tables checks 1-9 read (gaps,
> evidence_sources, evidence_population_match, search_languages) — **all four are 0 rows
> today** post clean-room-reset (2026-08-06)

**Derived this session:**

| Table | Reason claims | Actual |
|---|---|---|
| `gaps` | 0 | **11** |
| `evidence_sources` | 0 | **5** |
| `evidence_population_match` | 0 | **5** |
| `search_languages` | 0 | 0 |

**And the check itself reports `EXAMINED: 21` and finds 1 issue** (A8). It is not vacuous at
all. Its registry entry describes a repository that stopped existing over a month ago.

**This is the single clearest instance of §4.1's "prose count" hard-coding**, and it is the
warrant for Phase C.

**AGONIST (Sonnet, design by Opus in C1):** ratchet this check to a real `min_items` derived
from its subject, and delete the false reason. **The floor value must not be typed** — see C1.

**ANTAGONIST (Opus):** check every *other* `no_floor` reason for the same rot before
accepting a one-check fix. If more than one is stale, a per-check repair is the wrong shape
and C1 must land first. **This is a dependency judgement, and getting it wrong costs the
whole phase.**

---

## B4 — the three honest corpus-empty checks

Verified this session — all three reasons are **currently true**:

| Check | Subject | Rows |
|---|---|---|
| `population_integrity_audit` | `citation_population_links`, `probe_population_links`, `extraction_population_links` | 0, 0, 0 |
| `pmp_audit` | `spec_value_probes` | 0 |
| `reasoning_doc_citations_audit` | `reasoning_doc_citations` | 0 |

**No fix owed.** Each needs a stated, machine-evaluable ratchet trigger under C1. Note
`spec_value_probes` is among the **21 unwritable columns** (its `item_code` FK reaches the
emptied `items`), so its ratchet is blocked upstream — say so in the reason rather than
implying rows are merely awaited.

---

## B5 — `medical_lens_integrity`: rows are owed, and two tables cannot accept them

`base_taxonomy_medical` holds 0 rows. Derived this session, **`icf_medical_map.medical_code`
and `identity_medical_map.medical_code` are both UNWRITABLE** — NOT NULL FKs into that empty
table. The lens cannot be crossed to until the vocabulary is minted.

The registry entry records a **corrected** owner ruling — and the correction history is the
point:

> It read "blocked on an owner licensing ruling"; the owner then ruled "use ICD-11" … Its
> second version said the lens was DEMAND-POPULATED and that 0 measured demand; the same-day
> adversarial pass superseded that … because demand-population yields zero rows and so
> re-instates the deferral the owner had overruled hours earlier.
> **THE RULING AS CORRECTED: populate by CORRESPONDENCE from the registries already held —
> 17 axes and 23 populations, less the identity-first and umbrella codes taking no anchor**

**AGONIST (Opus):** this is content work under an owner ruling, not apparatus repair.
Derive the correspondence set from the live `axes` and `populations` registries — **do not
type a list of codes.** The bound (~15–20) is the ruling's estimate, **not a target**: if the
derivation yields a different number, the derivation wins and you report the discrepancy.
Mint via `db.py add-medical`, which refuses the three failure modes the entry names
(diagnosis-only lens, value-bearing `display_name`, crossing-less row).

**ANTAGONIST (Opus):** verify the exclusion of "identity-first and umbrella codes" is
derived from a property of those rows, not from a hand-picked list. **Fault-inject all three
refusals** — the entry records that this was already done on 2026-09-11 and they fired;
confirm they still do. Then confirm the two map tables became writable, which is the
falsifiable consequence.

---

# PHASE C — cross-cutting: make the floors self-policing

## C1 — the floor ratchet audit (the anti-hard-coding engine)

**This is the highest-leverage item in the brief, and B3 is its proof case.**

`--selftest` already reports, as INFO:

```
checks with a real floor: 37 of 70 — every no_floor is a corpus that cannot yet falsify its
check; ratchet this up as the corpus fills
checks with no stated authority: 21 of 70 — ratchet this down, do not invent authorities
```

**33 checks carry a `no_floor` prose excuse. At least one (B3) is already false. Nothing
checks them.** They are maintained by memory, which is the condition rule 8 exists to end:

> None of these is ever a list maintained alongside the thing it describes, because the list
> and the thing drift and only the list is checked.

### AGONIST brief — Opus (design) → Sonnet (implement)

**Design the declaration so the claim becomes machine-falsifiable.** A `no_floor` check
should declare *what its subject is*, in a form a script can evaluate:

- `empty_kind: corpus` + the tables or query whose emptiness is being asserted
- `empty_kind: changeset` + the path globs it scopes to
- `empty_kind: vocabulary_owed` + the ratchet trigger condition

Then a check verifies: **a `corpus` declaration whose subject is non-empty is RED.**

**Constraints, all of which are §4.1:**

- The subject declaration must be **evaluated**, never compared against a stored count.
  Storing "expected 0" reintroduces the hard-coded number one layer up.
- Do not build a second registry. The declaration lives in `check-registry.yaml` beside the
  check — *"`governance/check-registry.yaml`'s `batteries:` is the one home"* is the
  established pattern.
- **Include a dead-declaration detector**: a declaration naming a table that no longer
  exists must fail, exactly as `retired_vocabulary_audit`'s dead-exemption detector does.
- **Apply §8 before writing it.** *What wrong thing reaches the guidebook?* A gate whose
  metadata says "nothing to examine" while its corpus filled is how a defect class rides
  through unexamined for a month — B3 is that, measured.

### ANTAGONIST brief — Opus

- **Fault injection:** flip a `corpus` check's subject from empty to non-empty on a scratch
  DB. The new audit must go RED. If it does not, it is decoration.
- **The recursion test:** does the new audit itself carry a floor, and is that floor derived?
  An audit that polices hard-coded floors with a hard-coded floor is self-refuting.
- Verify `--selftest` C8's rules (`min_items` XOR `no_floor`, no bare `true`, positive
  integers) still hold with the new field.
- Count how many of the 33 go red on first run. **A first run that reports 0 stale
  declarations, when B3 is known stale, means the audit is not reading what it claims.**

## C2 — seven contract criteria that no check claims (the top-down half)

From `--selftest`:

```
cross_stage/attestation-doctrine-binding      judgment/convergence-independence
evidence/discovery-provenance                 render/register-invariants
judgment/comparator-recorded                  specification/no-diagnosis-only-determination
synthesis/opus-routing
```

One is a **known artefact, already explained** in `medical_lens_integrity`'s entry:
`specification/no-diagnosis-only-determination` *is* enforced — that criterion's own
`check:` field names the script, but `basis:` is singular so the selftest cannot see the
second claim. The entry argues, correctly under §8, that splitting the script in two to
satisfy a one-to-one field *"would be apparatus added for the apparatus's sake."*

**AGONIST (Opus):** for each of the remaining six, decide and record one of:
**(a)** a check exists and the `basis` wiring is wrong — fix the wiring;
**(b)** no check exists and one is warranted — state what wrong thing reaches the guidebook
without it (§8), then write it;
**(c)** the criterion is not currently enforceable — record why, in the contract, so the
next reader does not re-derive it.

**Do not write six checks reflexively.** §8: *"Before adding a check, state what wrong thing
reaches the guidebook if it does not exist. If the answer is about the apparatus rather than
the book, do not add it."* `synthesis/opus-routing` is the one to scrutinise hardest — it
governs who may write `best_practice_synthesis`, which is a real doctrinal floor (§6).

**ANTAGONIST (Opus):** challenge every (b). Challenge every (c) harder — "not enforceable"
is the answer that never expires. Confirm the selftest's count moves by exactly the number
of criteria actually wired.

## C3 — 21 checks with no stated authority

The selftest's instruction is explicit and is itself the guard against the obvious failure:

> ratchet this down, **do not invent authorities**

**AGONIST (Haiku enumerate → Opus attribute):** for each, find the DR, ruling or rule that
actually warrants it. Where none exists, leave `unattributed` and say so. An invented
attribution is worse than an honest blank, because it manufactures a warrant the project
never gave.

**ANTAGONIST (Opus):** spot-check every new attribution against the cited document. One
fabricated citation is §5c, and this repository has a measured history of exactly that.

---

# §10 — Execution order and dependencies

```
                    ┌─────────────────────────────────────────┐
   PHASE A          │ A1 locators ─┐                          │
   (parallel        │ A2 pydantic ─┤  independent, run in     │
    where shown)    │ A3 vocab ────┤  parallel                │
                    │ A7 archive ──┘                          │
                    │                                         │
                    │ A8 protocol ──► informs A2 (rule-5      │
                    │                  column-retire pattern) │
                    │                                         │
                    │ A4 reasoning ──► PRODUCES the subject   │
                    │                  B2 needs               │
                    └──────────────┬──────────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────────┐
   C1 FIRST IF      │ C1 floor ratchet                        │
   B3 IS NOT ALONE  │   └─► B1, B3, B4, B5 all consume it     │
                    └──────────────┬──────────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────────┐
   PHASE B          │ B-SPINE ──► B1, B2, B3, B4, B5          │
                    └──────────────┬──────────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────────┐
   LAST             │ A5, A6  (framing depends on B-SPINE)    │
                    │ C2, C3  (top-down, after registry settles)│
                    └─────────────────────────────────────────┘
```

## §10.1 — SUPERSEDED BY AN INDEPENDENT DERIVATION, 2026-09-16

**This section first reported 9 stale `no_floor` declarations. That figure was WRONG and is
corrected below to 11. The error and its cause are recorded because the cause is the same
defect this brief exists to fix, committed by its own author.**

An independent Opus agent, given the question and the primitives but not the first analysis,
re-derived the answer by running all 33 checks **through `run_checks.py`'s own dispatcher**
(not standalone, which is what the first pass did) and measuring each claimed subject
separately against the database. Three of its key findings were then verified against
primaries before being accepted here.

### FALSIFIED: 11 of 33 — reason asserts an empty subject, the subject is not empty

| Check | Level | Measured |
|---|---|---|
| `extraction_relations_integrity` | **BLOCKING** | `EXAMINED: 18` — its own stated RATCHET trigger has fired and was missed |
| `validate_evidence_state` | **BLOCKING** | `EXAMINED: 2` |
| `source_slug_links_duplicates` | **BLOCKING** | `EXAMINED: 5` |
| `citation_mining_session` | **BLOCKING** | examines **4** — see the instrumentation trap below |
| `citation_mining_backlog_t2` | informational | examines **4** — same trap |
| `research_protocol_audit` | advisory | `EXAMINED: 21`, and currently exits 1 |
| `gap_mining_audit` | advisory | `EXAMINED: 11` |
| `metadata_integrity_audit` | advisory | `EXAMINED: 5` |
| `derivation_handshake_integrity` | advisory | `EXAMINED: 1`; its ratchet has also fired |
| `test_verification_pipeline` | advisory | claims "fixtures, not a corpus" — has a `[G] Live state` section querying the canonical DB |
| `test_directness_2_2` | advisory | same claim; its live leg always runs because `run_checks` always sets `GUIDEBOOK_DB_PATH` |

### WHAT THE FIRST PASS GOT WRONG, AND WHY IT MATTERS

It read the kind off each reason's **prefix** (`empty-by-decision`, `selftest`,
`not-instrumented`, `changeset-scoped`) and treated the prefix as a fact about the check.
**A prefix is a claim, not a fact.** Two of the ten `selftest` claims are false — those checks
do reach live data. The first pass therefore excluded them from scrutiny on the strength of
the very declaration under audit.

**That is this brief's §4.1 defect committed one level up:** a curated label trusted in place
of a derived fact. Any C1 design that verifies `no_floor` reasons by reading their declared
kind inherits the same hole. **The kind must be established from what the check does, not
from what its reason says it does.**

### THE ROOT DEFECT IS LARGER THAN STALE PROSE

**17 of the 33 print no line `run_checks.py` can read.** No `^\s*EXAMINED:\s*<n>` and no
`^\s*VERDICT: NOTHING-IN-SCOPE`. For those, `vacuity_failure` returns `None` and
`nothing_in_scope` returns `False`, so **the runner reports PASS whether or not they examined
anything.** Half the `no_floor` set sits outside the vacuity apparatus entirely.

Two near-misses are one-line fixes and are the place to start:
- `citation_mining_*` print `Examined (slug-linked T1-2 sources in scope): 4` — the
  parenthetical falls between the word and the colon, so the anchor cannot match.
- `research_dod` prints `EXAMINED: 5` **mid-line**, inside `R10b: PASS — EXAMINED: 5 …`, so
  the line-start anchor rejects it.

**C1 cannot detect what the runner cannot read.** Closing this gap is therefore step one, not
a follow-up: a detector built on today's instrumentation would cover 16 of 33 and report the
other 17 as fine.

### FALSIFIED ON CAUSE OR SCOPE, NOT ON COUNT

- **`validate_verification_consistency`** (BLOCKING): `EXAMINED: 0` is honest, but the stated
  cause — "the corpus was emptied by decision" — is false. `specifications` holds 2 rows; the
  zero comes from a **state filter over a non-empty corpus**, which is a different and less
  safe reason to carry no floor.
- **`attestation_presence` / `attestation_schema` / `attestation_verdict`**: all name the
  window as "HEAD~1..HEAD". `scripts/audit/adherence_log_audit.py:73` has read
  `DEFAULT_BASE = "origin/main"` since 2026-09-11 (**verified**). The changeset *kind* holds;
  the named window does not. **B2 of this brief repeats the stale window and is corrected by
  this paragraph.**
- **"79 attestations on disk"** appears in four reasons. Measured: **128**.
- `doctrine_recheck` ("158" ACTIVE decisions; measured 185), `decision_capture` ("49 orphan
  DRs"; measured 51), `research_dod` ("R1 fails NON-COMPLIANT"; now COMPLIANT) each attach a
  volatile figure as self-justification. The structural claims hold; the evidence offered for
  them has rotted.

### TRUE, CONFIRMED

`population_integrity_audit`, `pmp_audit`, `reasoning_doc_citations_audit`,
`medical_lens_integrity` (the only ratchet-bearing reason whose trigger has **not** fired),
`validate_cross_refs`, `pipeline_completeness_fresh`, `attestation_evidence`,
`research_dod_selftest`, and seven `test_*` checks.

**Open caveat, stated rather than papered over:** the four TRUE empty-corpus checks were
confirmed empty *now*. The clause "emptied **by decision**" was not traced to a migration or
DR and remains unverified for all four.

### A TRAP THAT WILL MISLEAD THE NEXT AUDITOR

`gap_mining_audit`'s registry `note` says "EXAMINED prints COUNT(*) FROM gap_mining".
`gap_mining` holds 0 rows; the script actually prints `EXAMINED: 11`, the `gaps` count.
**Verifying via the note yields "0, therefore the reason is true" — the exact opposite of the
measurement.**

### The ratchet value, unchanged

`min_items: 1` in every case. Not a measurement — the boundary between "examined something"
and "examined nothing". Three registry entries already reached this independently.

---

**The one sequencing decision that matters.** B3 proves at least one `no_floor` reason is
stale. **Before fixing B3 by hand, run the C1 staleness probe (§11 T2) across all 33.**
If more than one is stale, C1 must land first and B1/B3/B4/B5 become its output — fixing
them individually would be curating the very list C1 exists to derive. **That is §4.1 rule 1
applied to the programme's own shape.**

**Hard ordering constraints:**

- A4 **before** B2 — B2's live test is A4's attestation.
- B-SPINE **before** A5/A6 — both may be reclassified rather than fixed.
- C1 **before** B1/B3/B4/B5 if the probe shows >1 stale declaration.
- Nothing merges while `--selftest` is not PASS.

---

# §11 — Derivation appendix: regenerate every figure in this brief

**CLAUDE.md rule 7 applies to this document.** Every count above is a hand-written count in
a derived document, and therefore suspect the moment it is written. **Do not trust a single
figure in this brief — regenerate it.** All commands below were executed and verified in
the authoring session.

**Generated: 2026-09-16, against `origin/main` = `be25c89`. Every figure below drifts.**

### T1 — registry shape (§0 baseline, C1, C3)

```bash
python3 -c "
import yaml; d=yaml.safe_load(open('governance/check-registry.yaml')); c=d['checks']
print('active      :',len([x for x in c if x.get('battery') not in ('quarantined','retired')]))
print('min_items   :',len([x for x in c if x.get('min_items')]))
print('no_floor    :',len([x for x in c if x.get('no_floor')]))
print('unattributed:',len([x for x in c if x.get('basis')=='unattributed']))"
```

Verified output: `active 70 · min_items 37 · no_floor 33 · unattributed 21`.
**Note 37 + 33 = 70 — the selftest's C8 floor/no_floor exclusivity holds. If that sum ever
stops equalling `active`, C8 has been broken.**

### T2 — the `no_floor` staleness probe (B1, B3, B4, B5, C1)

**This is the single most important command in the brief.** It is the manual form of what
C1 automates.

```bash
python3 -c "
import sqlite3
con=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
for t in ['gaps','evidence_sources','evidence_population_match','search_languages',
          'spec_value_probes','reasoning_doc_citations','citation_population_links',
          'probe_population_links','extraction_population_links','base_taxonomy_medical',
          'specifications']:
    print(f'  {t:32s}', con.execute(f'select count(*) from \"{t}\"').fetchone()[0])"
```

Verified: `gaps 11 · evidence_sources 5 · evidence_population_match 5 · search_languages 0 ·
spec_value_probes 0 · reasoning_doc_citations 0 · citation_population_links 0 ·
probe_population_links 0 · extraction_population_links 0 · base_taxonomy_medical 0 ·
specifications 2`.

**The table list here is itself hard-coded** — it was read out of the `no_floor` reasons by
hand. **C1's job is to make that list derived from each check's own declaration.** Until C1
lands, this command is a stopgap and must be treated as one.

### T3 — determination state (B1, A6)

```bash
python3 -c "
import sqlite3
con=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print('stated/provisional:',con.execute(\"select count(*) from specifications where state in ('stated','provisional')\").fetchone()[0])
print('live (not retired):',con.execute('select count(*) from specifications where retired_at is null').fetchone()[0])"
```

Verified: `stated/provisional 0 · live 1`.

### T4 — the unwritable set (B4, B5)

Use the derivation in CLAUDE.md §4 verbatim. Verified this session: **21 columns**, including
`spec_value_probes.item_code`, `icf_medical_map.medical_code`, `identity_medical_map.medical_code`,
`item_taxonomy_links.item_code`. **`specifications` is NOT in the set** — see §12.

### T5 — per-check evidence

```bash
python3 scripts/audit/source_locators_integrity.py          # A1: 550/48/31/17
python3 scripts/audit/validate_pydantic_schemas.py --strict # A2: 68 models, 20 mapped
python3 scripts/audit/retired_vocabulary_audit.py           # A3: 62 occurrences
python3 scripts/validate_reasoning.py --strict              # A4: 1 doc, 15 errors
python3 scripts/tests/test_verification_pipeline.py         # A5: 15/18, G01-G03 red
python3 scripts/generate/build_site.py --check              # A6: 0 pages
python3 scripts/validate_schema.py --cross-check            # A7: 83 archived / 84 live
python3 scripts/audit/research_protocol_audit.py            # A8: CHECK 8, REF-00987
```

### T6 — corpus scale (A4, A5 premises)

```bash
python3 -c "
import sqlite3
con=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print('slugs        :',con.execute('select count(*) from slugs').fetchone()[0])
print('slugs searched:',con.execute('select count(distinct slug) from search_executions').fetchone()[0])
for t,c in [('source_slug_links','slug'),('source_value_extractions','slug')]:
    print(f'{t} on room-acoustic:',con.execute(f\"select count(*) from {t} where {c}='room-acoustic-performance'\").fetchone()[0])"
```

Verified: `slugs 106 · searched 2 · room-acoustic links 0 · room-acoustic extractions 0`.
**A4's entire premise rests on the last two being 0. Re-verify before acting on A4.**

---

# §12 — Findings outside the check battery

Three things no check reports, surfaced during derivation. **They are not Phase A or B
items; they are reported because an executing agent will otherwise trip on them.**

1. **CLAUDE.md §4 is factually wrong about `specifications`.** It states the table is
   unwritable because `parameter_id NOT NULL` reaches into an empty `base_parameters`, and
   that *"no determination can be written until a parameter is minted"*. **`base_parameters`
   holds 1 row; `specifications` holds 2; `specifications` is absent from the derived
   unwritable set.** Layer 0 breaking its own rule 7. **This is an owner-facing edit under
   rule 0 — flag it, do not silently patch doctrine.**

2. **The `no_floor` prose class is unmaintained by construction** (C1). B3 is the measured
   instance; the probe will say how many others.

3. **`run_checks.py`'s vacuity escalation cries wolf** (B-SPINE). Two of the three
   "BLOCKING and vacuous" checks are changeset-scoped and will report vacuous on most
   commits forever.

---

# §13 — Definition of done

**Per item:**

- [ ] AGONIST REPORT complete, including the three-part HANDSHAKE sentence (§1)
- [ ] ANTAGONIST VERDICT recorded, with a **fault injection actually attempted**
- [ ] `EXAMINED` did not silently fall
- [ ] No literal introduced that fails §4.1's test
- [ ] `python3 scripts/run_checks.py --selftest` → PASS
- [ ] `python3 scripts/run_checks.py --changed-from origin/main --explain` → no new failure
- [ ] Any DB change went through `emit_data_migration.py` → `migrate_db.py`, and
      `migrate_db.py --rebuild /tmp/rebuilt.db` reproduces
- [ ] Attestation present where rule 2 requires one
- [ ] Commit follows rule 1's format

**Per phase:**

- [ ] `--all` re-run; the advisory-failure and nothing-in-scope counts **explained, not just
      reduced** — a count that fell because a check stopped examining is a regression
- [ ] `research_batch_dod.py --session <latest>` still COMPLIANT
- [ ] Every deletion recorded in its commit with the evidence §8 requires

**Programme:**

- [ ] `no_floor` declarations are derived and self-policing (C1)
- [ ] Contract criteria are wired, or their non-enforcement is recorded (C2)
- [ ] No curated list was replaced by a fresher curated list anywhere in the diff

---

## §14 — The standing refusals

Say **no** and escalate rather than proceed, if any item would require:

- writing `data/guidebook.db` outside a migration;
- editing a frozen record in `sessions/`, `audits/`, `versions/`, `_archived/` or
  `scratchpad/` to make a check pass;
- skipping, disabling, quarantining or loosening a check to reach green;
- backfilling a field whose value would be a **reconstruction** rather than a record
  (CHECK 7's standard, A8);
- copying a DOI embedded in a title into that row's `doi` column (A1);
- creating placeholder render output to satisfy a floor (A6);
- pinning a threshold to today's measurement (A5, §4.1 rule 3);
- editing CLAUDE.md doctrine without an owner ruling (rule 0, §12 item 1).

**Rule 0 governs all of it: a live owner statement supersedes every prior ratified record it
touches, on contact. An agent's reading of a document is not an owner statement, and neither
is this brief.**
