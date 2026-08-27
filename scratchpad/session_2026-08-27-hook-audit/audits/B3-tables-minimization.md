# B3 — Tables, minimization, and the §1 burden of proof (adversarial)

Subject: `scratchpad/session_2026-08-27-hook-audit/WALKABILITY-PLAN.md`, esp. Parts 6.6 and 9.5,
read in full (1117 lines), against `NOMENCLATURE.md` Parts E/I/J/K/L, A2-W3, A4-B9, and
`CLAUDE.md` §1 and rule 4. Every figure below measured this session against `data/guidebook.db`
read-only (base reproduces: **66 tables, 33 zero-row, 18 views**) and the non-archived tree.
Convention for "caller": `grep -rlw <table>` over `scripts tools skills governance schemas
.github .claude`, excluding `_archived`, `__pycache__`, `skills/deprecated/` — `grep -r`, not
ripgrep, per rule 4b. Re-derivation commands inline.

---

## 1 · BLOCKER — Tier 1 `situations` is a doctrinal Co-1 entity; deleting it is owner-gated content, not agent-evidenced apparatus

The ground given ("0 rows, no writer") is true for executable writers (sweep:
`grep -rlw situations scripts tools skills schemas` → only `057_baseline`). But `situations` is
not apparatus:

- `governance/functional-taxonomy.md:324` — *"First-person accounts → situations"*; `:97` — the
  `situations` entity and Co-1 testimony are *"never subordinated"*.
- `governance/held-tensions.md:363` — *"situations rendered beside specifications"* — a **book
  surface**, stated in doctrine.
- The table's own DDL carries `co1_status` and `operational_access` — *"marks broken-lift-class
  evidence (doctrine §5.5)"*.

§1's own carve-out: *"Owner sign-off is still required for content and doctrine: … evidence-tier
definitions … work-product inclusion."* The structured home of Co-1 testimony is exactly that
class. **Failure scenario:** the table is deleted on agent evidence; when Co-1 situation accounts
arrive, they land in prose notes or nowhere — in the project's own words, erasing Co-1 structure
is *"the worst failure available here."*
**Smallest fix:** move `situations` out of Tier 1 into an owner-gated line ("delete only on owner
sign-off; doctrine names it"), one row edit in 9.5.

## 2 · BLOCKER — Tier 1 `connections`/`connection_targets`: the fold target does not exist in the counted design, and the table feeds a book part today

The ground is "design fold (J.2/K.4): a comparative synthesis-item or derivable". But:

- The fold target is `syn_items.kind='connection'` **plus `syn_synthesis_links`** (J.2's own
  shape: "their targets in `syn_synthesis_links`"). 9.5's create list is `jud_items`,
  `syn_judgment_links`, `spe_synthesis_links`, `figures` — **`syn_synthesis_links` is absent**,
  deferred by §6.6's own note ("48 if `syn_synthesis_links` is deferred with comparative
  synthesis"). Deleting a table on the ground that it *becomes* X, while deferring X, is deletion
  with no successor.
- `connections` is not writer-less: `scripts/db.py` has full CRUD (`INSERT INTO connections`
  :113, `connection_targets` :117, update :129, delete :692–693, `next-id connections`), and
  `log-mining` merges `connections_produced` (:225–255). `scripts/generate_parts.py:245–257`
  **builds Part 5 of the book from `connections`** (existence-guarded, so the drop won't crash —
  it will silently empty a book part, the §2(a) shape). Plus `schemas/connection.py`,
  `validate_cross_refs.py`, `audit_consolidator.py`, graph audits, **11 skills**, registry and
  retired-vocabulary entries. Command:
  `grep -rlw connections scripts tools skills governance schemas | grep -v _archived`.

**Failure scenario:** Tier 1 executes "now"; Part 5's data source and the mining-yield write path
vanish; the comparative-synthesis replacement never lands because it was deferred.
**Smallest fix:** re-tier as "fold in the same commit that creates `syn_items.kind` +
`syn_synthesis_links`" and add `syn_synthesis_links` (+1) to the arithmetic — range becomes 53–64,
or `connections` leaves Tier 1.

## 3 · MAJOR — `reference_stubs` "no writer" is false; the drop collides with two committed data migrations; and the true ground is stronger than the one given

`grep -lE '(INTO|UPDATE|FROM|TABLE)[[:space:]]+"?reference_stubs' scripts/migrations/data_*.sql`
→ **2 files**. `data_20260823223839` INSERTs the stubs; `data_20260823225142`'s own header:
*"fold reference_stubs into source_locators … Runs as a DATA migration so it replays AFTER
data_20260823223839 fills reference_stubs."* So on `--rebuild`, both migrations replay and
**require the table to exist**; an ordinary schema `DROP` (which replays before data) breaks
reproducibility. The plan ran the C5 collision measurement for its renames and **never ran it
against its deletion set** — I did; `reference_stubs` is the only Tier 1/2 collider.
Rule 5's own procedure ("grep `scripts/migrations/data_*` for the name first") was skipped by the
document that quotes it.
**The honest ground is better:** not "no writer" but **superseded** — migration
`data_20260823225142` already performed this deletion's work (folded 10 of its 11 columns, which
are a column-subset of `source_locators`, `metadata_quality` excepted). §1 lists "superseded" as
exactly the evidence wanted.
**Smallest fix:** re-ground the row and mark the drop `-- AFTER_DATA` explicitly (T-B.5's blanket
AFTER_DATA note covers renames; say it covers this drop too).

## 4 · MAJOR — `search_coverage`/`search_languages`: the duplication claim is right, but by a recorded ruling the plan never cites, and "delete now" omits six live readers

The task's question — is per-slug derivable from per-query? — has a measured answer in the tree:

- **Naively, no.** The grids carry judgments, not restatements: `status IN
  ('SEARCHED','THIN','NO-DATA','NOT-RUN')`, `co1/tier5/tier6_attempted` flags (DDL above,
  `PRAGMA table_info`). A missing execution row cannot distinguish NOT-RUN from never-planned.
- **But the repo already ruled and built the derivation.** `scripts/db.py:264–320`: the grids are
  **FROZEN** (`FrozenGridError`), per `workplan/search-coverage-completion-workplan.md` — *"derive
  every coverage matrix as a VIEW over that log"* — and the successor views exist
  (`v_coverage_jurisdiction`, `v_coverage_language`, `v_coverage_branch`). Measured drift that
  motivated the freeze: 634 SEARCHED cells vs 15 corroborated. The grids' own history is why
  rule 5 wins here.

So the Tier 1 verdict **survives**, but on the frozen-grid ruling + built views, not on the bare
"restates `search_executions.slug/jurisdiction`" — which is false as written (the grids restate
the *key* and add non-derivable judgment columns; the ruling is what makes those columns
illegitimate). And "delete now" is mispriced: live readers are `tools/evidentiary_audit.py`
(:250, :261, :369–373, :486, :719 — feeds a **blocking** freshness gate), `scripts/db.py` status
counts (:546–549), `scripts/tests/test_db_integrity.py`, `scripts/audit/research_batch_dod.py`,
`research_protocol_audit.py`, `research-log-manager_SKILL.md`, plus registry prose.
**Failure scenario:** the drop lands without the sweep; `evidentiary_audit_fresh` goes red or
vacuous on `no such table`.
**Smallest fix:** cite the freeze ruling as the ground; name the six-reader sweep in the same
Tier 1 row. (Deleting a *frozen historical artifact* also deserves one sentence engaging that
recorded disposition — the A4-B9 "recorded reasoning unexamined" class — though with 0 rows post
clean-room-reset the artifact is empty and the point is dischargeable in a line.)

## 5 · MAJOR — Tier 2's check, actually run: **7 of 11 clear; 4 do not**, and one non-clearer is live CI infrastructure

Command per table: `grep -rlw <t> scripts tools skills governance schemas .github | grep -v
'_archived\|__pycache__\|/deprecated/'` plus the data-migration DML grep (all 11: **0 DML
collisions**). Results:

| table | verdict | evidence |
|---|---|---|
| `url_verification_runs` | **KEEP — move to Tier 3** | writer `scripts/verify_urls.py`; **dedicated scheduled workflow `.github/workflows/verify-urls.yml`** (one of CLAUDE.md §5's four); `test_url_verifier.py`; registry entry. Deleting it decapitates a live pipeline's log |
| `gap_mining` | does not clear as-is | registered check `gap_mining_audit` — registry :1092: *"EXAMINED prints COUNT(*) FROM gap_mining, the table this whole audit walks"*; `db.py`; `gap-driven-mining_SKILL.md`. And §6.3 calls the gap-driven walk *"a live requirement"* — deleting its act log while affirming the activity is incoherent. Deletable only via the acts fold (§6 below) |
| `supersession_check` | does not clear as-is | `db.py:1051` — *"DR-2026-05-24: v2 requires … supersession_check_complete=1"*; `bpc_metadata.supersession_check_complete`; `supersession-audit_SKILL.md`; `code_currency_audit.py`. Fold, don't delete |
| `item_audit_runs` | does not clear as-is | `db.py` `add-audit-run`/`update-audit-run`/`audit-runs` (:1191–1211, :730–766); `audit_consolidator.py`; 2 skills |
| `case_study_specs` | **does not clear — KEEP** | it is the named remedy inside a live `db.py` **refusal** (:2486: a REF-id in `--sources` prose is refused with *"Link the source through case_study_specs"*). Deleting the designated remedy of a live refusal is the exact R6 defect CLAUDE.md voids ("the designated remedy for a violation still on the books") |
| `extraction_population_links`, `probe_population_links`, `citation_population_links` | clear, with a named sweep | readers are audit-only: `population_integrity_audit.py`, `regenerate_vetting_surface.py`, `schemas/population_links.py` (Pydantic mirror — drift is a bug, so drop it in the same commit), registry, `known_debt.yaml` |
| `case_study_populations`, `economics_entry_populations`, `economics_entry_specs` | **clear** | only `057_baseline` + `pipeline-map.yaml` + `context-map.yaml` |

**Consequence for the arithmetic: the 52 floor is unreachable by deletion.** With 7 of 11
clearing, deletion-only bottoms at **66 − 6 − 7 − 1 + 4 = 56**.

Fairness check the other way (Tier 3 rows that could be Tier 1): `room_items` and
`external_root_registry` have the identical caller profile to the clearing junctions (057 + two
governance maps, nothing else) — the plan protects them as "ordained empty" while deleting their
twins. Defensible (render/evidence will need them) but the asymmetry is asserted, not evidenced;
one sentence each would fix it.

## 6 · MAJOR — the two family folds: the refusal is half right, and the measurement is used backwards

Verified: **acts 7-way column intersection = ∅** and **leads 4-way = {`notes`}** (command:
`PRAGMA table_info` + set intersection; script in session log). The plan's numbers are honest.
The inference is not:

- **Zero shared columns is naming drift, not row-kind evidence.** All 7 act tables carry the same
  two facts — who ran it, when — spelled 7 ways (`session/executed_at`,
  `attempted_by_session/attempt_at`, `checked_by_session/checked_at`, `run_by_session/started_at`,
  …). The stat that "refutes" the fold is the disease J.3 diagnosed, measured.
- **The core four are near-siblings.** `gap_mining ∩ supersession_check` = **6 substantive
  columns** (`candidates_returned`, `candidates_reviewed`, `check_method`, `outcome`,
  `search_strategy_record`, `notes`); `search_executions` already carries `mining_direction` —
  the plan's own J.1 quote (*"a mining pass IS a search with a different origin"*) is a ruling
  that the fold is the model. Union of the four = **55 raw columns**, and roughly a third
  dissolve under the plan's own decisions: mining yield → `res_items` rows with
  `origin`/`parent_item_id` (T-B.7), packed `superseding_ref_ids`/`candidate_dois` → lead rows or
  a junction, triplicate id/session/timestamp → one spelling. A folded `res_searches` with
  `kind ∈ {search, mine-backward, mine-forward, gap, supersession}` lands near ~35 columns —
  narrower than `jurisdictional_values` (32) plus its own stamps, nothing like the "~90-column
  >80% NULL" strawman, which only describes the 7-way merge nobody should do
  (`url_verification_runs` and `pipeline_runs` are counters-reports — a genuinely different
  row-kind — and `item_audit_runs` a process checklist; keeping those out is correct).
- **Leads:** the {notes}-only stat conceals that `reference_stubs` shares **10 of its 11 columns**
  with `source_locators` and was **already folded** by `data_20260823225142` — one of the four
  "unfoldable" tables was folded by a committed migration the plan never greps.
  `search_candidates → res_items` is clean (union 32 columns; `tier_guess`→`tier_claimed`,
  `locator`→identifier columns, `disposition`→`status`, `exec_id` kept as provenance — the same
  column J.1 already adds). `jurisdictional_values` is the one genuine deferral: its 16 `loc_*`
  columns are a **byte-for-name duplicate of `source_value_extractions`' locator block** (24
  shared columns total — measured; a live structural dual home no document has flagged), so its
  fold needs the T-B study the plan promises.
- **And the promise has no owner.** The plan calls these folds *"worth more than every deletion
  combined"* (9.5) — then assigns them **no task ID anywhere in T-0…T-C**. The highest-value
  minimization item in the owner's own metric is scheduled nowhere.

**Smallest fix:** add a T-B task: fold `citation_mining`, `gap_mining`, `supersession_check` into
`res_searches` with `kind` (−3, J.4-mandated), fold `search_candidates` into `res_items` (−1),
defer `jurisdictional_values` to the named column study.

## 7 · MAJOR — `figures` fails §1's mirror clause as scheduled

The burden's first half is paid in book terms (§6.5: no alt-text column exists in a guidebook
about access; a drawn value-figure drifts) — A4-B9 credits it and I concur. The second half is
not: *"Nothing is added without naming what reads it."* **No renderer reads `figures`, none is
scheduled, zero figures exist**, and `figures` appears in the 9.5 arithmetic (+1) while appearing
in **no task** (T-A2's table omits it; NOMENCLATURE put it "in the baseline", which the plan
refuted). The plan applies "re-create a sibling when a stage actually needs one" to the
population junctions and exempts `figures` from the same rule without argument. K4's corrections
(per-stage junctions, not `figure_links(target_kind,…)`) also mean the real cost is +1 table plus
junctions, uncounted.
**Smallest fix:** strike `+1 figures` from the count; create it in the commit that ships the
first figure, with its generator named as the reader.

## 8 · The §1 judgment on what the plan creates, strictly in §1's terms

| object | verdict | book harm as stated |
|---|---|---|
| `syn_judgment_links`, `spe_synthesis_links` | **PAYS** | Part 4 :199 — a rendered "1200 mm ●" with *"no key path … back to the extraction that produced it, or the paper"*; *"a reader cannot check the number and neither can a gate — which is how five fabricated citations passed six green gates."* That is the guidebook, not the apparatus. A4-B9's charge ("inferable and never stated") is answered by this text |
| `jud_items` | **HALF-PAID + IOU** | Part 4's traceability harm justifies a *keyed path*, which a direct syn→evi key would also give. `jud_items`' distinctive content — soundness, weight, `dissent_of` — is paid only by "a determination built on ungraded, unweighed extractions," which 9.1 concedes came from A4 and exists nowhere operative yet ("must be paid in those words in the migration header" — i.e., not yet). The plan's sentence "The burden is paid" overstates by one third |
| `syn_synthesis_links` | **UNPAID and UNCOUNTED** — yet presupposed by Tier 1's `connections` ground (finding 2). Its payment is easy (Part 5's book content needs a warrant chain) but unwritten |
| `figures` | half-paid; reader unnamed (finding 7) |
| `res_items.origin` + `parent_item_id`, `dissent_of`, `unknown-legacy` | columns; pass — T-B.7 states the closed defect (138 harvested DOIs, 4 promoted) |
| 9.7-H prefix-drift check; S-1 ledger-execution check | **FAIL §1 as written** — both are justified entirely in apparatus terms ("the rename is a one-time correctness event with no guard"; "a check should read it"). §1: *"If the answer is about the apparatus rather than the book, do not add it."* Either pay them in book terms or drop them — the plan cannot add apparatus-justified checks in the same document that voids others for that ground |

## 9 · DEFECTS

- **D1 — two tables fall out of the menu.** §6.6's 19-table set minus Tier 1 (6) minus Tier 2
  (11) leaves `case_study_outcomes` and `case_study_strategies` in **no tier** — not in Tier 3's
  12 names either. If they were meant Tier 2, the floor is 50, not 52; if Tier 3, the K.4
  split-ground of §6.6 was silently dropped. Count the list.
- **D2 — "the only keyed cross-stage edge in the schema" (9.5, re `search_admissions`) is false**
  by the plan's own tables: `evidence_sources.ref_id` carries 7 cross-stage inbound keys (Part C),
  `gaps.gap_id` 2, and X2 itself names `specifications.convergence_id`. The defensible claim:
  the only keyed edge joining two *consecutive* stages' act/hand-off objects. The KEEP verdict
  survives; the superlative does not.
- **D3 — the `items` −1 assumes the outcome of the plan's own open question.** 9.6 recommends the
  retirement be re-put as a re-grain (a parameter-code registry) — under which the count is
  **net 0**, not −1. The range should say "−1, or 0 pending Q2/9.6."

## 10 · The arithmetic and the honest count

- **As stated, 52–63 is internally correct**: 66−6−1+4 = 63; −11 = 52. Verified.
- **As composed, it is not honest**: +1 owed for `syn_synthesis_links` (finding 2), −1 unearned
  for `figures` (finding 7), Tier 2 clears 7 not 11 (finding 5), −1 for `items` conditional
  (D3), two tables missing from the menu (D1). **Deletion-only, the reachable number is 56.**

**A genuinely smaller correct design exists (task 7), and it is the folds, not the deletions:**
delete the 3 evidenced Tier 1 (grids + stubs, with AFTER_DATA) −3; the 7 clearing Tier 2 −7;
fold acts −3 and `search_candidates` −1; fold `connections`+`targets` into
`syn_items.kind='connection'` when synthesis lands −2; retire `items` −1 (or 0 per 9.6); create
`jud_items` + 3 junctions +4; defer `figures`; `situations` only on owner sign-off (−1 more).
**66 → 54 firm, 52–53 with the owner-gated and study-gated items — below the plan's reachable
floor, deleting no live infrastructure, and by the mechanism (J.4) the owner's own quoted rule
prescribes.**

## 11 · Attacked and could not break

The base measurements (66/33/18, re-run above); the 7-way-merge refusal and the polymorphic-
junction refusal (both sound); the `ren_items` withdrawal and check-artifact resolution
(046-compliant and §1-clean); **no view reads any deletion-menu table** (measured over
`sqlite_master` — a point in the plan's favor it never claims); the `search_admissions` KEEP
(`v_source_admission` reads it; the packed `admitted_ref_ids` alternative is worse, as 9.5 says);
Tier 3's protection of the spine tables and of `case_studies`/`economics_entries` (R12 verbatim
confirmed at `governance/research-contract.yaml:186–193`); the 52–63 arithmetic *qua* arithmetic;
X5's retraction of "33 empty = 33 unpaid" (correct, and consistent with rule 4).

---

**DIGEST (5 lines):**
1. Tier 1 is wrong twice: `situations` is owner-gated Co-1 doctrine (functional-taxonomy:324, held-tensions:363), and `connections` feeds book Part 5 while its fold target (`syn_synthesis_links`) is deferred and uncounted — both BLOCKERs.
2. `reference_stubs` "no writer" is false — 2 committed data migrations collide (drop needs AFTER_DATA); true ground is "already folded by 225142"; the grids' true ground is the recorded freeze ruling + 3 successor views, with a 6-reader sweep the plan omits.
3. Tier 2 run: 7 of 11 clear; `url_verification_runs` (scheduled CI workflow), `gap_mining`, `supersession_check`, `item_audit_runs`, and refusal-remedy `case_study_specs` do not — so deletion-only bottoms at 56, and the 52 floor is unreachable as written.
4. The fold refusal misreads its own stat: zero shared columns is naming drift; core-4 acts fold (~35 cols, J.1/J.4-mandated) and `search_candidates` fold are feasible now, have no task ID despite being "worth more than every deletion combined," and are what actually reach ≤54.
5. §1: junctions PAY (Part 4 states the book harm); `jud_items` half-paid with an admitted IOU; `figures` counted but reader-less and unscheduled — strike it; 9.7-H and S-1 checks are apparatus-justified and fail §1's own test.
