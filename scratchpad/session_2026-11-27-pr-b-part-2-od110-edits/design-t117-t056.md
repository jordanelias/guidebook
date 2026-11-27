# PR B, tooling: T-117 (the marker table) and T-056 item 3a (`design_scale` from the key). Agonist's design

Agonist, 2026-11-27. Branch `claude/remediation-plan-orient-mjxms3`, head `c6e5ad6d` (`git log --oneline -1`), schema
`PRAGMA user_version` 167. **Design only.** The repository and `data/guidebook.db` were read only; sha256
`3d419efb…68edb9` before and after every probe (`sha256sum data/guidebook.db`). Engine runs used a scratch copy:
`/tmp/claude-0/-home-user-guidebook/943cc08d-9b18-5690-b0c6-54a354b936e3/scratchpad/probe/p.db`, probe script `probe.py`
beside it (read-only connection; it runs `determine()` on every live lens cell and tags each governing source).
Rule 7a: every figure below sits beside the command that derives it. Re-run; do not trust.

**Inputs re-used, not re-derived:** `scratchpad/session_2026-11-26-governance-reconciliation/prb/prb-design-1.md` §1 and §3
(cited "D1 §n"), as corrected by `prb-antagonist-1.md` (cited "A1 Dn/On"). Binding: A1's SPLIT (no `worse_at`, no harm
reader) and A1 D1 (OR-23/OR-23b are rules for **unretrievable** sources, not unverified ones).

**Scope (verified against the ledger, not trusted from the brief).**
- In: T-117 as narrowed by OD-110 (`grep -n -F 'OD-110 STATUS:' references/project-standards.md`) and OD-98; T-056 item 3a only.
- Out: the T-059 selection slice and the eligibility union (OD-110 "What waits"; OD-101 "This waits with the T-059 slice");
  the harm record (OD-102); PROXY-thin and the `population_match` parent extension (OD-98, last bullet); T-056 items 1-5
  except 3a; every governance/skill/atom prose row (T-120 follows this task, OD-110).
- Interim only, never decided: OD-92 and OD-99 (both `REFERRED BACK TO THE OWNER`; their "Meanwhile" bullets are the
  rule built here), OD-100 (its "Meanwhile: (a)").
- Gate (T-117 §2's function, extended by me to the interim ids): OD-31, OD-48, OD-57, OD-59, OD-64 print
  `OPEN (owner)`; OD-95, OD-98, OD-110 print `OPEN (delegated; confirmed with corrections applied)`; OD-92, OD-99, OD-100
  print `CLOSED (… REFERRED BACK TO THE OWNER)`, which is why the engine refuses on them rather than builds them.
- Check: `for n in OD-31 OD-48 OD-57 OD-59 OD-64 OD-92 OD-95 OD-98 OD-99 OD-100 OD-110; do gate $n; done` with `gate()` from T-117 §2.

---

## 0. The probe: what reaches the book today, and what this PR changes

`python3 <scratch>/probe/probe.py <scratch>/probe/p.db` (needs cwd-independent `retrieval_log.LOG_ROOT`; the script
`chdir`s to the repository, because `LOG_ROOT` is the relative path `retrieval-log`: `grep -n '^LOG_ROOT' scripts/research/retrieval_log.py`).

**Every live lens cell** (`select distinct … from extraction_lens_links join source_value_extractions …`, in the probe):
only 3×MOB and 12×MOB compose a value; every other cell is `pending`. WHEEL has no row in `base_taxonomy_identity`
(`select identity_code from base_taxonomy_identity where identity_code='WHEEL'` prints nothing), so OD-91's first
cells cannot be probed until T-102; MOB stands in.

| cell | today (engine, quoted) | stating rows of the unconditioned headline (probe) | after this PR (derived) |
|---|---|---|---|
| 3×MOB | provisional, ≤ 5 %, `○`, `universal`, rso 0, proxy 1 | 25 REF-00992 T6 VERIFIED; **28 REF-00994 T4 UNVERIFIED, retrieved**; 30 REF-00995 T6 VERIFIED | **Refusal naming OD-99 (Q1)** (REF-00994 states the value and is retrieved-UNVERIFIED) and OD-92 (marks {○, ?, ○}); nothing written. REF-00997 (T5, no logged retrieval, `standard_number` NULL) would also be excluded, naming OD-100. |
| 12×MOB | provisional, ≤ 6000 mm, `○`, `universal`, rso 1 | 116 REF-00988 T5 VERIFIED | provisional, ≤ 6000 mm, **`○` by the table** (T5 → ○) instead of by the override, **`population`**. REF-01016 (T6, UNVERIFIED, retrieved, not stating) stays governing (OD-99 Meanwhile, first bullet). C10 passes. |
| 4, 5, 6, 9, 11 × MOB | pending, `universal`, rso 1 | — | pending; `design_scale` → `population`. No other field. |
| every other cell | pending, `population` | — | unchanged |

Retrieval standing of the non-VERIFIED sources (OD-99 Q2 (b): no logged retrieval, or `verification_method` in the two
not-retrieved values): `python3 -c` over `retrieval_log.manifest_lines_for(ref,url,doi)` for
`verification_status<>'VERIFIED'` gives REF-00997 0 lines (unretrieved), REF-01002 lines but method
`corroborated-not-retrieved` (unretrieved by (b)), and every other one ≥ 1 line with method `tool` or NULL (retrieved).
The two method values are members of the column's CHECK (`dbcore.check_values(conn,'evidence_sources','verification_method')`).

**The 8 `specifications` rows.** All are parameter 3 × MOB and all retired (`select count(*), sum(retired_at is null)
from specifications` prints `(8, 0)`); every marker is NULL. The rebuild copies them unchanged: NULL passes the new
CHECK, and no live row is re-run (re-assessing is research, rule 10). Re-running their key would now refuse (row above),
so none is superseded by this PR. 12×MOB has no `specifications` row at all.

**Today's two gates on a would-be live row.** The CHECK refuses `⚠` and refuses `◐` with rso 1
(`select sql from sqlite_master where name='specifications'`, the `marker` CHECK); C10 refuses any non-VERIFIED
governing source (`grep -n -F 'no published cell rests on an unverified' scripts/tests/test_db_integrity.py`), so the
12×MOB row would fail C10 today on REF-01016 (D1 §0, quoted rc=1).

Check: re-run the probe; `sha256sum data/guidebook.db` unchanged.

---

## 1. The smallest change, per file (delete first; CLAUDE.md §8 order)

Do-nothing is refused: the ruled table (`governance/tier-system.md` §5, lines 66-79) is already doctrine and the code
contradicts it (§0). Each piece names what wrong thing reaches the guidebook without it.

**1.1 `schemas/tier_derivation.py` `band()`** (D1 §1.3 item 1, survived A1). Delete the T3 type split. Tier 1-2 FULL,
3-4 PARTIAL, 5-6 WEAK; docstring: a grey basis is marked ⚠ by the engine, never by a circle (OD-64). Co-1/Co-2 are
tiers 1/2 in `TIER_MAP`, so no list is typed. *Without it:* T3 clinical shows ● and T5 ◐.

**1.2 `schemas/enums.py` `EvidenceMarker`** (D1 §1.3 item 2; A1 Phase 1 (d)1). Add `WARNING = "⚠"`; `ordinal`
counts circles only, `WARNING.ordinal` raises; correct the `WEAK` comment ("grey … not retrieved" is false). `floor_mean`
iterates circles only. *Without it:* a fourth member renumbers ● from 3 to 4 (`ordinal = len(EvidenceMarker) - index`,
`sed -n 96,98p schemas/enums.py`), breaking the 2026-09-13 derived-figure rule (tier-system.md:78).

**1.3 `scripts/dbcore.py`: two predicates, one home for engine and C10** (A1 D1 scope; OD-99 Meanwhile).
- `not_retrieved(conn, ref_id) -> bool`: the source is not VERIFIED **and** (`retrieval_log.manifest_lines_for(ref, url,
  doi)` is empty **or** `verification_method` is one of the two OD-99 Q2 (b) values). Lazy import of `retrieval_log`, as
  `db.py` does (`grep -n '_retrieval_log()' scripts/db.py | head -2`). The two values are asserted to be members of
  `check_values(...)`, never trusted.
- `route_shown(conn, ref_id, parameter_id) -> bool | None`: for `tier >= REGULATORY_FROM_TIER` (OR-23b): `jurisdiction`
  and `standard_number` non-NULL and every live value-supplying row (`VALUE_SUPPLYING_ROLES`) of the source for the
  parameter carries `clause_id` or a `loc_*` column (names read by PRAGMA). Titles are never parsed (OD-99 Meanwhile, 4th
  bullet). For T1-T3: returns `None`, "not settled" (OD-95: "settled then, or put to the owner").
- *Without them:* the engine and C10 would each carry a copy of "could not be retrieved" (rule 5), and REF-00997 would
  govern 3×MOB though OD-100's interim says it does not.

**1.4 `scripts/assess/assess_cell.py` `determine`.**
- (a) **Exclusion before `classify`** (OD-99 Meanwhile, 3rd bullet; OD-100 Meanwhile (a)): a source with
  `not_retrieved` and `route_shown is False` is dropped from `recs`, still counted in `has_unverified_sources`, and each
  of its rows is linked `excluded` with a reason naming OD-100. A source with `not_retrieved` and `route_shown is None`
  (T1-T3) raises `Refusal` naming OD-95 and OD-99 (Q2). *Live reach:* REF-00997 on parameter 3; REF-01002 is gathered by
  no composing cell (probe).
- (b) **Delete the regulatory-only override** (`if regulatory_stratum_only: source_bands = []`) and correct the comment
  block above it ("Option A section 2.3 … weak"). *Without it:* a T4-only cell shows ○ (owner: ◐, 7195).
- (c) **The marker of the value (OD-59).** `compose_value`/`_compose_headline` return, as a sixth element, the
  extraction ids of unconditioned headline rows whose bound equals a selected bound (D1 §1.3 item 4). Then:
  ```
  def own(ref):                                   # tier-system §5, one source
      r = by_ref[ref]
      if r["evidence_type"] == EvidenceType.GREY.value: return WARNING            # OD-64
      if r["verification_status"] != "VERIFIED":
          return WARNING if not_retrieved(conn, ref) else None                     # routed-unretrieved ⚠ (4540, 7053, tier-system:77); retrieved-UNVERIFIED: OD-99 Q1
      return confirmed.get(ref) or band(r["tier"], r["evidence_type"])
  basis = stating_refs if value_shown else governing           # no value shown: the cell's set (R7), as today
  marks = {ref: own(ref) for ref in basis}
  if value_shown and not stating_refs: raise AssertionError    # engine defect: a shown bound no row states (see thin, below)
  if None in marks.values(): raise Refusal("OD-99 … <refs> …")  # text below
  if value_shown and len(set(marks.values())) > 1: raise Refusal("OD-92 … <ref: mark> …")
  if not value_shown and WARNING in marks.values() and len(set(marks.values())) > 1: raise Refusal("OD-92 …")
  marker = (next(iter(marks.values())) if value_shown else
            WARNING if set(marks.values()) == {WARNING} else floor_mean(marks.values()))
  ```
  Refusal texts (findable by id: `grep -n -F 'OD-99' scripts/assess/assess_cell.py`):
  - `"OD-99 (referred to the owner, Question 1): <REF-…> states the shown value and was retrieved but is stored
    UNVERIFIED; whether its value carries ⚠ or its tier's circle is the owner's to say. Nothing written."`
  - `"OD-92 (referred to the owner): several sources state the shown value with different markers (<REF: glyph>, …);
    which marker the value carries is the owner's to say. Nothing written."`
  - `"OD-95 / OD-99 (Question 2): <REF-…> could not be retrieved and is T1-T3; what counts as its academic route is
    unsettled. Nothing written."`
  *Without it:* the marker is the floor mean of every governing source (OD-59 rejected that, 7273/7333), and a value
  read off a retrieved-UNVERIFIED source shows a circle no ruling gives it.
- (d) **`_confirmed_bands`** (D1 §1.3 item 5, survived A1): an unconfirmed row takes its source's own band, not WEAK; it
  is called for every stated/provisional cell, not only proxy cells (OR-22b, 6183). *Live reach:* nil; every `confirms`
  edge has a label referent (`select relation_id,to_extraction_id,to_label is not null from extraction_relations where
  relation='confirms'` prints three rows, `to_extraction_id` NULL).
- (e) **rso under confirmation** (A1 D4): when the stating source's mark comes from `confirmed` (a study's band), set
  `regulatory_stratum_only = 0`, as the proxy branch already does for a basis no longer purely regulatory. One line. Keeps
  the CHECK's `●` guard (§3) satisfiable in the one owner-ruled state that would otherwise hit it.
- (f) **Thin: no new branch.** The ruled causes are the project's own inference (7123) and a value that mixes a finding
  with a project inference (7159); OD-98 narrows both to "only when no source in the lens states it". Not causes:
  `rests_on_proxy_inference` by itself (OD-98 heading), a PROXY grade (Q3, `grep -n -F 'Whether any PROXY grade makes a
  value thin' references/project-standards.md`, 7093). The engine shows only bounds that a governing row states
  (`_compose_headline` takes `min`/`max` over row bounds; `sed -n 895,905p scripts/assess/assess_cell.py`), so the ruled
  cause is unreachable today; the `AssertionError` above makes the invariant loud instead of building a dead branch.
  The proxy-branch string (`grep -n -F 'most-accommodatingly within what the' scripts/assess/assess_cell.py`) is reworded
  to state no thin verdict.
- (g) **T-056 item 3a.** `design_scale = SCALE_POPULATION if lens.get("identity_code") else SCALE_UNIVERSAL`, set once
  before the cascade; delete the G1 line (`grep -n 'design_scale = SCALE_UNIVERSAL' scripts/assess/assess_cell.py`); correct
  the G1 header line (`grep -n 'G1  T4' scripts/assess/assess_cell.py`). "Rests on codes" stays read from
  `regulatory_stratum_only`; no code reader reads it from `design_scale`
  (`git grep -n -E 'design_scale|SCALE_UNIVERSAL' -- scripts schemas ':!scripts/migrations' ':!scripts/tests'`: vocabulary
  validators, the graph extractor, the writer). *Without it:* a wheelchair user's cell says it is for everyone (OD-48, 7995).
- (h) `RULE_VERSION` `pilot-8` → `pilot-9`, one comment line. The sha payload format is unchanged.

**1.5 `schemas/directness.py:51`** comment "universal / code-compliant" → "names no group (OD-48)". Comment only.

**1.6 `scripts/tests/test_db_integrity.py` C10** (OD-99 Meanwhile, last bullet, verbatim scope). Subject unchanged
(live stated/provisional cells). Fails a cell when (i) a governing source has `dbcore.not_retrieved` and
`dbcore.route_shown` is not True, or (ii) every governing source is non-VERIFIED or grey and the marker is a circle.
Delete the VERIFIED-only clause. *Without it:* the only composing cell that needs no owner answer (12×MOB) cannot be
published, and a route-less unretrieved source could be.

**Deleted:** the override; the T3 split; the WEAK default in `_confirmed_bands`; the proxy-only guard on it; the G1
`design_scale` line; C10's VERIFIED-only clause; the CHECK's `marker = '○'` clause. **Not built:** route for T1-T3,
PROXY-thin, the parent match, `worse_at`, the union.

Size (reasoned, [UNVERIFIED] until built): `git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'`
expected near +150/−45 excluding tests.

Check: `git grep -n -F 'source_bands = []' scripts/assess/assess_cell.py` prints nothing after; `git grep -n -E "OD-(92|95|99|100)" scripts/assess/assess_cell.py` prints the four texts.

---

## 2. Red tests, written first

`scripts/tests/test_assess_cell_pilot.py` (prefix free: `git grep -c -E 'T117-|T056-' -- scripts/tests` prints nothing);
fixtures from `synth_db`, which must gain `url`, `doi`, `verification_method`, `standard_number` on `evidence_sources` and
`clause_id`, `loc_clause` on `source_value_extractions` (a fixture laxer than the schema is its own warning, `sed -n 59,90p`);
retrieval through `scripts/tests/_fixture_log.py` `fixture_log_root` with `GUIDEBOOK_RETRIEVAL_LOG` set, as
`test_db_amend_writers.py:96` does. Each line: fixture → assertion → **red on today's code because**.

| id | fixture → assertion | red because / kills |
|---|---|---|
| T117-01 | one T4 VERIFIED `standard_eb` states 1:12 → `◐` | today `○` (override) |
| T117-02 | `band(5,"national_fw") is WEAK` (unit) | today PARTIAL; engine-level T5-only is masked by the override (A1 agrees), so the unit test is the red one |
| T117-03 | `band(3,"clinical") is PARTIAL`; `own()` on a grey source returns `"⚠"` and `"️" not in` it | today FULL; grey path absent. Engine-level grey is unreachable until the T-059 slice (T3 grey never governs: `grep -n 'elif b\["t3g"\]' scripts/assess/assess_cell.py`) |
| T117-04 | T4 UNVERIFIED, no logged retrieval, `jurisdiction`+`standard_number`+`loc_clause` set, states the value alone → `⚠`. Same without `standard_number` → excluded, reason contains `OD-100`, cell `pending` | today `○` and it governs |
| T117-05 | migration DDL via `try_row`: live `⚠` accepted; `◐` rso 1 accepted; `●` rso 1 refused; `"⚠️"` refused | first two refused today; last two are guards that kill "drop the ● clause" and "accept the emoji form" |
| T117-06 | OD-59 within one stratum: T4 VERIFIED states 1:20, T6 VERIFIED states 1:12, `lower_is_better` → value 5 %, `◐` | today `○` (override); the mutation "floor mean over governing" gives `○` (floor((2+1)/2)=1) |
| T117-07 | OD-99: T6 UNVERIFIED **with** a fixture manifest line states the value alone → `Refusal`, text contains `OD-99` | today `○` |
| T117-08 | OD-92: T4 VERIFIED and T6 VERIFIED both state 1:20 → `Refusal`, text contains `OD-92` | today `○` |
| T117-09 | guard: T6 VERIFIED states the value; T6 UNVERIFIED-retrieved governs, states 1:12 → no refusal, `○`, the second ref in `governing_refs` | kills "refuse on any unverified governing" and "drop retrieved-UNVERIFIED" |
| T117-10 | anchored cell: T1 UNVERIFIED, `verification_method='corroborated-not-retrieved'` → `Refusal` containing `OD-95` | today `stated` with it anchoring |
| T117-11 | C10 on a temp copy of the live DB, one seeded live cell each: (a) retrieved-UNVERIFIED governing, verified stating, `○` → pass; (b) unretrieved, no `standard_number` → fail; (c) all governing non-VERIFIED under `○` → fail; (d) unretrieved with route, sole governing, `⚠` → pass | (a) and (d) fail today; (b), (c) guards |
| T117-12 | `[m.ordinal for m in (FULL,PARTIAL,WEAK)] == [3,2,1]`; `WARNING.ordinal` raises; `floor_mean` of the five 2026-09-13 rows unchanged | `WARNING` absent today; kills "WARNING as an ordinary member" |
| T056-01 | G1 cell at `MOB` → `population` | today `universal` |
| T056-02 | anchored, `d450` only → `universal` | today `population` |
| T056-03/04 | G1 `d450` only → `universal`; anchored `MOB` → `population` | guards |

Existing assertions that flip (callers, edited in the PR; locate by text): `grep -n -E "T6-only => design_scale universal|T3-clinical alone is provisional and still full|source with no recorded verification|stated cell resting on an unverified source|lends only the weak band" scripts/tests/test_assess_cell_pilot.py`.
The 5-tuple unpack: `git grep -n 'compose_value(' -- scripts/tests`.

Seeded defects, each must be KILLED: `band()` T4 → WEAK (T117-01); override restored (T117-01); `⚠` with U+FE0F
(T117-03, T117-05); `own()` → floor mean over governing (T117-06); OD-99 branch returns `WARNING` instead of refusing
(T117-07); OD-92 branch takes the best circle (T117-08, and this is OD-92 option (a) being decided by code).

**Dropped from the T-117 file, because a ruling makes them unbuildable:** T117-04's PROXY clause and all of T117-08
(PROXY-thin, `population_match` parent; OD-98); T117-07 as written ("⚠ passes C10"; OD-99 Meanwhile replaces it);
T117-06 as written (T1 + T6: the cascade never lets T6 govern beside an anchor, `grep -n -A3 'if anchors:'
scripts/assess/assess_cell.py`, so the fixture cannot exist without the T-059 slice).

Check: run each new case on the unchanged tree and see it red, then the after-run green; the whole file green.

---

## 3. The migration

`scripts/migrations/168_marker_table.sql` (number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` is
`167_…`, plus one; free on every ref: `git log --all --format=%h --name-only -- 'scripts/migrations/168_*'` prints
nothing). Ends `PRAGMA user_version = 168`.

**The CHECK:** `marker IS NULL OR (marker IN ('●','◐','○','⚠') AND (regulatory_stratum_only = 0 OR marker <> '●'))`
(T-117 item 5 as written; A1 D4 restores the guard that D1 dropped). The live⇔marker CHECK and the lens CHECK unchanged.

**Rebuild recipe:** migration 114's (`scripts/migrations/114_extraction_slug_and_root.sql`), generated from the live DDL
with the one substitution; never hand-typed. The object list is derived, not typed:
- views, transitive closure over `sqlite_master` of views whose SQL names `specifications` (regex `\b<name>\b`, iterate to
  fixpoint): today `v_best_practice, v_determination_provenance, v_divergence, v_gap_subject, v_item_provenance,
  v_pending, v_source_reach_all`;
- `select name from sqlite_master where type in ('index','trigger') and tbl_name='specifications'`: today
  `idx_spec_row_identity, idx_spec_retired, trg_spec_retire_needs_reason`;
- inbound FKs, `PRAGMA foreign_key_list` over every table where the target is `specifications`: today
  `specification_source_links`, `specification_extraction_links`, and the self-reference. `determination_gates` matches a
  `like '%specifications%'` search but has no such key (A1 D6); the `like` search is not the rebuild list.
- sequence: carried by `SELECT` from the old row, never a literal (076's error, A1 Phase 1 (d)5).
- Order: drop the view closure; `CREATE TABLE "_168_new_specifications"`; `INSERT … SELECT` by column name; drop old;
  rename new (never rename-old); recreate indexes, trigger, views from stored SQL; restore sequence; then
  `PRAGMA foreign_key_check` prints nothing (`migrate_db.py` turns keys off outside the transaction:
  `grep -n -i 'foreign_keys' scripts/migrate_db.py`).

**No `-- AFTER_DATA:` marker** (corrects T-117 item 5's "required"; D1 §1.5 and A1 row 6 agree). The CHECK only widens
on the copied rows (all NULL markers), no column is renamed or dropped, and the last data migration writing
`specifications` precedes the last marker:
`for f in scripts/migrations/data_*.sql; do grep -qiE '(INSERT INTO|UPDATE|DELETE FROM) +"?specifications\b' $f && basename $f; done | sort | tail -1`
(today `data_20260918201549…`) against `grep -h '^-- AFTER_DATA:' scripts/migrations/*.sql | sort -u | tail -1`
(today `20261106053823`).

Check: `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"`; `python3 scripts/audit/migration_reproducibility.py --deep`;
the CLAUDE.md §4 UNWRITABLE derivation prints no new line; `python3 scripts/generate/context_map.py`.

---

## 4. Caller sweep (rule 4)

Names: `band(`, `EvidenceMarker`, `floor_mean`, `_confirmed_bands`, `compose_value`, `regulatory_stratum_only`, `marker`,
`design_scale`, `SCALE_UNIVERSAL`, `○`, `⚠`, `weak band`, `C10`, `not_retrieved`, `route_shown`. Per name, T-117 §5's
four commands (code `git grep`; `sqlite_master like`; registry; prose `git grep` over governance, architecture,
CLAUDE.md, references, `workplan/pipeline-state-graph`), plus `grep -r` for `.ignore`d trees when a ruling is sought.

- **Views/triggers:** none reads `marker` or `design_scale` (`select name from sqlite_master where type='view' and sql like '%marker%'`
  and the same for `design_scale`). `v_item_provenance` names `regulatory_stratum_only`; it is recreated verbatim. A 0-row
  view is unproven: re-select each recreated view on the rebuilt copy and diff against the canonical.
- **Registry:** `test_db_integrity` (blocking; C10), `test_assess_cell_pilot` (advisory), `derivation_handshake_integrity`
  (advisory; reads the stored marker via `stale_determinations`), `migration_reproducibility`, `schema_reference_audit`
  (blocking): `python3 -c "import yaml;[print(c['id'],c.get('level')) for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if c['id'] in (…)]"`.
  `run_checks.py --selftest` after.
- **Code comments made false, fixed here** (prose callers inside `scripts/`, A1 O3): `grep -n -F 'shown ○' scripts/db.py scripts/research/retrieval_log.py`;
  `grep -n -F "renders ○" scripts/audit/research_batch_dod.py`; `grep -n -F 'weak band' scripts/assess/assess_cell.py scripts/tests/test_assess_cell_pilot.py`.
- **Tests:** `git grep -l -w marker -- scripts/tests`; `git grep -n 'compose_value(' -- scripts`; `synth_db` columns (§2).
- **Prose and atoms, listed for T-120, not edited** (T-117 item 6; OD-110 puts T-120 after this task; OD-111 makes the
  `design_scale` ones superseded on contact):
  `git grep -n -E '○.{0,60}(grey|thin|unverified|retriev)|weak band' -- governance skills architecture`
  (today: `owner-browser.yaml` 111/807/830/858, `mission-and-epistemics.md` 42/136, `held-tensions.md` 308,
  `evidence-auditor_SKILL.md` 45-56, `run-pipeline_SKILL.md` 399, `voice-style_SKILL.md` 121-122);
  `design_scale` as code-only basis: `governance/evidence-methodology.md:144`, `governance/evidence-architecture.md:121`,
  atom EVI-331 (`grep -n EVI-331 workplan/pipeline-state-graph/ATOMS.tsv`); old-marker atoms EVI-062, EVI-141 (A1 O2).
  `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after; report the difference.
- **One departure for the coordinator:** `governance/tier-system.md:81` ("Until T-117 lands …") is made false by this PR
  alone. T-117 item 6 forbids governance edits; I recommend deleting that one line here (no attestation needed for
  `governance/`) and record it as the only exception. Not decided by me.

Check: the four commands per name, before and after; each hit judged caller or mention in the PR body.

---

## 5. Dead after

Deleted in the PR (§1 list). Still read, so kept: `floor_mean` (no-value cells under R7; `_confirmed_bands`;
derived figures, tier-system.md:78); `has_unverified_sources`; `_verified` (C10 reasoning and `_confirmed_bands`'s
confirmer filter). Made dead and **not** deleted here: none found. `grey_flag`/`grey_reason` remain a duplicate home of
grey (T-117 item 4; OI-67), read by nothing this PR adds.

Check: `git grep -n -w -E 'floor_mean|_verified' -- scripts schemas` shows a caller for each kept name.

---

## 6. Stop conditions

- The gate (scope block) changes: any of OD-31/48/57/59/64 not `OPEN (owner)`; OD-98 or OD-110 not confirmed; OD-92,
  OD-99 or OD-100 answered (then build the answer, not the refusal, and drop T117-07/08 or T117-04's exclusion as the
  answer requires).
- T-117 item 4 or tests T117-04/T117-08 are not corrected in the task file to OD-98 before build (the ledger governs; the
  file is owed the edit, OD-90..113 ACTION (1)).
- The live-data comparison shows any change beyond §0's table: a value, a state other than 3×MOB's refusal, or a marker
  on a cell other than 12×MOB.
- The stating set of a composing cell differs from §0 after a unit-string data fix (A1 D5: rows that state the value in
  prose but do not parse): list per cell the governing rows whose `claimed_value` names the selected bound but whose
  `bound_on_scale` is None; non-empty is reported, not absorbed.
- `--rebuild` or `--deep` differs; UNWRITABLE prints a new line; a check green before is red after.
- Deriving any cause needs a list beside a column (rule 8). The two OD-99 Q2 (b) method values are the exception: an
  owner question's interim text, checked against the CHECK, deleted when answered.

---

## 7. Open owner inputs I do not decide

- **OD-92** (several stating sources, different markers): refused meanwhile. Blocks 3×MOB.
- **OD-99 Q1** (retrieved-but-UNVERIFIED stating source: ⚠ or circle): refused meanwhile. Blocks 3×MOB (row 28).
- **OD-99 Q2** (how "could not be retrieved" is recorded): interim (b) built in `dbcore.not_retrieved`.
- **OD-100** (an unretrievable route-less source governing, ⚠): excluded meanwhile. Reaches REF-00997.
- **OD-95** (what an academic route is, for T1-T3): refused when live; no live reach.
- **Q3** (PROXY → thin): not built (OD-98). Reach: every PROXY row is MOB-targeted
  (`select target_population, match_grade, count(*) from evidence_population_match group by 1,2`).
- **OD-96/OD-97** (code-only below richness; grey-only): such cells stay `pending`; untouched.
- **ALL as an identity** (OD-31; T-056 items 1-3, T-115): with 3a alone, a cell keyed `identity_code='ALL'` stores
  `population`, which is today's value for those cells too (probe: 4×ALL … 11×ALL `population`); not changed here.
- Coordinator (not owner): the T-117 file defects in §2 "Dropped" and §6; the tier-system.md:81 departure (§4).

---

## 8. The agonist's case (numbered claims for the antagonist)

1. **After this PR, 12×MOB is the one composing cell that publishes with no owner answer: provisional, ≤ 6000 mm, `○`,
   `population`, C10 green.** Evidence: probe row 12×MOB (stating 116, REF-00988 T5 VERIFIED; band after = WEAK);
   REF-01016 retrieved (≥ 1 manifest line), so OD-99 Meanwhile bullet 1 keeps it and C10 (i) does not fire.
   Falsified if: a second stating row parses after a unit fix with a different mark (then OD-92 fires); or REF-01016's
   manifest lines are index records only.
2. **3×MOB is refused, naming OD-99 and OD-92, and nothing is written.** Evidence: stating rows 25/28/30; REF-00994
   UNVERIFIED with 3 manifest lines and method `tool`; OD-92 and OD-99 both name 3×MOB as blocked. Falsified if:
   REF-00994 fails OD-99 Q2 (b) (then it is unretrieved; route False → excluded, marks {○, ○} → `○`).
3. **Thin needs no new branch: the ruled causes are unreachable by construction.** Evidence: OD-98 first bullet; 7123,
   7159; `_compose_headline` selects bounds only from governing rows. Falsified if: a path exists where a shown bound
   is stated by no in-lens row (unit conversion is shown as a notation, not a new bound: `grep -n 'MARK_UNROUNDED' scripts/assess/assess_cell.py`).
4. **The interim refusal is the only way to honour "Meanwhile: the engine refuses the cell" without deciding OD-92 or
   OD-99 Q1.** Any marker written for those cases picks an option ((a)/(b)). Evidence: OD-92 options; OD-99 Q1 options.
5. **The refusal for an unretrieved T1-T3 source (OD-95) is in scope and decides nothing.** OD-99's interim excludes a
   source "that fails it and has no route"; for T1-T3 "has no route" is undecidable (OD-95). Excluding would decide that
   `corroborated-not-retrieved` is not a route; including would decide it is. Falsified if: OD-95's "Meanwhile, a
   route-less unretrievable T1 to T3 source does not anchor" is read as making every unretrieved T1-T3 route-less.
   **[CONFIDENCE: medium; riskiest-3.]**
6. **One home for "could not be retrieved": `dbcore`, read by engine and C10.** Evidence: C10 already imports `dbcore`
   (`sed -n 40p scripts/tests/test_db_integrity.py`) and not `assess_cell`; `manifest_lines_for` is already "one home"
   for VERIFIED (`sed -n 2302,2307p scripts/research/retrieval_log.py`). Cost: the engine now reads the filesystem log, so
   the marker depends on files `derivation_sha` does not hash; the engine already declares the marker "A CACHE over …
   how sources [are] verified" (`grep -n -F 'THE MARKER IS A CACHE' scripts/assess/assess_cell.py`). **[riskiest-2]**
7. **Keep T-117's `●` guard in the CHECK; set rso 0 when a confirming band is used.** Evidence: A1 D4; OR-22b 6183;
   proxy branch precedent (probe: 3×MOB rso 0, proxy 1). Falsified if: rso is read as "governing set is regulatory"
   by a reader that must stay 1 under confirmation (`git grep -n regulatory_stratum_only -- scripts`).
8. **No `AFTER_DATA` marker; 168 is free; the rebuild list is the closure in §3.** Evidence: the two loops in §3; A1 row 6.
9. **T-056 3a changes `design_scale` on six MOB cells and nothing else, and no code reader breaks.** Evidence: probe (3,
   4, 5, 6, 9, 11, 12 × MOB are `universal` today; 3 is refused after, so six rows change); the `git grep` in §1.4(g).
   The prose readers (evidence-methodology:144, evidence-architecture:121, EVI-331) are superseded by OD-111 and listed
   for T-120. Falsified if: a render contract reads `universal` as code-only (`grep -n design_scale governance/pipeline-contract.yaml`).
10. **The no-value branch keeps R7 (floor mean over governing) and refuses on mixed ⚠/circle (OD-92).** No live cell
    reaches it (probe: every composing cell shows a value). **[riskiest-1: it extends OD-92 from "stating sources" to a
    no-value governing set, and 7059 is the only text for that.]** Falsified if: the ledger rules the no-value marker.
11. **The grey arm of `own()` is read only after the T-059 slice; it is one condition from a ruled table and is tested at
    unit level.** Evidence: T3 grey never governs today (`elif b["t3g"]`). Falsified if: a T4-T6 source can carry
    `evidence_type='grey'` (`select tier, evidence_type, count(*) from evidence_sources group by 1,2` shows none).
12. **Four statements in the T-117 file are made unbuildable by rulings:** item 4's PROXY and `rests_on_proxy_inference`
    causes and the parent match (OD-98); item 4a / T117-07 "⚠ passes C10" (OD-99 Meanwhile); T117-08 (OD-98);
    T117-06's T1+T6 fixture (cascade, no slice). Item 5's "AFTER_DATA required" is false (§3). T-117 §2 was revised;
    item 4 was not. Evidence: `sed -n 66,67p` and `sed -n 102,106p` of the task file against OD-98/OD-99.

[UNVERIFIED]: `synth_db`'s extension shape; the `run_checks` accessor C10's test uses; size; that `fixture_log_root`
accepts a ref-tagged line for an arbitrary fixture ref.
