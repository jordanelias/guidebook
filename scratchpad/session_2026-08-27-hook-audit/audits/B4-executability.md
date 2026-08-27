# B4 — Adversarial audit: walkability and executability of WALKABILITY-PLAN.md Part 7

**Lens: hand this plan to a Sonnet session. Does it execute, or does it turn `main` red, produce a
vacuous pass, or miss a caller?** Audited 2026-08-27 against `data/guidebook.db` `user_version` 64
(read-only), HEAD of the working tree, SQLite 3.45.1. Every finding below is bound to a measurement,
a test run this session on a scratch copy, or a file:line; commands are inline. Conventions stated
where a count depends on one. No tracked file other than this report was written.

**Verdict up front.** The plan's diagnosis and track-split are sound, and its best safety devices
(T-0.4 helper, T-A3 gating T-A2, run-both `--selftest`/`--changed-from`) are real. But executed
top-to-bottom by a Sonnet that does what the task tables say, it breaks `main` at T-A2 in at least
two independent ways (B-1, B-4), stalls on three acceptance criteria that cannot be satisfied on a
healthy repo (M-1, M-2, M-5), and reproduces the exact defect its own Part 9 convicts the source
document of: **the corrections are recorded after the plan instead of merged into it, so the
transcription surface a mechanical executor reads is the refuted text** (B-3).

---

## BLOCKERS

### B-1 · T-A2 renames `source_locators` while two committed data migrations still write it by name — the rebuild breaks, and the plan's own "0 of 33" claim is false for this table

T-A2 (WALKABILITY-PLAN.md:728) claims: *"No `AFTER_DATA` — measured: 0 of 33 data migrations
reference any table this touches"* — and then its own rename table (line 735) includes
`source_locators → res_items`. Measured, using the plan's OWN DML-only convention from §9.9:

```bash
grep -lE '(INTO|UPDATE|FROM|TABLE)[[:space:]]+"?source_locators"?[[:space:],(]' scripts/migrations/data_*.sql
# → data_20260822053540... (string-literal only — not executable)
#   data_20260823223155... (INSERT INTO "source_locators" — real DML)
#   data_20260823225142... (UPDATE source_locators / INSERT INTO source_locators — real DML)
```

Two files carry genuine DML; both timestamps exceed `BASELINE_DATA_CUTOFF_TS = "20260812083255"`
(`scripts/migrate_db.py:267`), so both **replay on every `--rebuild`**. The default plan order is
all schema then all data (`migrate_db.py:286–298`), so migration 065's rename runs first and the
replay dies. Demonstrated on a scratch copy this session:

```
ALTER TABLE source_locators RENAME TO res_items;   -- then replay the committed DML:
UPDATE source_locators ...  → REPLAY FAILS: no such table: source_locators
INSERT INTO source_locators → REPLAY FAILS: no such table: source_locators
```

`migration_reproducibility` is **blocking** (`governance/check-registry.yaml:326`), so `main` is
red on the first CI run after T-A2. Note the plan holds the refutation of its own claim: §9.9's
correction table (line 1054) prints `source_locators | 3` under DML-only, and C5's track split
(line 291) assigns `source_locators` to **Track B** — yet T-A2's table pulls it into Track A with
the zero-collision claim intact. The internal contradiction was never reconciled.

The plan's supporting claim that AFTER_DATA is *"in live use by two migrations"* (line 269) is also
false today: `grep -lE '^--\s*AFTER_DATA:' scripts/migrations/*.sql` matches **nothing** — the 056
marker was absorbed into the 057 baseline, whose header says *"It is unused now."* The mechanism
exists (`migrate_db.py:283–330`, verified) but has never run against the current migration set.

**Failure scenario:** Sonnet ships `065_the_item_spine.sql` exactly as specified; local
`--rebuild` fails (or, if skipped because the acceptance's byte-identity clause already failed —
see M-1 — gets pushed anyway); blocking `migration_reproducibility` turns `main` red.
**Smallest fix:** either move the `source_locators → res_items` rename to Track B (where C5 already
put it), or put `-- AFTER_DATA: 20260825215123` on 065 — and in either case scratch-test
`migrate_db.py --rebuild` before commit, because this would be AFTER_DATA's first live firing since
the baseline.

### B-2 · T-A3's acceptance depends on work the plan schedules at T-B — the exact later-step dependency this audit was told to hunt (the A2-B4 class, reproduced)

T-A3 acceptance 2 (line 788): *"A rendered figure resolves to its extraction and its paper by key
path alone."* Rendering anything requires the generators. But after T-A2, `specifications` is
`spe_items` and `bpc_metadata` is `syn_items`, and:

- `scripts/generate/build_site.py` — `FP_TABLES` names `specifications`,
  `specification_source_links`, `item_bpc_links` (plus `items`, `item_population_links`); its
  build walks `SELECT item_code FROM items` (A3-F14, verified by grep this session);
- `scripts/generate/spec_page.py`, `population_page.py`, `scripts/generate_parts.py` all query
  `specifications`/`bpc_metadata` (3 executable refs in `generate_parts.py` alone).

The generator rewrite is scheduled **at T-B**: §9.8's own resolution is *"promote it in the same
commit that rewrites the generators (T-B)"*, and no T-A2 or T-A3 task rewrites any generator. So at
T-A3 the render stage cannot execute at all — the walk's sixth stage is a crash — and acceptance 2
is unsatisfiable until a phase that comes after the phase it gates. This is precisely the sequencing
class A2-B4 found in the source document (*"Part L's step 1 arms a blocking gate against a table
Part I retires"*), re-created by the document that cites A2-B4.

**Failure scenario:** Sonnet reaches T-A3, cannot render, and either declares the phase passed on
acceptance 1+3+4 (leaving the spine's book-facing claim untested — the §2(a) shape) or pulls T-B's
generator rewrite forward ad hoc, unswept. **Smallest fix:** scope T-A3 acceptance 2 to the SQL
level (the key-path join from a determination row to `evi_source_authors`, which this session
verified is expressible — see "could not break" below), and move the generator rewrite explicitly
into T-A2's commit, where the blocking freshness gates already force it (B-4).

### B-3 · Part 9 refutes Part 7's tables and the GATE text, and the plan ships both with only "Part 9 wins" as the merge instruction — the transcription surface is the refuted text

The plan states (line 862): *"The earlier text is left in place rather than overwritten."* The
consequences for a mechanical executor:

1. **T-A2's DDL table (lines 735–739) is the shape §9.3 rejects.** It says `evi_items` gains
   `research_item_id NOT NULL`; K1 (line 916) moves that key to `evi_sources` on measured grounds
   (six admitted sources `REF-00965`–`REF-00970` have no clue-store row). It says `syn_items` is
   renamed `bpc_metadata`; K2 (line 917) says the re-key off PK `slug` is *mandatory*. The
   `jud_items` column block (lines 744–759) still contains the four `evidence_population_match`
   fold-in columns that X4 (line 872) withdraws ("Refuted on grain... My 'resolution' was wrong").
   A Sonnet transcribing DDL from Part 7 — the phase section, the natural place — ships all three
   refuted shapes. This is A3-F1 (*"Part E specifies the key shape Part B rejects... Part E is the
   table a migration-writer will transcribe DDL from"*) reproduced one document later.
2. **The GATE's Q1 text (line 701) sends the owner a measurement the same document declares
   false.** It says reading (a) is *"contradicted by live data: evidence_population_match holds 25
   grades across 10 sources"* — and §9.1-X3 (line 871) rules: *"The measurement does not reach the
   question... Q1 is a genuine design question, not a countable one."* §9.2 replaces the whole
   framing (recommend (d); put only (a)-vs-(b), as a dissent-design question, *"with no false
   measurement attached"*) — but no rewritten GATE text exists. S-3 (*"put the measurement, not the
   question"*) is violated by the only gate message the plan provides.
3. **Part-9 additions never enter the task tables.** Verified absent from every T-row: the
   `figures` table (counted `+1` in §9.5's arithmetic, line 984; created nowhere), the re-mint of
   the 11 `REF-VERIFIED-*` ids (§6.4, line 543: *"must be re-minted BEFORE the per-stage allocators
   are written"*; in no phase), K3's blocking zero-link check (line 918: *"DDL alone cannot carry
   it"*; no registry entry is scheduled), and §9.4's DR-2026-08-06 supersession paragraph +
   PROMOTE-status writer refusal, which §9.4 itself says *"is a T-0 item"* (line 938) — T-0's table
   (lines 665–671) has four rows and this is none of them.

**Smallest fix:** one reconciled Part 7′ — regenerate the T-0/T-A2 tables and the GATE text with
Part 9 applied, and mark Part 7 superseded in place. That is exactly the "one plan, reconcile E
against J" remedy A2's verdict imposed on the predecessor.

### B-4 · The T-A2 caller sweep, as named, misses at least five BLOCKING-check enforcers that query the renamed tables — including the biggest one, `validate_evidence_state.py`

The union of Part G's list (per A3-F6: views, `db.py`, `dbcore`, `schemas/`, pipeline-contract,
`pipeline_completeness.py`, registry `basis:` refs, skills, `data_*`) and §9.7-A's additions
(line 1015) was checked against a derived caller set:

```bash
for t in specifications bpc_metadata source_value_extractions source_locators; do
  grep -rlE "\b$t\b" scripts tools schemas governance skills --include='*.py' --include='*.yaml' --include='*.md' | grep -v __pycache__; done
```

**Missing from both lists, with executable SQL against a table T-A2 renames** (ref counts by
`grep -cE '(FROM|INTO|UPDATE|JOIN)\s+...'` per file):

| file | refs | consequence at T-A2 |
|---|---:|---|
| `scripts/validate_evidence_state.py` | reads `specifications` + `convergence_assessment`; line 352 returns error *"tables absent"* on a missing table | **blocking `validate_evidence_state` RED** |
| `scripts/tests/test_db_integrity.py` §named in 9.7-A ✓ but listed here for the count: lines 123/521/527/689 | 6+ | blocking `test_db_integrity` RED (named — sweep must actually fix it) |
| `scripts/audit/check_rendered_docs.py` | 3 (lines 96/196/212) | **blocking `check_rendered_docs` RED** |
| `scripts/validate_verification_consistency.py` | 3 (lines 55/100) | **blocking `validate_verification_consistency` RED** |
| `scripts/audit/research_batch_dod.py` | 4; its `--selftest` *"must clone the LIVE schema"* (line 108) then `INSERT INTO source_locators` (lines 735/741) | **blocking `research_dod_selftest` RED** |
| `scripts/audit/citation_mining_completeness.py` | 1 `FROM citation_mining` | blocking `citation_mining_session` RED at **T-B.4** |
| `scripts/assess/assess_cell.py` | 2 | breaks (uncalled by a check, but a writer path) |
| `scripts/audit/adjudication_integrity.py` | 5 | breaks |
| `scripts/audit/register_integrity_check.py` | 2 | advisory red |
| `scripts/audit/pre_rehab_banner_audit.py` | 1 | breaks |
| `governance/research-contract.yaml` | names `specifications` (R12 area) | editing it trips **blocking `research_contract_sync`** unless the SessionStart hook is regenerated in the same commit |
| **17 skills** (union naming `specifications`/`bpc_metadata`/`source_locators`; 13+4+2 by table) | — | a skill is a caller (§0.4); T-B.3 sweeps only `MOB` + retired population codes |

Plus one **path error** in §9.7-A itself: it names `scripts/generate/generate_parts.py`, which does
not exist — the file is `scripts/generate_parts.py` (`ls` verified). A helper built from the named
list sweeps a nonexistent path and misses the real caller.

The plan's safety net is that T-0.4's helper is supposed to be a true tree-wide + `sqlite_master` +
registry + skills grep, in which case all of the above are found at run time regardless of the
named list. **But T-A2's task table never instructs running the helper** — the word "sweep" does
not appear in T-A2, and its acceptance (rebuild/selftest/`foreign_key_check`/inbound-FK) contains
no battery-green criterion, so a Sonnet can satisfy T-A2 as written and push a `main` that is red
on five blocking checks. **Smallest fix:** add to T-A2: "run the T-0.4 helper for every old→new
name in this migration; acceptance additionally requires `run_checks.py --changed-from origin/main`
green" — the same clause T-0 already has.

---

## MAJOR

### M-1 · "`--rebuild` byte-identical" fails on healthy `main` today — an acceptance test that can never pass

T-A2 (line 770) and T-B (line 812) both accept on *"`migrate_db.py --rebuild /tmp/rebuilt.db`
reproduces byte-identically."* Measured this session on the untouched tree:

```
python3 scripts/migrate_db.py --rebuild $SCRATCH/rebuilt.db   # exit 0
sha256: data/guidebook.db 6cceacd2… · rebuilt.db 76b5bf6a…    # NOT identical
```

The actual contract is `migration_reproducibility`'s seven invariants plus the `--deep`
content compare modulo `VOLATILE_COLUMNS` (`scripts/audit/migration_reproducibility.py:55–71`) —
byte identity of a SQLite file is not and has never been the gate. A literal Sonnet either stalls
forever on an unpassable criterion or starts "fixing" the canonical DB, whose sha256 §4 forbids
moving. **Fix:** acceptance = `migration_reproducibility` and `_deep` green.

### M-2 · T-A1's acceptance "`pipeline_completeness_fresh` green with `EXAMINED: n > 0`" is unsatisfiable — the check is deliberately uninstrumented

`tools/pipeline_completeness.py:844`: *"Deliberately NOT instrumented with an EXAMINED line"*, and
the registry entry carries `no_floor: not-instrumented` with the recorded 2026-08-14 reasoning
(`check-registry.yaml:1293–1308`). The clause cannot be observed green; satisfying it requires
instrumenting the check against a recorded considered-and-reverted decision — the "promoting past
the recorded reason unexamined" move A4-B9 flags. **Fix:** drop the `EXAMINED` clause for this
check (keep it for the stage rows inside the dashboard if wanted), or re-open the recorded decision
explicitly.

### M-3 · T-A1.2's justification for the four-criteria move is false for one of the four, and the criterion that "stays" is about a table the same plan moves to synthesis

Verified against `governance/pipeline-contract.yaml:73–101`:

- `governing-refs-nonempty`, `no-regulatory-stratum-stated`, `tier3-alone-threshold`: check =
  `scripts/validate_evidence_state.py`, which validates **`specifications` rows**
  (`validate_evidence_state.py:237`) — the plan's claim holds for these three.
- `derivation-handshake`: **`check: null`**, with the contract's own comment: *"honestly
  DECLARED-BUT-UNENFORCED, not phantom-VERIFIABLE"* (contract lines 92–96). The plan's sentence
  "All enforced by `validate_evidence_state.py` against `specifications`" (M-6, T-A1.2) is false
  for it. The move is still right — its criterion text is about determinations — but the stated
  test does not separate the four from the fifth, so an executor checking the plan's premise finds
  it false and stalls or improvises.
- `convergence-independence` "stays with judgment" — but its subject is `convergence_assessment`,
  which Part 6.2 (line 409) moves to **synthesis** (`syn_convergence`) at T-B. After T-B, judgment's
  only criterion governs another stage's table. Decide its home in the same breath as its table's.

### M-4 · T-A1 and T-A2 both change generator inputs and never schedule the regeneration commit

T-A1.3 edits `tools/pipeline_completeness.py` (STAGES, ten queries, `items_judged`) — the committed
`tools/pipeline-completeness-dashboard.html` (DEFAULT_OUT, line 33) immediately diverges, and
blocking `pipeline_completeness_fresh` compares them. T-A2 changes what
`tools/evidentiary_audit.py` reads (`bpc_metadata` at lines 247/353 — blocking
`evidentiary_audit_fresh`). No task row in either phase says "run `scripts/regenerate_derived.sh`
in the same commit." The acceptance criteria imply it for T-A1 only; T-A2's acceptance omits the
render battery entirely (see B-4). **Fix:** one line in each phase.

### M-5 · T-A1's acceptance "no five-stage list outside `_archived/` and `sessions/`" requires editing ratified DRs and frozen records — unachievable without breaking append-only rules

Measured (`grep -rlE "research.*evidence.?collection.*judgment.*synthesis.*render"` excluding
`_archived`, `sessions/`, `.git`): **12 files**, including `decisions/DR-2026-08-24-…` (a ratified
DR), `references/project-standards.md` (append-only ledger), five frozen scratchpad files of prior
sessions, and this plan's own document plus two A-audits that QUOTE the five-stage list in order to
criticise it. Satisfying the acceptance literally means rewriting records the repo forbids
rewriting; not satisfying it means the phase never closes. **Fix:** scope to live machine surfaces
— `pipeline-contract.yaml`, `tools/pipeline_completeness.py`, `CLAUDE.md`, `check-registry.yaml`.

### M-6 · K1's corrected key placement is mechanically harder than any phase states, and the plan carries no task for it

Under §9.3-K1 the lead key lands on `evi_sources` — a table with **10 live rows**, six of which
(`REF-00965`–`REF-00970`) have no clue-store parent. Tested this session on 3.45.1:

```
ALTER TABLE evi_sources ADD COLUMN research_item_id TEXT NOT NULL REFERENCES res_items(ref_id)
→ FAILS: Cannot add a NOT NULL column with default value NULL   (table non-empty)
```

So K1 requires a create-copy-swap on a **populated** table — a third rebuild beyond T-A2's stated
two (*"evi_items and syn_items. Both hold 0 rows, so it is trivial"*) — plus the six backfilled
`origin='hand-entered'` lead rows A3-F3 specifies, which are a **data migration** (with ledger
rows), not DDL. None of this appears in T-A2. The "trivial" claim is true only for the shape Part 9
rejected. **Fix:** T-A2 gains: (a) create-copy-swap of `evi_sources`; (b) a paired
`emit_data_migration` for the six backfill leads, header declaring them legacy.

---

## DEFECTS

- **D-1 · T-0.2's "NULL forward" collides with a NOT NULL constraint and two replaying INSERTs.**
  `evidence_population_match.source_ref` is `TEXT NOT NULL` (DDL verified), and two post-baseline
  data migrations INSERT it (`grep -l source_ref scripts/migrations/data_*.sql` → 2 files, both
  2026-08-19, ts > cutoff). Rule 5 forbids the drop; NULLing forward requires removing the NOT
  NULL, i.e. a **schema migration** with a table rebuild — which consumes migration number 065,
  while T-A2 hardcodes `065_the_item_spine.sql`. Say "the next free number" and note the
  constraint-drop mechanics in T-0.2.
- **D-2 · T-A1.3's query list is 10 of 12.** `grep -c "FROM specifications"
  tools/pipeline_completeness.py` → 12; lines 232 and 235 (the item-frontier matrix) are absent
  from the plan's list. Same file, same fix, so cheap — but the plan's list is presented as
  exhaustive.
- **D-3 · T-A1.4 names 1 of 3 live `basis:` refs.** The only stage-qualified judgment refs are the
  three on `check-registry.yaml:571` (`governing-refs-nonempty`, `no-regulatory-stratum-stated`,
  `tier3-alone-threshold`, one list, one line). The hedge "plus any other moved by T-A1.2" covers
  them in practice; the derived list should simply be stated. Verified that C7
  (`scripts/run_checks.py:759–770`) fails on any `basis` containing "/" absent from the contract —
  so a missed re-point IS caught by `--selftest`, and `ci.yml:114–115` runs `--selftest` blocking
  on every gated run, so even a skipped local run is caught in CI. The plan's claim that
  `--changed-from` alone misses it is confirmed correct.
- **D-4 · §9.7-A path error**: `scripts/generate/generate_parts.py` does not exist; the caller is
  `scripts/generate_parts.py` (3 executable refs). See B-4.
- **D-5 · Registry-note drift the plan creates and does not schedule.** After T-A3 writes the first
  determination, `validate_evidence_state`'s `no_floor: empty-by-decision` reason (registry
  :573–583, *"Both are 0 today"*) becomes false and should flip to `min_items` per the registry's
  own house rule; likewise the `site_pages_fresh` note's *"93 today"* and the
  `pipeline_completeness_fresh` note's *"bpc_metadata is empty post clean-room-reset"*. No T-C row
  covers registry-note re-derivation.
- **D-6 · The spine's own keys contradict §6.4's constraint 3.** T-A2's `jud_items` spec references
  `evi_items(extraction_id)` — the INTEGER surrogate §6.4 lists as a defect (*"4 of the spine
  objects key on an INTEGER"*) — and no phase re-keys `evi_items` or `spe_items` to minted
  `EVI-/SPE-` codes. Either constraint 3 is deferred (say so, dated) or the re-key belongs in
  T-A2's create-copy-swap list, which for these two 0-row tables is where it is cheapest.
- **D-7 · T-A3's walk depends on writers whose specification exists only as one row of §9.7-C.**
  Verified: `scripts/db.py` has no `add-extraction`/`add-synthesis`/`add-specification`/junction
  writers (A3-F2/F16, reconfirmed by parser grep). §9.7-C says "writers ship with the migration" —
  an Opus-scale design task compressed into a table cell, with no column semantics beyond the
  `jud_items` sketch. If the writers slip, T-A3 is unexecutable by its own rule 4 ("never
  hand-write SQL against a table the CLI can reach") — the right refusal, but the plan should name
  the writer set as a T-A2 deliverable with its own acceptance (each writer refuses at least once
  in T-A3, which acceptance 4 already half-states).

---

## Answers to the eight briefed questions

1. **Sequencing.** Two later-step dependencies found: T-A3→T-B generators (B-2) and §9.4's
   "T-0 item" absent from T-0 (B-3.3). T-0.2 also silently consumes T-A2's hardcoded migration
   number (D-1). Otherwise T-0→T-A1→GATE→T-A2 preconditions hold.
2. **Acceptance tests.** T-A3's join is **valid SQL in both candidate shapes** — built and run on a
   scratch DB this session; the K1-corrected walk
   (`res_items ⟵ evi_sources.research_item_id; evi_items.ref_id ⟶ evi_sources; jud → syn-links →
   syn → spe-links → spe`) returns the row. But under K1 the res→evi hop traverses the
   `evi_sources` satellite, so acceptance 1's "using only hand-off keys" is textually
   unsatisfiable in the corrected schema — reword to "using only keys, never `slug`".
   T-A2's "≥1 inbound FK on each hand-off object" is necessary, not sufficient — vacuously true
   between empty tables — and the plan itself says so (S-2, T-A3 gates T-A2): correct as a
   structural precondition, honest only because T-A3 exists.
3. **Blocking gates per phase** (exhaustive over the 64-check registry; 25 blocking): T-A1 —
   `pipeline_completeness_fresh` (stale dashboard, M-4); `--selftest` C7 if basis refs missed
   (caught). T-A2 — `migration_reproducibility` (B-1), `validate_evidence_state`,
   `test_db_integrity`, `check_rendered_docs`, `validate_verification_consistency`,
   `research_dod_selftest`, `evidentiary_audit_fresh`, `pipeline_completeness_fresh` (second
   edit: `spe_items`); advisory red: `site_pages_fresh`, `validate_items`, `context_map_fresh`,
   `register_integrity_check`, `validate_pydantic_schemas`, `graph_audit`. T-B —
   `citation_mining_session` (renames `citation_mining`), `validate_axes` (named ✓),
   `evidentiary_audit_fresh` again (reads `search_languages`/`search_coverage`, both deleted at
   T-B.5 — `tools/evidentiary_audit.py:250/261/369–373`), `research_contract_sync` if
   `research-contract.yaml` is touched. Vacuous-pass risk: `validate_evidence_state` post-rewrite
   examines 0 by declared decision (fine today; flip to `min_items` after T-A3 — D-5).
4. **`--selftest` vs `--changed-from`.** Confirmed: C7 fails on dangling stage-qualified basis
   refs; selftest runs blocking in CI's classify job (`ci.yml:114–115`) on every push and PR, so
   the failure cannot reach a green `main` even if the plan's run-both instruction is skipped.
   Real basis list: the three refs on `check-registry.yaml:571` (plan names one; D-3).
5. **Caller sweep completeness.** Materially incomplete — five blocking-check enforcers plus
   `assess_cell.py`, `adjudication_integrity.py`, `register_integrity_check.py`,
   `pre_rehab_banner_audit.py`, `research-contract.yaml`, 17 skills, and one wrong path (B-4, D-4).
   Views: 10 of 18 reference the four renamed tables; `ALTER TABLE RENAME` rewrites their bodies
   automatically (A3-F9's measurement, relied on, not re-tested), so views survive T-A2
   mechanically — the sweep burden is the Python/YAML/skill callers.
6. **The four moved criteria.** Three of four genuinely enforced by `validate_evidence_state.py`
   against `specifications`; `derivation-handshake` is `check: null`, declared-but-unenforced —
   the plan's premise is false for it (M-3). `convergence-independence` staying is doubtful once
   its table moves to synthesis at T-B (M-3).
7. **Attestations/commit format.** T-C is clean: T-C.2 writes `decisions/`, T-C.3 explicitly
   schedules the rule-2 attestation. No other phase touches a rule-2 path (`CLAUDE.md`,
   `governance/`, `workplan/`, `scratchpad/` are outside rule 2's four paths). Commit format is
   ambient rule 1 and the plan neither restates nor contradicts it. One gap: the session close
   that writes `sessions/<stem>.md` owes its own attestation, and the plan (which will span
   sessions) never mentions session-close mechanics.
8. **The GATE.** Procedurally it blocks the right things — T-A2 declares "blocked on Q1, Q2", and
   Q3's non-blocking status is sound (the status quo is files; T-A2's `syn_items` adds no prose
   column, so proceeding ratifies the default reversibly). But it is prose-only — nothing
   mechanical stops a `dontAsk` session from rolling through — and the graver defect is B-3.2:
   the gate text an executor would send is the version §9.1-X3 refutes.

## Attacked and could not break

- **The C5 zero-collision claim for the true spine.** Re-measured under the plan's DML-only
  convention: `specifications`, `bpc_metadata`, `source_value_extractions`, `items`, `axes`,
  `convergence_assessment`, `spec_value_probes`, `item_bpc_links` — **0 data-migration files
  each**, exactly as claimed. Only `source_locators` breaks the set (B-1).
- **T-0.1's line citations.** `CORE_INVARIANTS` at `migration_reproducibility.py:54–63`, `needed`
  at 137–138, selftest hardcoding `items` at 446–563 — all verified; the de-hardcode is the right
  first move and its contract/DR framing (§9.7-B) is accurate.
- **T-A1.3's ten line numbers** — all ten verified against the file (the two missed are D-2).
- **The T-A3 join** — valid SQL, returns the walk row on a scratch build of the proposed schema.
- **The AFTER_DATA mechanism** — present and correctly described at `migrate_db.py:283–330`
  (plan says 282–320; off by a few lines, mechanism as stated), though currently unused (B-1 tail).
- **CI wiring claims** — `--selftest` blocking in classify (`ci.yml:114`), render battery on every
  gated run (`ci.yml:251`), commit-format check push-only (`ci.yml:257`): all as the plan and
  CLAUDE.md describe.
- **§9.8's site_pages_fresh sequencing correction** — verified sound: the check is advisory today
  (`check-registry.yaml:1361`), reads `items` for its EXAMINED corpus, and deferring promotion to
  the T-B generator-rewrite commit is the right order.

---

**Digest (5 lines):**
1. BLOCKER B-1: T-A2 renames `source_locators` while 2 post-baseline data migrations still write it — rebuild breaks (demonstrated on scratch), blocking `migration_reproducibility` red; the plan's "0 of 33 collisions" is refuted by its own §9.9 table.
2. BLOCKER B-2/B-3: T-A3's "rendered figure" acceptance needs generators rewritten at T-B (later-step dependency), and Part 7's DDL tables + GATE text are the shapes/measurements Part 9 refutes, with no merged text — a transcribing Sonnet ships the refuted schema and sends the owner a falsified measurement.
3. BLOCKER B-4: the named caller sweep misses ≥5 blocking-check enforcers (`validate_evidence_state.py`, `check_rendered_docs.py`, `validate_verification_consistency.py`, `research_batch_dod.py --selftest`, `citation_mining_completeness.py`) plus 17 skills and one wrong path; T-A2 never instructs running the T-0.4 helper and its acceptance omits the check battery.
4. MAJOR: three acceptance criteria fail on a healthy repo — "rebuild byte-identical" (shas differ on clean main, measured), "pipeline_completeness_fresh with EXAMINED>0" (deliberately uninstrumented, source line 844), "no five-stage list outside _archived/sessions" (12 files incl. a ratified DR); plus K1's key needs a populated-table rebuild + 6-row backfill no phase schedules (ADD COLUMN NOT NULL fails, tested).
5. Sound and verified: the spine/nomenclature track split, T-0.1's citations, T-A1.3's line list, the walk join's SQL validity, C7 catching basis drift in CI, and §9.8's promotion sequencing — the plan's skeleton executes once Part 9 is merged into Part 7 and the six fixes above land.
