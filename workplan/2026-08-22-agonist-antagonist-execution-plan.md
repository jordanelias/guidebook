# Execution plan — 2026-08-22: the first answered question, and the owner decision that unblocks it

**Author.** Opus 5, from a Fable 5 read-only review of `session_2026-08-20-provenance-walk`, its
attestation, `governance/pipeline-map.yaml`, the cull plans, and
`decisions/DR-2026-08-19-research-restart-operative-instrument.md`.
**Form.** DR-2026-08-19 §7 — agonist / antagonist, blind-then-compare, lenses L1–L8, no third judge.
**Status of this file.** An execution plan, not doctrine. It expires when §6's acceptance test is
met or fails. It proposes **no successor document**, and §7 makes that checkable.

> **This plan's own governing verdict.** The reason to write it is not that the last session was
> wrong. It was unusually honest, its SQL-derived claims held **exactly** under a fourth adversarial
> pass, and its refusal of the A-18 × AUT cell was correct. The reason to write it is that its
> **ordered handoff is wrong at act 1 and wrong at act 2**, that a fix it schedules would revert
> ratified doctrine, and that the thing actually blocking the project's acceptance criterion is an
> **owner decision nobody has been asked for**.

---

## 0. What binds, and the four rules that actually stop you

`CLAUDE.md` §0 rules 1–4 (commit format · attestation on synthesis paths · migrations only ·
sweep the callers). `DR-2026-08-19` is the operative instrument. `references/project-standards.md`
is the live rule ledger. Where the session record and the instrument disagree, **the instrument
wins** (CLAUDE.md, lines 9–12) — and §1.1 below is the first place they disagree.

**Read before acting:** the DR (operative), then this file. The pipeline map is a **reference**, not
a read-first document — DR §8 caps the read set at four, and the handoff's instruction to read the
map second breaches that cap (§1.9).

---

## 1. FINDINGS — conflicts, gaps, misses, and poor reads

Every finding below was re-derived against the live repository. Where a claim came from a grep hit
count, it was re-derived by reading the call site; that distinction is doing real work — **every
SQL-derived claim in the last session held exactly, and the claims that failed were all
grep-shaped**, which is the same pattern the session itself recorded and then, in one place,
repeated.

### F-1 — CONFLICT, decisive. The instrument's next act and the handoff's next act are opposites, and both are wrong

- DR §3 step 4 reads *"**Run the first research batch** … **← THIS IS THE NEXT ACT.**"* Step 4 is
  **done** (`evidence_sources` 5, `search_executions` 9). The DR was never amended, so its literal
  next act is now **step 5, "Render the determination and read it."**
- The session record §7 reads *"**Do not** author a determination as the next act"*, and orders
  **BRK-26 first**.

An agent obeying CLAUDE.md obeys the instrument — and the instrument, followed literally today,
commands authoring the cell that BRK-20 proved **has no lawful applicability edge at all**. The halt
was recorded only on `sessions/**`, a non-binding surface; the DR's own amendment mechanism was not
used. **This is the single most dangerous state in the repository right now.**

**Resolution (§3 act 0):** amend the DR in place — one paragraph, §3 step 4 struck as DONE, step 5
re-scoped to *"render a determination for a cell chosen applicability-edge-first"*. That is a
correction to an existing document, which the freeze clause explicitly permits.

### F-2 — POOR READ, and a near-miss. "Do BRK-25 in the same pass" would revert ratified doctrine

The handoff's act 1 says fix BRK-26 and *"do BRK-25 in the same pass or record why not."*

BRK-25 says `v_best_practice` never filters on `regulatory_stratum_only` and so a T4–T6-only cell
*"surfaces as best practice annotated rather than excluded"*, quoting CLAUDE.md §6's *"walled off"*.

The live DDL is:

```sql
CREATE VIEW v_best_practice AS
    SELECT *, CASE WHEN regulatory_stratum_only = 1 THEN 'weak' ELSE 'anchored' END AS strength_band
    FROM "specifications" WHERE state IN ('stated','provisional') AND code_floor_only = 0
```

`_archived/scripts/migrations/029_best_practice_weak_band.sql` produced it verbatim and says why:

> *"under DR-2026-07-21-product-posture-thinking-tool-not-authority (RATIFIED): a determination whose
> entire evidence basis is the regulatory stratum … **IS** a best-practice determination at the WEAK
> band … The engine contradicted this: migration 027's `v_best_practice` EXCLUDED those rows
> outright. **This migration reconciles the engine with the ratified doctrine.**"*

CLAUDE.md's wall is *"walled off from **full-strength anchoring**"* — which `strength_band` is.
BRK-25 truncates the doctrine at "walled off", never cites the DR that adjudicated this exact
question, and rates the result `severity: high`.

**BRK-25 is REFUTED as a break.** Its DDL observation is correct; its doctrinal reading is not.
BRK-25 and BRK-26 also pull in opposite directions — BRK-25 faults the live view for *not*
excluding those rows, BRK-26 faults `assess_cell.py` for shipping DDL that *does*. Both cannot be
regressions. **Do not "fix" BRK-25. Amend the entry.**

### F-3 — SUSTAINED with corrections. BRK-26 is real; its guard line is refuted; and it does not block the next act

Verified line by line at `scripts/assess/assess_cell.py:590–604` (the map says 590–599, off by
five, in two places): the engine DROPs and re-CREATEs `v_best_practice` inside the determination
write, appends the DDL to the emitted replayable SQL, and its comment claims the definition is
interim *"until migration 027 adds a real `regulatory_stratum_only` column"* — a column that exists
today. Applying it drops `strength_band` and reverts to the superseded 027 marker semantics.
The stale DDL has demonstrably travelled before: `working/pilot/data_20260712_pilot-cell-backfill.sql:23–24`.

Two corrections to the entry:
- Its `guard:` line says `migration_reproducibility.py` *"compare[s] ROWS, so a view redefinition is
  invisible to them by their own admission."* **Refuted.** `deep_compare` compares view/trigger/index
  **DDL** (lines 311–315), and line 221 is the *rationale for doing so*. There is even a selftest
  constructing two DBs that differ only in a view's WHERE clause. The real residual gap is narrower:
  a stale DDL that travels *inside a migration* changes both sides consistently and passes.
- "older, weaker form" is imprecise — the in-code form is *more* exclusionary, and weaker only as
  apparatus.

**And the handoff's premise for putting it first is false.** BRK-26 is *not* "a defect in the write
path you are about to use": the write path for a determination is **hand SQL** (DR §12.5 makes
`specifications` permanently manual), and `assess_cell.py` cannot address the cell anyway — see F-4.

### F-4 — MISS, structural. There is no engine that can author the next determination

`scripts/assess/assess_cell.py` is the **pilot** engine. It carries a hardcoded seven-cell list
(`PILOT_CELLS`, line 113) — E-08×DEAF, E-12×MOB, G-03×MOB, C-02×DEM, E-06×MOB, G-03×SCI, B-10×NEU —
**none on `room-acoustic-performance`, none for AUT or NDV**. Its CLI takes `--db --emit-sql
--report-json`; there is no `--item`/`--population`. It refuses the canonical DB by design. It
stamps every row it writes with `SESSION = "session_2026-07-12-evidence-architecture-pilot"` and
`STAMP = "2026-07-12 00:00:00"` — so any row it emitted today would carry **false provenance**, which
is the exact defect class D-2 and the provenance walk exist to close. Its docstring names a module
for `source_value_extraction`; the live table is `source_value_extractions` (0 rows) and the
singular does not exist.

The **renderer** generalises — `scripts/generate/spec_page.py` and `pilot_renderings.py` read
`FROM specifications` for all rows — so the acceptance criterion is reachable. The **engine** does not.
Consequence: the next determination is authored by hand SQL, adversarially reviewed, and rendered.
No engine work is on the critical path, and none should be started.

### F-5 — MISS, and this is the real blocker. Every applicability edge in the repository is unwarranted

BRK-20 is correct that A-18 has **zero** `item_population_links` and is the only item on its slug
without them (verified: the other twelve hold 42). But the inference — *choose a different item and
you get a lawful edge* — does not hold:

```
item_population_links                 372 rows
  ... with a non-null rationale_ref     0
  applicability: applies 366 / context_dependent 6
  created_by: session_2026-05-11-items-population-normalization 358, +14 others
```

**Not one of the 372 edges cites evidence.** They are the same class of unwarranted assertion as
the axis map D-1 quarantines; A-18 differs by having *none* rather than *unexamined ones*. So
BRK-20 is half-right: choosing a different item does not buy a lawful edge, it buys an
**unexamined** one, and the determination inherits it silently.

This is the fork in the road, and it is **owner-gated** (population applicability is DG-NON):
either applicability edges are scaffolding — in which case D-1 quarantines all 372 and **no cell is
determinable anywhere** — or they are substrate, in which case A-18 is entitled to its edges and the
question is which populations they name. §2 puts this to the owner as OD-A.

### F-6 — MISS, first-order, and nobody has named it. Deaf and hard-of-hearing people are absent from the acoustics slug

`populations` holds `DEAF`; it carries **16** `item_population_links` — to `A-10`, `A-11`, `A-12`
(assistive-listening-systems), `E-08`, and eleven others. **Zero of them are on
`room-acoustic-performance`.** The thirteen items of the reverberation slug are linked to
ALL/AUT/BRAIN/COM/DEM/MH/MOB/NDV/PAIN/SCI and to no hearing population at all.

Meanwhile the project's own reasoning document names DEAF as the **only** population on this
parameter with a Tier-1-anchored numeric value, and the two Tier-1 sources for it
(Iglehart 2016 `REF-00578`, Iglehart 2020 `REF-00325`) are held in `source_locators` today.

A guidebook centred on disabled people whose room-acoustics chapter does not apply to deaf and
hard-of-hearing people is a content defect, not a schema defect. It is DG-NON. **OD-B in §2.**

### F-7 — MISS, the largest. The question was already answered in May 2026, in prose, and destroyed by the reset

`references/bpc-reasoning/room-acoustic-performance.md` (41 KB, authored 2026-05-15/18,
**owner-signed-off inline**, five sign-off items) contains a complete worked determination for A-18:

| Population | Value | Basis as recorded |
|---|---|---|
| DEAF | **RT60 ≤ 0.3 s** (≤ 283 m³) | Iglehart 2020 (REF-00325) T1; ANSI/ASA S12.60 Footnote e; PMP walk PMP-A18-001 strict-termination PASSED |
| NDV/AUT | **≤ 0.4 s**, explicitly labelled *conjecture rationally informed by literature* | lower bound of Bettarello 2021 (REF-00561, T3, 0.4–0.7 s); Marzi 2025 corroborates the **absence** of a T1 threshold |
| DEM | **≤ 0.5 s** | T2–T3 bundles only; self-described as *"the thinnest evidence base of the four"* |
| general | **≤ 0.6 s** | cross-jurisdictional convergence |

plus a **16-jurisdiction comparison table** with a comparator-type column, per-population worst-case
users, step-7 rationales, step-8 trade-offs, and a step-9 cross-population conflict flag
(convergent, no arbitration needed).

The 2026-08-06 clean-room reset removed every `evidence_sources` row it cites, orphaning all 11
citations. The 2026-08-19 batch then re-searched the question as though the slug were unexplored,
and the OD-5 witnesses (REF-00561, REF-00578) are two of those 11 orphans. **This is D-2
demonstrated, not argued:** reasoning held in prose was invisible to the pipeline and to the
researchers.

Two things follow, and they cut against each other:
- The doc is **Pass-1** and says so: *"Citation-grade verification of this table is PENDING."*
  Its values are **hypotheses** under R15, and its PMP claim has no surviving DB record
  (`items.pmp_*` all NULL for A-18; `spec_value_probes` 0 rows). Nothing may be copied from it.
- It is nevertheless the **strongest lead set in the repository**, already owner-reviewed, and it
  makes the shape of the answer knowable in advance — which is exactly why the falsification design
  must be fixed *before* it is used (§4, agonist protocol).

### F-8 — CONFLICT, live trap. The runbook instructs the write that failed the last session

DR §12.1 **Step 10** reads *"Code values → `jurisdictional_values` (5 cleared rows on A-04 await
backfill)."* The owner's 2026-08-12 REFERENCE-ONLY ruling forbids the table holding values at all;
the 2026-08-21 session wrote 12 such rows, was caught by blocking `test_db_integrity` L02 (109 YAML
vs 121 table), and shipped a compensating retraction. Live: 109 rows, `value_text`/`value_numeric`/
`unit`/`is_code_minimum`/`spec_id`/`source_section` **0 non-null of 109**.

The runbook still says to do it. **Strike Step 10's `jurisdictional_values` clause.** And note the
lesson the digestion session recorded, which generalises: *a table emptied by ruling looks identical
to a table empty for want of data*, and the only record of the ruling was a comment in a YAML header.

### F-9 — CONFLICT. The read-set cap, and this review's own standing

- DR §8: *"A fresh session reads exactly four … **No fifth document may join this set.** That is the
  termination property, not a preference."* The handoff instructs reading `governance/pipeline-map.yaml`
  **second**, ahead of the session record. That is a fifth and sixth document.
- `references/project-standards.md` (RULE, 2026-08-19, owner directive): an adversarial pass *"may
  be commissioned ONLY against a diff that (a) wrote rows to the research tables … or (b) authored or
  amended a synthesis artifact. **Plans, critiques, censuses, handoffs, registers, session records,
  Decision Records and this ledger are not adversarial-pass subjects**"*; *"at most one adversarial
  pass per research batch. **A pass on a pass is forbidden**"*; and a pass *"may not create or modify
  a workplan."*

Measured against that rule, the provenance-walk session ran **three** passes on a census
(`pipeline-map.yaml`), the third of which corrected the first two — a pass on a pass — and emitted
workplan files. **And so does this review**: its subjects are a session record, provenance
documentation, cull plans and a plan, and its output is a workplan file. It was commissioned by the
owner, which is how the rule itself was made; but the waiver belongs in the record rather than in
silence. **Recorded here as a deviation, not argued away.** §3 act 0 asks the owner to ratify or
refuse it.

### F-10 — POOR READ. `unclassified_paths:` understates the condition by 3×, and names a file that does not exist

The map lists eight unclassified entries. Re-derived by importing `run_checks.classify()` and running
it over all 2,171 tracked paths:

```
unclassified: 1229 of 2171 (57%)
  _archived/ 610 · references/ 341 · workplan/ 106 · skills/ 61 · working/ 39
  audits/ 32 · retrieval-log/ 24 · scratchpad/ 8 · versions/ 3 · CLAUDE.md, .ignore, …
```

`README.md`, which the block lists, **is not in the repository**. Omitted entirely: `_archived/**`
(the largest group), ~240 further `references/**` files, `versions/**`, `scratchpad/**`.
The "eight odd corners" framing becomes "most of the repo selects no kind-scoped battery" — including
`references/tooling-register.md`, a governance-grade register, and `references/standards-registry.md`,
which is the subject of a **blocking** check yet classifies to nothing.

**This is the mechanical form of the D-1…D-5 problem** the attestation flags: `workplan/**` matches no
work kind, so the five standing owner directives live on a surface no substantive check examines.

### F-11 — POOR READ. `steps_that_are_hand_sql: [4, 5, 8, 10]` omits the step where the R10 gate is armed

All four are genuinely hand-SQL. But DR §12.1 **Step 7** is CLI **plus a mandatory companion
UPDATE** — the runbook bolds *"Without `doi_resolution_outcome='RESOLVED'`, every VERIFIED DOI-bearing
source fails R10"* — and then a three-statement hand transaction over `search_executions`,
`search_admissions` and `search_candidates`. A sequencer reading `steps_with_coded_cli: [3, 9]`
models Step 7 as coded. It is not, and its hand half is exactly where the last batch's H03/H04/H05
parity risk lives.

### F-12 — POOR READ, inside the paragraph about epistemic hygiene

Map, lines 46–47: *"NOTHING READS THIS FILE. Repo-wide grep for 'pipeline-map' outside the file
itself returns nothing."* Four files contain it: the attestation (as an `evidence_path`), the
execution plan (×2), the session record (×2), and the command log. `readers_today: 0` survives —
none is a code reader — but the evidentiary sentence is a false grep result in the paragraph whose
purpose is to model grep discipline. Same defect class the file's own `views:` correction confesses.

### F-13 — POOR READ, stale internal cross-reference. BRK-24 still carries the pre-correction number

BRK-24 says *"17 exist; **11** have zero code readers (see `views:` above)"* and the islands note
points at a `with_zero_code_readers` list. The corrected `views:` block says **zero of 17** are
queried and contains no such list. The correction was not propagated. A reader landing on BRK-24
gets the refuted count — in the file that stakes its authority on recording its own corrections.

*(The "zero of 17 views queried by any code" claim itself is **SUSTAINED** under a full per-view
sweep that included the `.ignore`-hidden trees: no `FROM`/`JOIN <view>` exists in any `.py`, `.sh`,
`.js`, `.html` or `.yaml`, current or archived. Every semantic distinction the views carry — weak
band, code-floor wall, coverage priority — is dead read-surface.)*

### F-14 — WRONG. The attestation's `doctrine_sha`, and the reason built on it

The attestation carries `"doctrine_sha": "8366c28"` and declines a reattestation entry because
*"the doctrine SHA moved to 8366c28 since the last session attested at 0f2f525."*

```
git rev-parse HEAD:governance/mission-and-epistemics.md      -> 0f2f525…
git rev-parse 5579696:governance/mission-and-epistemics.md   -> 0f2f525…
governance/context-map.yaml:109                              -> doctrine_sha: 0f2f525
git log --oneline -1 8366c28  -> Merge pull request #71 … evidence-base-population  (2026-07-25)
```

**The doctrine did not move.** `8366c28` is a merge commit from a month earlier, not a doctrine blob;
all sibling attestations carry `0f2f525`, and this is the only one of ~80 that does not. The stated
reason for omitting a reattestation entry rests on a false premise, and any future materiality audit
keyed on this file anchors to an unrelated commit. **Correct it by amendment, and say why.**

### F-15 — WRONG, and it matters for what gets deleted

Session record §7 act 4: *"`REF-00968.pages` holds an article number **no payload asserts**."*
The held Crossref payload `81980e4f0b1ae87e.json` asserts `"article-number": "2645738"` (its `page`
field is null). The value is supported — **filed in the wrong column**. The correct repair is a field
move, not a deletion, and `REF-00607` and `REF-00967` carry the same defect, so REF-00968 is not
special. A session following the record's letter deletes a true value.

The surrounding claim is confirmed: `volume`, `issue`, `pages_start`, `pages_end`, `article_number`,
`issn` are NULL on **all five** rows while the payloads supply them, and all five are stamped
`metadata_quality='COMPLETE'`, which is false as stored.

### F-16 — CORRECTION to a review finding. `corporate_name_note` exists

One reviewer reported that handoff act 5 targets a nonexistent column. It does exist — on
`evidence_source_authors`, not `evidence_sources`, exactly as the adjudication §5 states. Verified:
column present, NULL on all 23 author rows; REF-00966 position 3 is `andsensory, Emily`.

But the write is weaker than it looks. **`corporate_name_note` has zero readers in any script.**
Nothing mechanical would stop the next agent from "tidying" the surname away — which already happened
once, on the paper whose entire Co-1 warrant is its autistic community co-authorship. And
`is_corporate = 0` on that row, so a chosen-name note in a column named for corporate names is a
repurposing the next reader will read as a defect. §3 act 3 handles both halves.

### F-17 — GAP, unclosed. Everything the adjudication referred to the owner is still open

Verified live, all still true: `co1_source_type` and `co1_provenance` **NULL on all three** Co-1 rows
(and on all five); the Co-1 → T3 re-grade of REF-00965/REF-00968 unresolved; REF-00967 still T1 on an
n=27 EEG study whose own note concedes it *"contains no RT60, NRC, STC or NC value"*; Greenland 2026's
figures still `[UNVERIFIED-QUANT]` and unretrieved; Mealings 2025 unverified; Rosas-Pérez 2023
unadmitted; the L5 setting-objection gap unrecorded in any row; `search_executions` still 9.
**If the re-grade is sustained, `tier_basis='Co-1'` on this slug rests on one source, not three.**

### F-18 — GAP. The three anti-recursion guards that ever had code have all expired, and one gate re-reds on first use

- `meta_work_freeze` — the only mechanical brake on new plans and new checks — **self-expired and was
  retired** the day it was ratified, at `evidence_sources ≥ 1`. DR §11 property 3 now reads
  *"A successor plan is no longer build-rejected."* Nothing prevents a fifth plan. This one included.
- §1.4's six-rule items quarantine, §2.2's four remaining freeze clauses, §6's two triggers and the
  `source_locators_floor` check, §7's `adversarial_findings` table, §8's four-document cap, §11's
  property-5 test: **convention only**. The DB holds **zero triggers**; `source_locators` appears
  nowhere in `check-registry.yaml`; `slugs.status='PROVISIONAL'` is used by 0 rows.
- **R9 verified in code by direct read**, not by grep: `research_batch_dod.py:432–437` selects from
  `evidence_sources` twice and never touches `source_locators`. OD-5's premise is confirmed; the cost
  has now been paid twice (REF-00578, REF-00561).
- `scripts/research/retrieval_log.py:95,100` still hardcode `.json` for every artefact regardless of
  content type. The B5-f defect was repaired **in data only** (seven artefacts hand-renamed). The
  blocking `check_json` gate passes today and **turns red on the next full-text fetch** — which is the
  first thing act 2 does. Fix it before the fetch, not after (§3 act 1).

### F-19 — GAP, provenance. The command log records the question and throws the answer away

Of 356 committed lines in `scratchpad/session_2026-08-20-provenance-walk/commands.jsonl`, **one** has a
non-null `exit` and **one** a non-null `is_error`, and both are synthetic probes: the harness's
PostToolUse payload carries `stdout` but neither key, so `tr.get("exit_code")` and `tr.get("is_error")`
return `None` on every real event. 886,787 bytes of stdout were hashed and discarded — the bodies are
stored nowhere, so the digests are checkable against nothing that outlives the container. stderr is
never read. The matcher is `Bash` only, so every Read/Edit/Write/Grep/MCP call is invisible — including
the hand-edit of a generated file, one of the five errors the apparatus exists to make reconstructable.
Since `e387888` any command containing the substring `git commit` or `git push` is dropped whole, so the
session's own closing commits are absent from its own provenance log.

Two further live traps:
- **`.claude/session` is stale.** It still reads `session_2026-08-20-provenance-walk`, so the
  2026-08-21 digestion session's commands — and this review's — were filed under the previous
  session. The per-session log is not per-session.
- **The livelock fix is reverted right now.** `/root/.claude/stop-hook-git-check.sh` (mtime
  2026-08-22 00:43, freshly provisioned) contains no exclusion; `grep -c scratchpad` returns 0. Any
  session that runs one command dirties a tracked file it may not always commit. The durable fix
  belongs in the **owner's own** `~/.claude/stop-hook-git-check.sh`, scoping both checks:
  `git diff --quiet -- ':(exclude)scratchpad/*/commands.jsonl'` and
  `git ls-files --others --exclude-standard -- ':!scratchpad'`.
  **And note the tension nobody has recorded:** that same dirty-tree complaint is the *only* thing that
  currently prompts anyone to commit the log. Install the exclusion naively and "the scratchpad is
  saved always" silently becomes "saved when an agent remembers".

### F-20 — GAP. No gate reads an attestation for meaning, and the code confirms it

`scripts/audit/adherence_log_audit.py`: check 0 presence (blocking), check 1 jsonschema shape
(blocking — minimum *string lengths*), check 3 rule ids resolve (advisory), check 4 `evidence_path`
**exists as a file** (advisory — never that it evidences anything), check 5 a DB cross-reference for
exactly **three** rules (advisory), check 6 `SequenceMatcher > 0.85` against the last ten
attestations (catches copy-paste, not fabrication), check 8 verdict arithmetic — and
`NON-COMPLIANT` *"is logged but does NOT exit non-zero"*.

An attestation with every rule `FIRED`, fresh prose, and `evidence_path` pointing at any real file
passes everything. CLAUDE.md §0 already says the gate reads no meaning; the code confirms it. The
practical instruction: **do not treat a CLEAN verdict anywhere in `attestations/` as machine-verified.**
The only machine-verifiable provenance in this repository is the retrieval log and git.

### F-21 — MISS. CLAUDE.md broke its own rule 4 when it was rewritten

CLAUDE.md now runs §0–§8. At least 28 non-archived references still point at **CLAUDE.md §9 and §10**,
including three in `governance/check-registry.yaml`, six in `governance/retired-vocabulary.yaml`, four
in `skills/*_SKILL.md` (loaded by sessions), and `references/synonym-chart.md`,
`references/tooling-register.md`, `references/connection-register.md`, `.ignore` itself.

Rule §0.4: *"A rename or removal is not done until the callers are swept."* The rewrite that made that
rule the fourth thing that stops you did not sweep its own callers. Cheap to fix, and it is the kind of
thing that is cited as authority long after it stopped existing.

### F-22 — Smaller record defects, folded in for the sweep

| # | Defect | Actual |
|---|---|---|
| a | Attestation: *"added a 400-line governance document"* | `pipeline-map.yaml` was **791** lines at that same commit |
| b | Attestation: *"Thirty-one commits"* | 32 in PR #111, 33 on the branch |
| c | Attestation deviation 1 cites *"the plan's own section 9"* as forbidding the sha move | §9's eight forbids contain no such clause; §4.5 explicitly permits movement via `migrate_db.py` |
| d | Workplan §2c heading: *"three standing rules"* | the section records five (D-1…D-5, plus D-2a) |
| e | Advisory-failure count | workplan §2b says two, record and attestation say three |
| f | *"preflight PASS, 50 green, 9 nothing-in-scope, 3 advisory"* | **unverifiable** — diff-scope-dependent. Only `63 checks / 4 quarantined` is reproducible, and both were confirmed exactly, with **zero dangling registry entries** |
| g | Both 2026-08-21 migrations are stamped `applied_by_session='session_2026-08-21-reasoning-doc-digestion'` | true, but a naive query for the provenance-walk session's writes returns zero |

### F-23 — The cull: real, but its keep-list contains a false claim and its plan is ~85% unexecuted

The cull was genuine and is the first inversion of this repository's ratchet: `af73005` + `80a34d1`
deleted **23 files / 6,716 LOC** and **15 registry entries**; registry 66 → 63 active, quarantine
16 → 4; and — verified independently — **every registry `cmd` path resolves, and of 17 ever-deregistered
ids, 16 have their scripts deleted**. The named failure mode ("deregister and leave the code") is
clean at the registry level. Every code deletion is covered by a named plan row.

Three qualifications:

**(a) One of the four "kept on evidence" claims is false.** The commit kept
`scripts/audit/adjudication_integrity.py` (178 LOC) because *"its wrapper `test_adjudication_integrity`
is a LIVE registered check."* It is not. `test_adjudication_integrity` appears in
`check-registry.yaml` exactly once — at line 1434, **inside the prose of another entry's quarantine
`reason:`**. The wrapper `scripts/tests/test_adjudication_integrity.py` (42 LOC) is invoked by nothing:
not the registry, not a workflow, not `preflight.sh`, no import, no subprocess. The parent is a
*quarantine* entry, which `run_checks.py` never selects. **220 LOC kept on a claim that was false when
made** — and `workplan/2026-08-11-remediation-and-pipeline-anatomy.md` had already recorded the wrapper
as UNREGISTERED. Its quarantine reason ("RED — 274 tier inconsistencies") was measured false on
2026-08-18 (PASS, 0) and never corrected. The other three keeps hold, with one half-truth:
`generate_parts.py` was correctly not culled, but §15.3 said *"must be **registered**, never culled"* —
and it still has no registry entry, no workflow, and no freshness gate, while CLAUDE.md §7 forbids
hand-editing the `parts/` it produces.

**(b) The live figures, re-derived.** `scripts/` 87 files / 25,717 LOC (`.py`+`.sh`) + `tools/` 3,196 =
**~29.3k executable LOC**, down ~6k net from the 35,444 CLAUDE.md §1 quotes, and not at §15.3's ~21,000
target. Classified by path, **~72% is apparatus policing the repo, ~28% produces the book** — the cull
removed dead weight from both sides, so the *ratio* did not improve. `scripts/migrations/` is a further
7,988 lines of SQL. **CLAUDE.md §1's "~35k" is now stale and should be replaced with a derivation, not
a number** — it is a §2(b) hardcoded volatile fact in the file that forbids them.

**(c) Roughly 85% of the cull plan never ran**, including the part that has now been scheduled and
skipped **three times**: Phase 0's record corrections. `check-registry.yaml:253` still says
`test_db_integrity` is *"RED on main (63/69 checks pass as of 2026-08-04)"*; it measured 72/72 on
08-18. Three quarantine reasons still assert RED states measured false. Also outstanding: 32,733 lines
of dead `references/` indexes; the rooms stratum (2,363 lines) whose generator crashes on a missing
table and which `build_site.py` explicitly disclaims; 7 DEMOTE/SUSPEND decisions; 5 registry merges;
and D7's blocking `PRAGMA foreign_key_check` gate — so **nothing blocking observes referential
integrity** today.

### F-24 — Dead data surface, measured

Zero code readers **and** zero code writers: `source_locators` (**835 rows** — the ratified recovery
stash that nothing can detect corruption in), `access_need_icf` (43), `access_duration` (3),
`access_stakes` (3), `life_stage_modifiers` (2); views `v_coverage_priority` (**7,209 rows**),
`v_source_admission` (5), `v_source_reach_all` (5); eight empty unread tables (`room_items`,
`situations`, `case_study_populations`, `case_study_specs`, `case_study_strategies`,
`economics_entry_populations`, `economics_entry_specs`, `external_root_registry`); eight further empty
unread views. 33 of 66 tables are empty.

---

## 2. THE OWNER DECISION BATCH — one sitting, and it is the actual blocker

Nothing in §3 acts 4–6 can be completed without these. They are DG-NON: population applicability,
work-product inclusion, and evidence-tier definitions.

| # | Question | What it unblocks | Recommendation |
|---|---|---|---|
| **OD-A** | **Are `item_population_links` substrate or scaffolding?** All 372 carry `rationale_ref` NULL; 358 came from one 2026-05-11 normalisation session. If scaffolding, D-1 quarantines them and **no cell is determinable anywhere**. If substrate, A-18's absence is a *gap to fill*, not a prohibition. | Every determination, forever. This is F-5. | **Substrate, provisionally** — with a standing requirement that any edge a determination *relies on* is re-derived and given a `rationale_ref` in that determination's own migration. That converts 372 silent assertions into a debt that is paid where it is used, rather than all at once or never. |
| **OD-B** | **Do deaf and hard-of-hearing people belong on `room-acoustic-performance`?** `DEAF` holds 16 links, none on this slug. The parameter's only Tier-1-anchored value is theirs. | Act 4, and the credibility of the acoustics chapter. This is F-6. | **Yes.** Reverberation is the paradigm access barrier for hearing-aid and cochlear-implant users; the reasoning doc's own step 2 names them the worst-case user. Recommend adding `DEAF` (and considering `COM`) to A-18 and A-03/A-06/A-07 with `rationale_ref` per OD-A. |
| **OD-C** | **A-18's applicability set.** Which populations does *"RT60 in Occupied Learning and Listening Spaces"* apply to? The reasoning doc answers four: DEAF, NDV/AUT, DEM, general. | Act 4. Without it, A-18 stays undeterminable and its 12 staged standards leads have no home. | **DEAF, AUT, NDV, DEM** — mirroring the doc, minus `general` (which is not a disability population and would re-introduce the umbrella problem CLAUDE.md §6 forbids). |
| **OD-D** | **Tier re-grade: REF-00965 and REF-00968, Co-1 → T3?** No co-production warrant is visible in the retrieved record; `co1_source_type`/`co1_provenance` NULL on all three. Only REF-00966 states participatory method and carries autistic community co-authors. | Any cell on this slug. If sustained, `tier_basis='Co-1'` rests on **one** source. | **Referred, not recommended** — it needs the full texts, which this environment cannot reach. But **rule now** that a Co-1 tier with `co1_provenance` NULL is *unwarranted-pending*, which is a mechanical statement a check can enforce. |
| **OD-E** | **REF-00967: T1 → T3?** n=27 single-centre EEG whose own DB note concedes it carries no RT60/NRC/STC/NC value. | Convergence counting on this slug. | **Re-grade to T3.** The antagonist's reading is the defensible one and needs no full text to sustain. |
| **OD-F** | **Ratify or refuse the waiver** that let this review — an adversarial pass whose subjects are a session record, a census and plans — run at all, against `references/project-standards.md`'s standing rule. | The integrity of that rule. See F-9. | **Ratify once, narrowly**, as an owner-commissioned review, and record it. A rule that is silently broken is worse than one that is explicitly waived. |
| **OD-G** | **Strike DR §12.1 Step 10's `jurisdictional_values` clause** (F-8), and record the 2026-08-12 REFERENCE-ONLY ruling *in the DB* rather than in a YAML header comment. | The next batch, which the runbook currently walks into a forbidden write. | **Strike it**, and add the ruling as a row-level note so an emptied-by-ruling table stops looking like an empty-for-want-of-data one. |

---

## 3. THE ACTS — ordered, with agonist and antagonist named for each

**Ordering rule:** an act runs only if its predecessor's antagonist did not sustain a blocking finding.
Acts 0–3 are corrections and are unblocked today. Acts 4–6 are research and need §2.

### Act 0 — Correct the instrument and the record. *(no owner gate except OD-F/OD-G)*

Corrections to existing documents, which every freeze clause permits.

1. **Amend `DR-2026-08-19` §3**: mark step 4 DONE; re-scope step 5 to *"render a determination for a
   cell chosen applicability-edge-first"*; append the §2 owner batch as steps 4a–4g. **Do not write a
   successor DR.** (F-1)
2. **Amend `governance/pipeline-map.yaml`** in place, recording each correction as the file's own
   convention requires: BRK-25 → `REFUTED`, with `_archived/scripts/migrations/029` and
   DR-2026-07-21 cited (F-2); BRK-26 `guard:` corrected and lines changed to 590–604 (F-3);
   BRK-24's "11" → 17 and the islands' phantom list reference removed (F-13); the false
   `grep`-returns-nothing sentence replaced with "no code reads it; four record files mention it"
   (F-12); `unclassified_paths:` replaced with the re-derived 1,229/2,171 figure and `README.md`
   removed (F-10); `steps_that_are_hand_sql` → `[4, 5, 7-partial, 8, 10]` (F-11).
3. **Amend the attestation**: correct `doctrine_sha` to `0f2f525`, withdraw the "the doctrine SHA
   moved" reason, correct 400 → 791 lines, 31 → 33 commits, and the §9 mis-citation. (F-14, F-22)
4. **Correct the session record**: `REF-00968.pages` is *supported but mis-filed*, not unasserted, and
   REF-00607/REF-00967 share the defect. (F-15)
5. **Sweep CLAUDE.md's own callers** — 28+ live references to §9/§10 that no longer exist — and replace
   §1's hard-coded "~35k executable LOC" with a derivation. (F-21, F-23b)
6. **Fix `.claude/session`** to the current session stem before anything else, so this session's
   provenance is not filed under the last one. (F-19)

**Agonist claim:** these are pure corrections; none adds apparatus; each is falsifiable by re-running
the command that produced the correction.
**Antagonist attack:** *"Amending a 791-line map that nothing reads is the recursion, dressed as
hygiene."* **Sustained in part** — hence the map is amended **only** where a reader would be actively
misled into a wrong act (BRK-25/26 drive act 1), and no new entry is added.
**Falsification:** if act 0 exceeds one commit and ~150 changed lines, it has become a project.

### Act 1 — The two fixes that must land before any retrieval

1. **`scripts/research/retrieval_log.py:95,100`** — choose the artefact extension from the content, not
   a hardcoded `.json`, and record it in the manifest's `artefact` field. ~3 lines, named in `e326e46`
   and deferred once. **The blocking `check_json` gate passes today only because seven artefacts were
   hand-renamed; act 2's first full-text fetch re-reds CI.** (F-18)
2. **BRK-26** — `scripts/assess/assess_cell.py:590–604`. The minimal fix is to **delete the interim
   view amendment**: the column it was waiting for exists, migration 029 supersedes its semantics, and
   the engine has no business rewriting a view mid-write. Do **not** touch BRK-25's live view. (F-2, F-3)

**Agonist claim:** both are defects in code, provable by running it; neither is owner-gated.
**Antagonist attack:** *"BRK-26 is not on the critical path — the write path is hand SQL and this engine
cannot address the cell (F-4), so this is elective work ahead of research."* **Sustained.** Consequence:
BRK-26 is fixed here **only because it is four lines inside a file act 1 is already open in**; if it
grows past that, it is deferred and recorded, and act 2 proceeds.
**Falsification:** `retrieval_log.py` fix is falsified if a deliberate HTML fetch still writes `.json`.
BRK-26's is falsified if the emitted SQL of a dry run still contains `DROP VIEW`.

### Act 2 — The search round, with the frame corrected at the *batch* level

The adjudication's query is right and insufficient. The batch-frame failure (R14 at frame level) was
that nine searches never crossed **parameter × setting × population**. Correcting it for AUT only
repeats the shape one population over — and it aims at the population the project's own reasoning
document says has **no** Tier-1 threshold, while the population that has one is unsearched (F-6, F-7).

Log verbatim before screening (R8), tier-ordered (R1). Minimum six executions:

| # | Population | Query shape |
|---|---|---|
| 1 | AUT/NDV | `("reverberation time" OR RT60 OR Tmf) AND (classroom OR school OR "learning space") AND (autistic OR neurodivergent OR SEN)` — the adjudication's query, unchanged |
| 2 | **DEAF** | `("reverberation time" OR RT60) AND (classroom OR "learning space") AND ("hearing aid" OR "cochlear implant" OR "hard of hearing")` — **the P1 miss** |
| 3 | **DEM** | `(reverberation OR "acoustic environment") AND (dementia OR "long-term care") AND (agitation OR wellbeing)` — closes **GAP-B01-002**, P1, the heaviest-weighted population (8 of 13 items) with no admission above PROXY |
| 4 | **MH** | any well-formed query at all — **GAP-B01-003**: MH (5 items) was never searched, never deferred, never mentioned |
| 5 | **BRAIN** | as above — appeared only as a conjunct inside another query, with no match row and no absence note |
| 6 | non-EN | `DIN 18041 Hörsamkeit Nachhallzeit Schule` (R5: non-English peer-reviewed work is academic, not grey) |

Keep every zero-yield with a `findings_note` diagnosing query-shape vs wrong-index vs genuine absence
(R14). **A zero-yield search is a completed unit of work.**

**Agonist claim:** non-trivial yield on 1–3 proves the 2026-08-19 zero-value finding was query-shape,
not absence.
**Antagonist attack, and it is the strong one:** *"You have read the reasoning document. You know the
answer is 0.3 / 0.4 / 0.5 / 0.6 s. Every query above is built to find what you already believe, and a
zero-yield you record will be a zero-yield you did not expect to matter."* **Sustained — and it is
structural, because DR §12.4 trap 12 (don't read the reasoning doc early) was written to prevent
exactly this and is now unavailable: the doc has been read, and reading it is *also* what revealed the
coverage failure.** Mitigation, recorded before searching: write the **prior expectation per query**
into `search_executions.findings_note` *before* running it, naming what result would surprise you;
grade tier and population-match **blind**, before consulting the doc (§4). The contamination cannot be
undone, only declared.
**Falsification:** if queries 2–5 return well-formed zero yields, the absence claim strengthens and
GAP-B01-002/003 close as *absence*, not as coverage failure — a real and publishable result.

### Act 3 — The bibliographic repair, and Emily's name

One migration, no new tables.

1. Backfill `volume`, `issue`, `pages_start`, `pages_end`, `article_number`, `issn` on all five rows
   **from the payload bytes held under `retrieval-log/`** — never from memory (CLAUDE.md §2(c)).
   Move the article numbers out of `pages` into `article_number` on REF-00607/00967/00968; keep
   REF-00966's true range `411-422`. Then either make `metadata_quality='COMPLETE'` true or stop
   asserting it. (F-15)
2. **`evidence_source_authors.corporate_name_note`** on REF-00966 position 3 — the column exists, is
   NULL, and this is the one act that protects an autistic co-author's chosen name from being deleted
   a second time on the paper whose entire Co-1 warrant is her co-authorship. Record: *"Emily publishes
   under the handle @21andsensory; `andsensory` is the surname as rendered by Crossref, OpenAlex,
   Europe PMC and the publisher. Correct rendering: **Emily (@21andsensory)**. Do not 'correct' this."*
3. **And add the check**, which is the one place in this plan where new apparatus earns its keep.
   `corporate_name_note` has **zero readers** (F-16), so the note alone stops nothing. CLAUDE.md §1
   asks what wrong thing reaches the *guidebook* if the check does not exist: **an autistic
   co-author is deleted from the source that carries the Co-1 grade — which has already happened
   once.** The check is ~15 lines: for any `evidence_source_authors` row whose `corporate_name_note`
   is non-null, fail if `last_name`/`first_name` changed without the note being updated in the same
   migration. Register it `blocking`, kinds `[data]`.
4. Populate `co1_source_type` and `co1_provenance` on all three Co-1 rows, or, where the warrant is
   not visible in the retrieved record, write the absence explicitly and let OD-D decide. **A tier is
   a judgement; a judgement with no recorded derivation is an assertion.**

**Agonist claim:** every field is copied from bytes on disk and is diff-checkable against them.
**Antagonist attack:** *"Adding a check inside the session that spent 6,716 lines removing them."*
**Answered, not dismissed:** the burden of proof is met by a named, already-realised harm, and the
check is registered rather than run ad hoc, so it is subject to the same symmetry rule as everything
else. If OD-D re-grades the Co-1 rows to T3, re-examine whether the check still has a subject.
**Falsification:** `--verify-authors` must run CLEAN with `EXAMINED > 0` after the migration; if it
prints CLEAN today over NULL fields, its scope is too narrow and *that* is the finding.

### Act 4 — Promote the held leads, blind-first *(needs OD-A, OD-B, OD-C)*

`source_locators` holds **835** leads the R9 gate cannot see. Three matter now, all already staged as
`search_candidates` and all named in `GAP-B01-004`:

- **REF-00561** `10.3390/app11093942` — Bettarello et al. 2021, *Indoor Acoustic Requirements for
  Autism-Friendly Spaces*. The second OD-5 witness; the most on-topic source for the population the
  last batch was studying, owned since 2026-08-06.
- **REF-00578** `10.1044/2016_AJA-15-0064` and **REF-00325** `10.1044/2019_AJA-19-0010` — Iglehart
  2016 / 2020. The first OD-5 witness, and the **only Tier-1 population-differentiated RT threshold
  the project has ever identified**.

Full R1–R15 walk each: DOI pre-check against **both** stores by hand (R9 cannot); re-retrieve every
locator through `retrieval_log.fetch()` (R10); mint nothing — reuse the held ref_ids (there is no
`next_ref_id` allocator and the stash high-water mark is 835); grade population-of-study against
population-served (R13) **before** reading the reasoning doc's own grades, then diff.

**The R13 result to expect, and not to soften:** Iglehart's participants are **children** with hearing
aids or cochlear implants. Against a served population of adults, and on a slug that currently serves
no hearing population at all, the honest grade is **PROXY** — the same grade that made REF-00607 the
weakest source in batch 1. *A Tier-1 study with a hard number is still PROXY if its population is not
the one served.* Recording that plainly is the point of R13.

**Agonist claim:** three admissions, one of them the first T1 numeric anchor on this parameter, all
from identifiers the project already owned.
**Antagonist attack:** *"You are promoting leads a prose document told you to promote, in the order it
suggested, and calling it retrieval."* **Sustained in part.** Mitigation: each promotion is
re-described from the retrieved payload under R15 and the staged description is corrected where it
over-claimed; the doc's tier guesses are recorded as guesses and **re-graded blind**.
**Falsification:** if the blind re-grade of REF-00561 does not land at T3, or Iglehart does not land at
T1-PROXY, the reasoning document is less reliable than this plan assumes and act 5 stops.

### Act 5 — One determination, authored by hand *(needs act 4 and OD-A/B/C)*

**Cell: A-18 × DEAF** — `RT60 in Occupied Learning and Listening Spaces`, for hearing-aid and
cochlear-implant users.

Why this cell and not another:
- It is the **only** cell on this slug where a numeric value has a Tier-1 anchor (Iglehart), a
  standards-side corroborant (ANSI/ASA S12.60 Footnote e), and an owner-signed prior reading.
- The AUT cell the last two sessions pursued has, by the project's own reasoning doc **and** by
  Marzi 2025 quoted in it, **no Tier-1 quantified threshold** — which is why it was correctly refused.
- Every other candidate on the slug (A-03, A-08, A-14, A-17 for AUT; A-05/06/07/09/10b for NDV) has
  an applicability edge but **no source carrying a value for it**: REF-00967's own note concedes it
  holds no RT60/NRC/STC/NC figure, and the three Co-1 sources are lived-experience accounts of
  agency, predictability and recovery — requirement-class findings, not threshold-class.

**How it is written.** Hand SQL against the scratch DB (DR §12.5: `specifications` is permanently
manual). `assess_cell.py` is not used and must not be — it addresses seven hardcoded pilot cells,
none of them this one, and it stamps a July session id and a July timestamp onto every row it writes
(F-4). Populate `specifications` + `specification_source_links` (role `governing`) +
`convergence_assessment`; `state` per `schemas/enums.py`; `falsification_condition` mandatory;
`governing_refs` consistent with the link rows.

**State: `provisional`, not `stated`, and the reason is R13.** The anchor is T1 but its population is
children and the served population is not. A `stated` cell here would be the "wrong number" the
antagonist warned about; a blank would be the "well-defended absence" it warned about more sharply.
**`provisional`, with the value present, the PROXY grade visible, and the falsification condition
naming the study that would settle it, is the third option both warnings point at.**

**Agonist claim:** one answered question, with its governing sources, its population-match grading,
and its search log including the empties.
**Antagonist attack, blind, before seeing the above:** re-derive the cell from the DB alone; re-grade
tier and population-match without reading this plan; attack through L1–L8; and press specifically on
**L5** (children→adults; a hearing population newly added to this slug by OD-B) and **L7** (would a
deaf person served by this recognise it, and does a `provisional` label read as a hedge or as
honesty?).
**Adjudication:** sustained → row correction by migration **in the same pass**; disputed → the cell
caps at `provisional` with the dispute recorded; doctrine-level → the owner. **One pass. A pass on a
pass is forbidden.**
**Falsification:** if the antagonist's blind grade differs from the agonist's on tier *or* population,
the divergence lands as a second `evidence_population_match` row keyed by `created_by_session` and the
cell does not advance past `provisional`.

### Act 6 — Render it, and read it

`python3 scripts/generate/spec_page.py` for A-18 (it reads `item_population_links`, so it renders
nothing useful until OD-C lands), then `build_site.py`, then **open the page and read it as a reader**.
Only then open `references/bpc-reasoning/room-acoustic-performance.md` and record convergence or
divergence against the May 2026 reading as a finding — in table columns, per D-2, with the prose as
supplement.

**This is the acceptance criterion.** *"One answered question, published … rendered and readable as
output, not as a row count and not as a green check."*

---

## 4. THE AGONIST–ANTAGONIST METHOD, as it applies here

Per DR §7 and the standing rule in `references/project-standards.md`.

**The agonist needs no construction.** R1–R15 already compel the authoring session to file its
complete affirmative case **as rows**: verbatim queries, re-retrieved locators, match grades, prior
expectation, named dissenter, falsification condition. The agonist's brief *is* the batch's data.
The one addition this plan makes is **prior expectation written before the query runs**, not after —
because F-7 means the answer is already known, and a prior expectation recorded afterwards is not one.

**The antagonist is a fresh context attacking the recorded case**, blind-then-compare: re-grade tier
and population-match **before** seeing the author's grades, then diff. That mechanic is what caught
A4/A5 in the 2026-07-26 precedent and MB1-011's downgrade in batch 1.

**Eight lenses**, each naming its claim and its evidence obligation: **L1** Existence · **L2** Fidelity
· **L3** Independence · **L4** Tier · **L5** Population · **L6** Contrary · **L7** Recognition ·
**L8** Query-shape.

**Four hard constraints, from the ratified rule and from what went wrong last time:**

1. **Subject discipline.** A pass may take as its subject only a diff that wrote research rows or
   authored a synthesis artifact. Acts 2, 3, 4, 5 qualify. Acts 0 and 1 do **not** — they get the
   mechanical gates and nothing more.
2. **One pass per batch. A pass on a pass is forbidden.** Three passes on a census, the third
   correcting the first two, is what happened last time.
3. **A pass emits data plus one session record. It may not create or modify a workplan.** To contest
   this plan, append **one page** of objection to this file, naming the clause and the evidence.
4. **SURVIVED is recorded, not only SUSTAINED.** A zero-finding pass must be able to show what it
   attacked, or it is indistinguishable from a pass that never ran.

**Adjudication has no third agent.** Sustained → row correction by migration in the same pass.
Disputed → cap at `provisional`, record the dispute. Doctrine-level → the owner. L5 needs no schema
change: `evidence_population_match` is keyed on `match_id` alone, so a dissenting grade lands as a
second row distinguished by `created_by_session`, and divergent grades read as a contest.

---

## 5. THE CULL, CONTINUED — but only after act 6

**Deliberately sequenced last.** The cull is the most satisfying work available and the least likely
to produce a row of evidence. Its plan is ~85% unexecuted (F-23c) and will keep. **Two exceptions
that ride along with acts 0–3 because they are corrections, not culls:**

- **Phase 0 record corrections** — planned and skipped three times. `check-registry.yaml:253` asserts a
  RED state measured 72/72 on 2026-08-18; three quarantine reasons assert RED states measured false.
  A registry that lies about its own health is CLAUDE.md §2(b) inside the gate inventory.
- **`adjudication_integrity.py` + its wrapper, 220 LOC** — kept on a claim verified false here (F-23a).
  Delete, with the evidence in the commit, per CLAUDE.md §1.

Everything else waits. When it resumes, the ranked list is: the four dead `references/` indexes
(**32,733 lines** — `claim-reference-join`, `global-reference-registry`, `specification-database`,
`bibliography-v11-draft`, all indexing REF-ids the 2026-08-06 reset deleted); the rooms stratum
(2,363 lines, generator crashes on a missing table, `build_site.py` disclaims it); the nine
zero-importer `schemas/` modules (1,136 LOC — one of which, `temporal.py`, was orphaned *by the cull
itself*); `anchor-correctness-sweep.js` (132 LOC, **zero mentions repo-wide including the
`.ignore`-hidden strata** — the cleanest single cull available); `code_currency_audit.py`;
`population_page.py` (wire it into `build_site.py` or delete it — an orphan generator for a live
surface is the worst of both). **Not candidates:** `generate_parts.py` (register it and give it a
freshness `--check` — it assembles the actual deliverable) and `emit_batch_sql.py` (invoked by prose
in CLAUDE.md §4 and the DR runbook). **Owner-gated:** `bootstrap.sh` (a platform-side caller may
exist), the `.ignore`/`deprecated/` moves, and every dead-table drop that sits inside the `items`
cascade.

---

## 6. ACCEPTANCE — five conditions, and only one of them counts

1. **A rendered A-18 × DEAF determination exists and has been read as a reader** — with its governing
   sources, its population-match grading including the PROXY call, and its search log including the
   empties. *(DR §4. This is the only one apparatus cannot satisfy.)*
2. **GAP-B01-002 and GAP-B01-003 are closed** — DEM carries a graded admission or a well-formed logged
   absence; MH and BRAIN each carry one. *(P1 and P2 in the live gap register, and neither appears in
   the previous handoff at all.)*
3. **GAP-B01-004 is closed** — the OD-5 witnesses are admitted, and the R9 blindness is either fixed or
   recorded as a live defect with its cost now paid three times.
4. **Net apparatus change ≤ 0**, counting the one check act 3 adds against the 220 LOC act 5's
   companion cull removes.
5. **The antagonist pass runs, on a qualifying subject, once**, and records SURVIVED as well as
   SUSTAINED findings.

**Scoring is honest or it is nothing.** The last plan scored itself **2 of 5** and said so; that was
the best thing in it. This one is scored the same way, in this file, before it is archived.

---

## 7. TERMINATION

1. **No successor document.** The next artifact after this file is a search log, a migration, or a
   rendered page. If the next session's first commit is a plan, this plan failed.
2. **Nothing mechanical enforces that**, and it must be said plainly: `meta_work_freeze` self-expired
   at `evidence_sources ≥ 1` and was retired the same day, so DR §11 property 3 now reads *"A successor
   plan is no longer build-rejected."* **This plan is itself the proof** — it could be written because
   nothing stopped it.
3. **This file is archived to `workplan/_superseded/` when §6 is scored**, whatever the score.
4. **It joins no read set.** DR §8 caps a fresh session's reading at four documents. This is not one of
   them; it is reached by citation from the DR's amended §3 and nowhere else.

---

## 8. DEVIATIONS AND SELF-CRITIQUE, recorded rather than absorbed

**Deviation 1.** This plan is the fifth-order artifact in a sequence the repository has already
diagnosed: batch → adjudication → provenance walk → this. Its own findings section says 3,266 lines of
prose were added against zero rows of evidence in the last three sessions, and then adds ~700 more.
The defence is that acts 4–6 end in rows and a rendered page and the whole file expires when they do;
the defence is not self-evidently sufficient, and F-9 records that the review producing it ran against
the ratified subject rule.

**Deviation 2.** The review was commissioned as read-only and this file is a write. It adds no rows and
no checks; the one check it proposes is proposed, not landed.

**Deviation 3.** The reasoning document has been read. DR §12.4 trap 12 exists to prevent exactly the
contamination that follows, and it cannot be undone — only declared, and countered by writing prior
expectations before queries and grading blind before comparing.

**Bias direction.** I am biased toward A-18 × DEAF being the right cell, because I found it, and
because a cell with a hard number is a more satisfying deliverable than a cell without one. The
specific risk that creates: I may be under-weighting how badly **PROXY** damages it — children are not
adults, and a slug that has never served deaf people acquiring both a deaf population and a deaf-anchored
determination in the same session is a coincidence worth distrusting. Against that, a bias the other
way: refusing is cheap, produces an unfalsifiable artifact, and has now been the outcome twice.

**The strongest counterclaim a reviewer could make.** *"This plan solves the last session's problem by
finding a better cell, when the actual finding is that the answer was written in May 2026, owner-signed,
and destroyed by a ratified reset — so the project's real question is not which cell to author next but
whether the clean-room reset was worth what it cost, and this plan does not ask it."* That is a fair
charge, and the honest answer is that the question is the owner's, not mine: `DR-2026-08-06` is ratified,
the reset's rationale was contamination, and re-litigating it is DG-NON. What this plan does instead is
make the destroyed work **recoverable as leads under R15** rather than lost — which is the most that can
be done without reopening a ratified decision.
