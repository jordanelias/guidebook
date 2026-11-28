# Second antagonist: the implementation of T-117 and T-056 item 3a

Read-only pass, 2026-11-27. Subject: `d13caa4d`, `4454d789`, `5570c7f5` (HEAD `dfd9f017` adds logs only: `git show --stat dfd9f017`). Every scratch artefact lives under `$S=/tmp/claude-0/-home-user-guidebook/943cc08d-9b18-5690-b0c6-54a354b936e3/scratchpad/ant2`. I used two worktrees, `$S/../wt-main` (origin/main `2ee5cf77`) and `$S/../wt-head`, and then removed them. Re-run the commands. Do not trust the figures.

## Phase 1 (blind): what a correct implementation must and must not do

From OD-57, OD-59, OD-64, OD-48 (a), the delegated OD-92/95/98/99/100/110 and the T-117/T-056 task files:

- **Must.** `band()` follows the table: ● T1, T2 (Co-1 and Co-2 sit there); ◐ T3 non-grey and T4; ○ T5 and T6.
  - Grey takes ⚠ in place of any circle, U+26A0 alone (OD-64).
  - The regulation-only override goes, so a T4-only basis shows ◐.
  - A shown value takes the mark of its stating source (OD-59).
  - The ⚠ member gets no ordinal.
  - The CHECK is widened by a faithful rebuild.
  - `design_scale` is set from the key (OD-48 (a)).
  - `RULE_VERSION` is bumped.
- **Must refuse, not decide.**
  - A non-VERIFIED stating source → refuse, naming OD-99 Q1 and OD-100.
  - Stating sources with different marks → refuse, naming OD-92.
  - PROXY-thin and `rests_on_proxy_inference` as thin causes are not built (OD-98, Q3).
  - The engine reads no retrieval log.
  - The C10 interim text comes from OD-99 Meanwhile.
- **Likely failure points.**
  - The `stating` set when an interval's two bounds come from different sources.
  - A cell that shows no value (it falls back to the floor mean, which can show a circle on a grey or unverified basis).
  - The R39 confirmation path, now that the override is gone.
  - Tests weakened so that they skip refused cells.
  - `AFTER_DATA`.
  - Prose callers that state the old table.

## Results, derived

**Migration 168: clean.**
- `git show origin/main:data/guidebook.db` and `5570c7f5^`'s database are both sha `3d419efb…`. Running `migrate_db.py` on a copy gives `ac7bc287…`, byte-identical to the committed blob, so the blob was changed only through the migrate flow.
- Pre against post (`python3 $S/cmp.py $S/pre.db $S/post.db`):
  - 183 sqlite_master objects on each side: 65 tables (64 plus `sqlite_sequence`) and 30 views, so the "94 objects" claim holds;
  - only `specifications`' SQL differs;
  - every table's rows are equal;
  - `foreign_key_check` is empty;
  - `sqlite_sequence` stays at 8;
  - `integrity_check` returns ok.
- `--rebuild` against post: identical apart from `data_migrations.applied_at/applied_by_session/notes`. `content_sha` is equal.
- `migration_reproducibility --deep`: PASS, EXAMINED 67. `--selftest`: PASS.
- UNWRITABLE: the same single line before and after.
- `AFTER_DATA` is not needed. The CHECK only widens. `build_plan()` places 168 at index 268. Two later data migrations name `specifications`, in prose only (`grep -il specifications scripts/migrations/data_*.sql`).

**New tests: red on origin/main for their stated reasons.**
- I copied HEAD's test file into wt-main and replaced the `OpenQuestion` import with a stub. Result: 22 FAIL, the four changed pre-existing assertions among them (`$S/red-on-main.txt`).
- T117-11 (b) and (c), the guards, are green on both.
- Everything is green on HEAD (282 cases).
- The pre-existing C10 subject was 0 and is still 0: `PASSED HAVING EXAMINED NOTHING`, C10 included.
- T117-11's seeding is honest as a unit test of C10:
  - each case seeds a live cell on a copy;
  - `role` defaults to `governing` (`PRAGMA table_info(specification_source_links)`);
  - (b) and (c) failing proves the sources are seen.
  - It cannot prove that the engine and C10 agree (see F4).

**Live cells** (`python3 $S/probe.py <wt> <db>`, 20 cells, every active parameter × each lens code on a live figure):
- 3×MOB: provisional 5 % ○ before → refused at HEAD. The refusal names OD-99, OD-100 and OD-92, as the ledger predicts.
- 12×MOB: ≤ 6000 mm ○ before and after.
- No other value, state or marker changed.
- `design_scale` changed on eight pending cells: five MOB cells (4, 5, 6, 9, 11) moved from universal to population; 3×d450, 3×A-EFFORT and 12×A-EFFORT moved from population to universal. This matches OD-48 (a), "whom it is for" (no identity; adjudication-3 §4).

**Reserved questions.** Nothing decides OD-92, OD-95, OD-99 Q1/Q2, OD-100 or Q3 for a shown value:
- no PROXY branch;
- no log read (`grep -n -i 'retrieval_log\|manifest' scripts/assess/assess_cell.py`);
- `derivation_sha`'s payload is unchanged and the label is bumped.

**OR-22b** (ledger 6183-6184, ANSWERED) says "The study's own band; migration 116's regulation-only rule (○) does not apply to it". OR-22 (4757) adds "not a regulation-only floor". So the changed R39 assertion (rso 0, ●) is warranted for its fixture, a floor claim confirmed by absence. T019-20's fixture change still kills its guard's mutation: with the lens clause removed from `_confirmed_bands`, it goes red on both trees (`$S/mut_f1.py`).

**The T-056 item 3a edit** is warranted by OD-48 (a). "The G1 line" alone would leave an ICF-keyed anchored cell reading `population`, a group it does not name.

## Findings

- **F1. The rso flip fires on a partial confirmation.**
  - Three VERIFIED T6 codes, one row confirmed by a T1 absence finding, no value shown, give `provisional ○ rso 0 T6-only(confirmed_by_study)` (`python3 $S/edge2.py` in wt-head).
  - The cause is the condition `any(confirmed[g] != bands[g])`. OR-22b covers a confirmed floor, and R39 says "one confirmed clause does not confirm the code".
  - Since T-056 item 3a, `regulatory_stratum_only` is the only home of "rests on codes". A cell that rests on codes would lose that flag, and `validate_evidence_state` line 282's "never stated" guard would lose it too.
  - No live cell is affected today: the live `confirms` edges join no parameter.
- **F2. T019-13 now skips refused cells.** It examines 16 of 17 pairs and drops 3×MOB, the only cell with a value (`grep T019-13 $S/head-test_assess_cell_pilot.txt`). The implementer's report does not list this edit. The links are computed before the refusal, so they could still be checked.
- **F3. Prose callers missing from the T-120 list.**
  - `governance/evidence-architecture.md:21` ("anchor at weak (○)").
  - `skills/run-pipeline_SKILL.md:403` and `:442`. Line 403 says to file a code-only cell that is not ○ as "an engine defect".
  - `workplan/pipeline-state-graph/IDEAL-GRAPH.md:411` (the old CHECK; in T-117 §5's caller scope).
  - Command: `git grep -n -E '(weak band|at ○|reads ○|never ●)' -- skills governance workplan/pipeline-state-graph`.
- **F4. Case A: the engine writes a cell its own gate fails.**
  - One UNVERIFIED T4 with no direction gives `provisional ○` with every governing source unverified (`python3 $S/edge.py`, case A), and C10 (ii) fails exactly that cell.
  - This is the status quo, kept by resolution decision 6. It does pick a circle for a wholly unverified basis, OD-99 Q1's ground, even though Q1 is literally worded for a shown value.
- **F5. The OD-92 refusal fires on any interval whose two bounds come from different sources** (case E). Its text, "several sources state the shown value", is inaccurate there.
- **F6. A cell keyed on `ALL` is written as `population`** (case I). OD-31 and OD-48 read `ALL` as universal. This is pre-existing, the T-056 items 1 to 3 residue.
- **F7. `band(3|4, grey)` stays ○.** It is "never displayed" only while grey never governs. If OD-97 (a) is answered, a no-value grey cell would show ○ through `floor_mean`, against OD-64. T4 grey has moved from ◐ to ○, with no live rows (`select tier, evidence_type, count(*) from evidence_sources where evidence_type='grey' group by 1,2`).
- **F8. T-117 §9 still says to stop if a value or state changes.** 3×MOB's state did change, as OD-92 and OD-99 Meanwhile require, but `d13caa4d` did not amend §9.
- **F9. C10, a blocking gate, now reads the retrieval log** through a cwd patch. With no manifest on disk, every non-VERIFIED T1 to T3 source fails. The subject is 0 today.

## Verdict

| Finding | Severity | Evidence |
|---|---|---|
| F1 rso and tier_basis flip on a partial confirmation | fix before PR | `python3 $S/edge2.py` |
| F2 T019-13 skips 3×MOB, unreported | fix before PR | `grep T019-13 $S/head-test_assess_cell_pilot.txt` |
| F3 four prose callers missing from the PR list | fix before PR (list them) | `git grep` above |
| F8 T-117 §9 stop condition not amended for the 3×MOB refusal | fix before PR | `sed -n '/## 9. Stop/,/## 10/p' workplan/.../T-117-marker-table-applied.md` |
| F4 engine ○ on an all-UNVERIFIED no-value cell; C10 fails it | note (coordinator) | `$S/edge.py` case A |
| F5 OD-92 wording on split bounds | note | case E |
| F6 `ALL` → population | note | case I |
| F7 grey band latent ○ | note | `band(3,'grey')` |
| F9 C10 depends on the log | note | `test_db_integrity.py` C10 |
| Migration, blob, sha chain, rebuild, AFTER_DATA | verified, no finding | `$S/cmp.py` |
| Red-then-green, OR-22b, T-056 item 3a edit, no log read, no PROXY branch | verified, no finding | `$S/red-on-main.txt` |

**What a finding would put in the book.**
- F1: a code-only cell stored as "confirmed by study", losing its only codes-only flag.
- F3: an auditor or pipeline operator filing correct ◐ markers as defects.
- F4 and F7: a circle on an unverified or grey basis, if the gate is ever bypassed or OD-97 is answered.

**Could not verify.** The preflight gate end to end: I ran no `--changed-from` battery, so I am relying on the implementer's 89/89. Whether OD-92's "stating sources" means bound-stating sources.
