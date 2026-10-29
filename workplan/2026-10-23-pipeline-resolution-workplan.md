# Pipeline resolution workplan: fix what the 2026-10-22 stress test found, in the order that keeps the first render honest

**Status:** DRAFT, NOT EXECUTED. Owner rulings are recorded in the ledger as they are given (`references/project-standards.md`, the entries beginning "Owner rulings 2026-10-29"); §4 says which are answered, and where an answer differs from the report's default the row says so. Every owner-gated item below is gated on its ruling. · **Date:** 2026-10-23 · **Scope:** Layer 0–2 apparatus (engine, writers, views, one renderer) and the research-data PRs that those tools make possible. No doctrine change except where a ruling in §4 says so.
**Reader:** the owner, then whoever executes a PR. **Self-retiring:** delete this file when §8 holds; git history is the archive.
**Basis (three documents, committed under `scratchpad/session_2026-10-22-pipeline-stress-test/`):** the question register (`question-register-2026-10-22.md`, Q0–Q14 and E0–E13), the reasoning pass (`fable-resolution-reasoning-2026-10-22.md`), and the resolution report (`resolution-report-2026-10-22.md`, cited below as **the report**). The report is the procedure: it holds each PR's exact steps, tests, mutations and commands, and its Appendix A lists where the reasoning pass was wrong. This plan holds the order, the gates, the owner decisions and the completion test. Where the two differ, this plan wins and §3 lists the difference.
**Antagonist:** one pass ran on commit 78bf84d9, commissioned by the owner on 2026-10-23 (LED-210). Each finding was checked against the artifact before it was applied; the commit after 78bf84d9 lists the dispositions. §10 states what was checked by script.

---

## 1. Standing constraints

Three constraints bind every PR. The first is the owner's, given on 2026-10-23 in this session and recorded verbatim in the ledger by H-0 (CLAUDE.md rule 0): *"ensure the outcome has as little code as possible, obeys code architecture, and allows for a dynamic pipeline walkable all directions."*

- **As little code as possible.** CLAUDE.md §8 governs: a PR adds nothing without naming what reads it and what wrong thing reaches the guidebook without it. A PR touching `scripts/`, `schemas/`, `.github/` or `skills/` does not raise their line total unless its description names the exception and what it replaces (`git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'`). Each item that adds code and has no reader today is marked *optional* in §5 and is built only on the owner's yes. **No offset is promised beyond the deletions each PR names.** Step 4.4 of the simplification plan would delete `graph_audit` and its modules, but that plan registers its check only when the set the check prints is empty or every member is a named residual (15 of 56 tables on the rehearsed stack; this plan touches none of them, and T-6b's foreign-key-less table joins the set), so that deletion is not counted on (§2). The aggregate is measured at the end and reported (§8 item 8); it is not gated.
- **Architecture.** Rule 5: point, do not copy; a derivable fact gets no column (the report's K-2 lists the tempting ones). Rule 8: a vocabulary is a table or a CHECK, never a list in code. Rule 3: the database changes only by migration. Rule 10: tooling and research ship in separate PRs, tooling first. The item layer is gone: no `[A-Z]-NN` code is a container.
- **Dynamic, and walkable in every direction.** Dynamic means a new parameter, slug, lens code, jurisdiction, language or unit needs a row or an `add-*` call and no code edit. The design already has that shape: a non-family unit is read on a scale of its own; the lens predicate runs over the lens columns; buckets are a table; parameters come from observed terms; the renderer queries live cells. Walkable means what the owner said on 2026-08-27 (`scratchpad/session_2026-08-27-hook-audit/WALKABILITY-PLAN.md` §6.0): "the pipeline must be walkable all directions (read write both ways) · render must end up able to pull data across all tables all stages", and it is measured by `workplan/pipeline-state-graph/walkability.py` (§8 item 6). **Whether a render stage made of views counts as reached is the report's U-7. The 2026-10-23 statement does not answer it** (it names neither views nor render); it is put to the owner as OW-1 (§4), and the report's T-5 acceptance, "walkability into render still prints NO PATH, by construction", stands until OW-1 is answered.

---

## 2. State this plan was written against, and the simplification plan

Re-derive; do not quote. Measured 2026-10-23 on `origin/main` at the merge of PR #201:

```
python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('PRAGMA user_version').fetchone()[0], c.execute('SELECT COUNT(*) FROM specifications WHERE retired_at IS NULL').fetchone()[0])"   # 116 0
ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1                                                  # 116_specification_marker.sql
grep -n '^RULE_VERSION' scripts/assess/assess_cell.py                                                          # pilot-4
git log origin/main --oneline --no-merges | grep -E 'step [0-9]'                                               # which simplification steps merged
```

**No determination is live** (second figure above), so nothing reaches a reader today. The order below is the order that makes the first render correct, not a response to harm in progress.

`workplan/2026-10-12-simplification-workplan.md` line 3 still says "NOT EXECUTED … no step has run". That is false: its Phases 1 and 2.2 and Phase 3 (base, research, evidence, judgment, specification) are merged. [CORRECTION: the status line of that file; not edited here.] What remains there, and how this plan meets it:

| simplification step | state | here |
|---|---|---|
| 3 synthesis | nothing built, by ruling (RULINGS R17: build nothing until a second parameter holds an extraction) | D-1 fires R17's trigger (`SELECT COUNT(DISTINCT parameter_id) FROM source_value_extractions` > 1); revisit R17 after D-1 |
| 3.R render | not built (`scripts/generate/` holds no renderer) | **T-5 owns it.** T-5's scope is wider than 3.R's "one view": three view changes and one renderer |
| 4.1 verbs diet | no commit names it | after T-8, so the new verbs are judged with the rest |
| 4.3 comment diet | optional in that plan | skipped |
| 4.4 one derived walkability check | no commit names it | after T-5, if its registration condition can be met. It registers the table-level check of IDEAL-GRAPH §6 (per table: reaches base, reaches the determination, orphan, dangling), **not** a stage-pair measure; its own text says `walkability.py` "is not a registered check". It registers only when the set it prints is empty or every member is a named residual, and until then `graph_audit` stays. So it is **not counted as an offset here**: it would delete `graph_audit.py`, `scripts/audit/graph/` and their test (`wc -l scripts/audit/graph_audit.py scripts/audit/graph/*.py scripts/tests/test_graph_audit.py`; the code alone was 1,385 lines on 2026-10-23) only once its condition is met. [UNVERIFIED: that the roughly 40-line check covers every duty of `graph_audit`; that is the old plan's claim.] |
| 4.5 centralize bindings | no commit names it | unchanged |
| 5 research PR | no commit names it | D-3 is its scan-debt work. Its other items (the `annotate-parameter` compensating migration, medical-lens rows by `add-medical`, the bytes backlog with `source_type` supplied for the sources that lack it, the missing admissions) are unchanged and are separate data PRs |
| 6 retire the scaffolding | — | last; deletes both plans |

---

## 3. Rules, and where this plan departs from the report

Every PR obeys CLAUDE.md and the simplification plan's W1–W10 (caller sweep in the same change; order by the graph; net-negative; probes and `build_graph.py --check`, instrument regenerated last; rules 9 and 10; migrations numbered at branch time with the `AFTER_DATA` marker where a backfill or rebuild needs one; a read-only antagonist pass on the diff; run from the repository root; the instrument shrinks as it works; rehearsal in a clone whose `origin/main` is the PR's base). Added here:

- **WR-1 One PR merges at a time.** Branches may be prepared in parallel; each later one takes the merged predecessor with `git merge origin/main` and renumbers its migration (`ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1`). A data PR is never open while a tooling PR that changes `data/guidebook.db` is open.
- **WR-2 `RULE_VERSION` bumps are derived, not planned.** T-1b (step 9), T-2, T-3 and T-4 each bump it. The label comes from `main` at branch time; K01's closed set (T-3 step 6) is derived from `git log -p -S'RULE_VERSION = ' -- scripts/assess/assess_cell.py`.
- **WR-3 Rulings first.** Each answer in §4 is appended to `references/project-standards.md` as a dated `## Owner ruling …` entry before any branch that depends on it opens. A ruling that changes a ratified record carries a `SUPERSEDES` line (report §7.3 lists them). A default is a proposal, not a ruling.
- **WR-4 Regression before and after.** Each tooling PR runs `scratchpad/session_2026-10-22-pipeline-stress-test/report-probes/regress_2026-10-22.sh` (usage in the report §6.2) before and after, and the PR body states the differences against the PR's acceptance list.
- **WR-5 Opus-class for synthesis.** A synthesis approach (T-4's `divergent` cells) is written only by an Opus-class session (CLAUDE.md §6). A session that is not Opus-class leaves such a cell unwritten.
- **WR-6 Commit trailers come from the session's harness.** The report's protocol step 8 hard-codes a model name; do not copy it.

| report says | this plan | why |
|---|---|---|
| T-1 is one PR | **T-1a** (steps 1–7, no ruling) and **T-1b** (step 8 on OR-3, step 9 on OR-10, step 10 on OR-11a; each its own PR, only on a yes) | three rulings should not hold the ruling-free work, and step 9 bumps `RULE_VERSION` |
| T-5: walkability into render prints NO PATH by construction | T-5 proposes mapping its views to `render` (§5, T-5), gated on OW-1 | the owner's 2026-10-23 statement requires walkability but does not rule on views (§1) |
| T-6 step 4: the owner rules the codes for UN and ISO, "not in the enum" | no ruling needed: `schemas/enums.py` `JurisdictionCode` declares `UN`, `ISO` and `INT`, `dbcore.check_jurisdiction` reads that enum, and live rows carry them | the report's sentence is false (`grep -n 'UN = \|ISO = \|INT = ' schemas/enums.py`) |
| T-6: OR-12 gates steps 4–6 (header) and step 3 (decision sheet) | **T-6a** steps 1–2 (no ruling); **T-6b** steps 3–5 (OR-12, OR-8), step 6 only if OR-9 names indices | the report is inconsistent; the sheet's reading is the safer one |
| "stops the guidebook giving autistic, blind and ADHD readers the wheelchair answer" | no live determination exists | §2 |
| protocol steps 1–10 omit the antagonist pass on the diff and the rehearsal clone | both stay (W7, W10); the harness assigns the branch (develop and push only there), so the report's `claude/<pr-slug>` is an example; `git checkout -B` and `git rebase` are blocked (CLAUDE.md §7), so a branch whose PR merged takes `git merge origin/main` | the report's branch name conflicts with the harness's |

---

## 4. Owner decisions

**Answered 2026-10-29 (ledger):** OR-1, OR-1b, OR-2, OR-3, OR-4, OR-5, OR-6, OR-6b, OR-7, OR-8, OR-9, OR-10, OR-11a, OR-11b, OR-12a, OR-12b, OR-13, OR-14, OR-15, OR-16, OR-17, OR-18, OR-19, OR-20, OR-21, OR-22, OR-23, OR-24 and OW-1. Follow-up questions the answers raised: OR-1c, OR-5b, OR-6c, OR-10b, OR-14b, OR-17b, OR-22b, OR-23b, OW-1b and OW-1c (the owner's browser page lists what is still open). Where an answer differs from the default shown in a row, the row's last column is annotated and the ledger entry governs.

The report §2 holds each question in full, with its default. Here: which PR each gates, and what happens to the code if the answer is no. Six gate building: **OR-1, OR-2, OR-3, OR-5, OR-6, OR-8**. All answers can go in one ledger entry (H-0).

| id | decides | report default | gates | code effect of "no" |
|---|---|---|---|---|
| OR-1 | a row reaches a cell only through its own lens codes (confirms D-0184) | yes; **answered: yes, but no `pending` row is stored for a lens the parameter is not relevant to, and every relevant model is filled (ledger)** | T-3, D-2 | **more** code: T-3 would build traversal of the crossing maps, which D-0184 measured and rejected |
| OR-1b | identity `ALL` rows reach every identity cell | no | T-3 | yes adds one clause |
| OR-2 | conditional branches beside a headline from unconditioned claims | yes, empty headline | T-2, D-1 | T-2 not built; a code's step table keeps printing as one number |
| OR-3 | reformat a value or unit in place (narrows D-0168) | yes | T-1b step 8, D-1 | step 8 not built; D-1 writes second rows and the old rows stay as contests |
| OR-4 | most accommodating anchoring value wins, tier-blind within anchors | yes | T-4 | T-4 waits for a rule that does not exist |
| OR-5 | Co-1 sets direction, not a dimensional value (§6.4) | yes; **answered: a Co-1 figure sets a value when its source is academically sound (ledger; OR-5b open)** | T-4 | T-4 step 3 not built; §6.4's false mechanism sentence is deleted either way |
| OR-6 | unsatisfiable anchors: `stated` + `divergent` + synthesis approach (§3.3) | yes; **answered: yes, with the T1 figure stated and the T2 dispute noted (ledger; OR-6c open)** | T-4 | "cap at provisional" amends canonical text |
| OR-6b | satisfiable but different floors count as divergent | no | T-4 | yes would add a synthesis approach to most multi-source cells |
| OR-7 | a T6-only cell renders as a flagged weak row (Option A) | yes | T-5 | view unchanged; two ratified texts amended |
| OR-8 | coverage per parameter × bucket-1/2 jurisdiction × language, buckets a table | yes; **answered: yes, a bucket member is a jurisdiction-and-language pair (ledger)** | T-6b | steps 4–5 not built |
| OR-9 | which indices must be searched | none yet | T-6b step 6 | not built |
| OR-10 | convert exact lengths (in, ft ↔ mm, m) | yes; **answered: yes, show both, rounded to the nearest 1/4 inch or 5 mm (ledger; OR-10b open)** | T-1b step 9 | not built; mixed-unit length parameters decline to compose |
| OR-11a | `verified` requires a full-scope scan | yes | T-1b step 10 | not built |
| OR-11b | a `preliminary` figure may set a value, flagged | yes, flagged | T-5 (the flag) | **adds a line**: `preliminary` joins the rule beside `dbcore.NOT_PUBLISHABLE_METHODS`, whose comment forbids it without this ruling; the report assigns that edit to no PR (it says only "nothing in T-1 to T-4") |
| OR-12 | AR/BN/HI/SW scoped out; model-generated aliases usable if flagged | yes; yes | T-6b step 3 | (a) no: alias building for those four languages becomes research debt; (b) no: the model-generated aliases (`python3 scripts/audit/alias_provenance_audit.py`) become unusable for searching |
| OR-13 | seed the quantity list by open-pass scan of held codes | codes | D-8 | slugs: D-8 runs per slug |
| OR-14 | a derived element page from a typed term pointer | yes | T-7, D-6 | **T-7 not built** (the largest optional item) |
| OR-15 | held batch-23 material for the inter-rater test | yes | D-5 | owner names other material |
| OR-16 | read held sources before fetching more | yes | D-3 scope | D-3 limited to bucket-1/2 |
| OR-17 | bulk vocabulary approvals by the assistant under LED-154 | yes | D-4, D-8 pace | each table goes to the owner |
| OR-18 | transcripts suffice as model/effort telemetry | yes | D-5 | session records gain `Model:`/`Effort:` lines |
| OR-19 | grey source echoing a code value: presumed echo, not re-tiered | yes | T-8 step 3 | step 3 not built |
| OR-20 | mine T4–T6 anchors backward | no | D-7 | yes adds a mining pass |
| OR-21 | per-lens direction when `contested` | when it first arises | — | trigger query returns 0 today |
| OR-22 | what a floor claim confirmed by an all-`absent` study is | owner | the REF-00980 cell in S-1 | cell left out of S-1 |
| OR-23 | an unretrievable source keeps its tier, earns no band above ○ | confirm | — | — |
| OR-24 | "skimmed" means `extraction_method = 'skim'` | confirm | — | — |
| OR-25 | batch 23's extraction cap carries over to scans | no cap | D-3 batch size | cap derived from batch 23's row count |
| OW-1 | (report U-7) a render stage made of views counts as reached: `stage-map.yaml` gains a `views:` key and `walkability.py` counts a mapped view as a member of its stage, which changes the rule its docstring states ("a view's stages are those of the tables it reads") | not in the report; the plan's proposal is yes, because it fits the owner's 2026-08-27 clause that render pulls data across all stages, but no ruling exists | T-5's walkability addition; §8 item 6 | no: no `walkability.py` change, the `*<->render` pairs stay NO PATH and are named residuals, or the owner designs a render table (none is designed here; the report says do not invent one) |
| OW-2 | keep `walkability.py` past Phase 6 and register it as the stage-pair gate | not in the report | §8 item 7 | no: it leaves with the instrument (simplification plan Phase 6) and walkability is a command run at the end of each phase; yes: one registry entry |

---

## 5. Pull requests, in merge order

Procedure for each is the report §3 (tooling) or §4 (data). "Code" is the report's Appendix D estimate of net non-test lines (an estimate; measure with `git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations' ':!scripts/tests'`). The T-1 to T-8 estimates sum to roughly 650–935 net non-test lines (each figure already nets the deletions Appendix D counts for it).

**H-0 Ledger entry** (docs only). Appends the owner's answers (§4) and the §1 statement. A ruling that supersedes a ratified text also needs the audit's grammar (`scripts/audit/supersession_backpointer_audit.py`): a `SUPERSEDES: <target> :: "<quote>"` / `BY:` pair in the entry, **and** a one-line SUPERSEDED or AMENDED mark carrying the BY quote at the target, so H-0 edits those targets (report §7.3 lists them); a mark in `decisions/` needs an attestation (rule 2). OR-10's target is the ledger itself, where the pair cannot be written (ledger entry of 2026-10-20), so that supersession is stated in the entry's prose only. Also adds the derived owner queue to `.claude/commands/orient.md` (report §5, E12: open gates, open follow-ups, catalogue names awaiting approval, unadjudicated observations; text only, no apparatus). Opens only after the owner has answered; T-1a and T-6a do not wait for it.

**T-1a Reading** (report T-1, steps 1–7). Needs nothing. Resolves Q3, E2, Q2-assembly (derived arithmetic), Q13-trust (half); closes GAP-056 (the row closes in D-1).
Moves the notation arithmetic to `dbcore`; deletes `parse_bound` (dead) and the duplicate arithmetic in `derive_extraction`; the writer refuses unreadable figures, prose units, a missing comparator, and a derived figure that contradicts its inputs. Includes the numeral gloss (`--verbatim-exempt` cannot stand in for it: it is refused when the quote occurs in the bytes, and row 80's does).
*Done when:* N1–N11 pass; `test_assess_cell_pilot.py` passes; `extraction_relations_integrity.py` prints `VERDICT: CLEAN` with `EXAMINED:` above 0; `grep -rn "def parse_bound" scripts` is empty; `fixtures_g1_g13.py` output is byte-identical before and after; M1–M5 print KILLED; `build_graph.py --check` reports 0 failures. Code +45..95 net of the deletions it makes (Appendix D).

**T-6a Case fold** (report T-6 steps 1–2). Needs nothing. Resolves the language-label split (Q10-coverage). `log-search` folds and shape-checks the language; the coverage views fold with `UPPER()`; no UPDATE of history.
*Done when:* the C6 test that `log-search --language fr` stores `FR` and `--language xx1` is refused passes (the two `--term` tests belong to T-6b); `SELECT COUNT(DISTINCT language) FROM v_coverage_language` equals `SELECT COUNT(DISTINCT UPPER(language)) FROM search_executions WHERE deferred_reason IS NULL` (the view reads non-deferred rows only; the report's all-rows comparison is equal today only because no language is deferred-only); M20 KILLED. Code +50..80 across T-6.

**T-2 Conditions** (report T-2). Needs T-1a; OR-2. Resolves Q4, Q5 (mechanism), Q8 (conditionals), Q2-cross (the edge is how one parameter checks another). Governing rows with an outgoing `condition_on` edge leave the headline and become branches; a new such edge from a governing row of a live determination is refused. Reads only edges **from** governing rows (K-11).
*Done when:* B1–B6 pass; M7, M8 KILLED; C20's governing-edge query prints 0 before and after; fixture output unchanged; parameter 3 under MOB still reads `max 5.0`. Code +35..50.

**T-3 Lens** (report T-3). Needs T-2; OR-1, OR-1b. Resolves Q7, Q9, the pending-path defect. A row reaches a cell only through the lens codes written on it; the attestation hashes all four lens columns; a pending cell claims no derivation path; a NULL lens column can be filled with warrant.
*Done when:* L1–L5 and the amend tests pass; M9–M12 KILLED; K01 and K02 print PASS with a non-zero subject count on a populated scratch; no row is stored for a lens no figure carries (AUT, BLIND, ADHD, d450 and A-EFFORT on parameter 3 have no cell, per the ruling on OR-1), an identity-ALL figure reaches only an ALL determination (OR-1b), and how a determination and its figures carry several codes of one model is settled by OR-1c before this PR opens; (MOB) and (MOB, d450) differ in `derivation_sha`. Code +55..85.

**T-4 Agreement** (report T-4). Needs T-1a, T-3; OR-4, OR-5, OR-6, OR-6b. Resolves Q1, E8, E13, E6 (spread text). Excluded rows name their true cause; unsatisfiable anchors are recorded `divergent` and refuse to be written without a synthesis approach (WR-5), which for a T1 figure against a T2 figure is the owner's: the T1 figure is stated and the T2 dispute is noted in the item's discussion (ledger, OR-6; its reach is OR-6c); a Co-1 figure sets a value only when its source is academically sound (ledger, OR-5; how that is established is OR-5b), and otherwise sits beside the value, not in it; the note says how many rows set the selected bound.
*Done when:* the G1–G4, G8, G12, G13 assertions pass; the F-tests (report §6.1: every governing value × 1.1 and × 0.9, each comparator flipped, expectations written beside each case; the factor lives only in the test) pass; M13–M16 KILLED; `test_evidence_cell_state_2_3.py` and `validate_evidence_state.py` pass; §6.4's mechanism sentence is gone and any atom quoting it re-verifies (`verify_atoms.py`). Code +85..125. No tolerance, no engine-written approach (K-4, K-5).

**T-1b Optional reading steps**, each its own small PR on its ruling. Step 8 (OR-3): widens `amend-extraction` to unit, value and NULL `setting`; **must merge before D-1 if OR-3 is yes**. Step 9 (OR-10): the length family; bumps `RULE_VERSION`. Step 10 (OR-11a): the `verified` gate; its reader is T-5. *Done when:* N12 and M6 (step 8); `('36','in','>=')` reads `(Fraction(4572,5), None)` (step 9); for step 10, a test the report cites ("T-1 step 10 test") but does not define: `insert_extraction` and `amend_extraction` refuse `verified` without a full-scope `source_scans` row covering the row's parameter and accept it with one [GAP: write that test].

**T-5 Render** (report T-5, plan step 3.R). Needs T-2, T-3, T-4; OR-7, OR-11b. Resolves Q0, Q8 (render), E4 (the `insufficient` and `exceeds` edges only; see §9), E6, E7 (handoff), E10. Redefines `v_best_practice` (a T6-only cell appears, flagged), adds `v_determination_branches` and `v_code_inadequacy`, and adds `scripts/generate/render_cells.py`, which reads `specifications` directly so pending cells are not lost. Output goes to `$TMPDIR`; no rendered file is committed. **[Re-opened by the ruling on OW-1 (ledger, "Owner rulings 2026-10-29 (third)"): the render stage is expected to hold a table of complete prose and bibliographic information built from specifications and the preceding tables, so T-5's design waits on OW-1b and OW-1c.]**
**Walkability addition (proposed; only on OW-1 = yes):** `governance/stage-map.yaml` gains a `views:` key naming `render` as the stage of each view the renderer reads, and `walkability.py` counts a mapped view as a member of that stage, with its reads as the edges. This changes the rule the script's docstring states, and the stage-map header and `architecture/meta-scripts-spec.md` §8 describe a different shape (a `pointer:` list of the stages a cross-stage view spans); the owner chooses between them in OW-1. `build_graph.py --check` and `walkability.py` read `tables:` only today (`build_graph.py:144`, `walkability.py:30`), so a new key breaks neither. [GAP: the `walkability.py` diff is not drafted; the file is small and the change is a few lines, unmeasured.] `weighting_profile`, the render stage's only table, is read by no script (report Appendix B, RC-H); its deletion is an owner case under LED-169 (simplification plan 1.9), not part of this PR.
*Done when:* R1–R5 pass, and R6 if OR-7 is yes (R1, the count of rendered cells equal to the live `specifications` count, is also the test that rendering is parameter-agnostic); M17–M19 KILLED; P-K reads PASS; `render_cells.py --db <populated scratch>` renders parameter 3 with code-floor lines, and with branch lines once D-1 has landed (before it, R5's fixtures carry the edges: no governing row has an outgoing `condition_on` edge today); if OW-1 is yes, `walkability.py` prints a path for each specification↔render pair on the populated scratch. Code +250..310 against a plan target of 300 for the renderer (unverified). Do not build before T-2 to T-4: it would print their defects with authority.

**T-6b Search terms and buckets** (report T-6 steps 3–5; step 6 only if OR-9 names indices). Needs T-6a; OR-12, OR-8. `--term` derives `terms_used` from the alias table; `jurisdiction_buckets` (a table, approval ref per row); `v_coverage_parameter_via_admission`. `jurisdiction_buckets` takes the codes the enum already declares (§3). It has no foreign key, so it joins step 4.4's failing set: name it a residual there (its reader is `v_coverage_priority`) or give it a pointer. *Done when:* the C6 tests pass, including the two `--term` tests; M21 KILLED.

**T-7 Element pointer** (report T-7). Needs T-5; OR-14. *Optional.* Resolves E0, Q6, Q5 (assembly). `term_relations` with one relation, `relate-term`, `v_element_page`, `--element` on the renderer; an element row holds no value and no item code. *Done when:* the four refusals each pass with a control; `v_element_page` lists parameters 3 and 12 for TERM-089; M22 KILLED. Code +70..100.

**T-8 Roots** (report T-8). Needs T-4; OR-19 for step 3. Resolves E5. `add-root` writes `external_root_registry` (RULINGS R24's filed GAP); `convergent` requires two or more distinct roots, counted from a row-level view shared with `v_value_independence`. *Done when:* the shared-root and distinct-root tests pass; M23 KILLED. Code +60..90.

**Data PRs** (rule 10; each separate; ritual in report §4.0; every figure computed by a script, none typed):

| id | does | needs |
|---|---|---|
| D-1 | repairs the unreadable and prose-unit rows of parameter 3; writes condition rows and `condition_on` edges; closes GAP-056; checks GAP-007; no determination written | T-1a, T-2, T-1b step 8 if OR-3 is yes; OR-2, OR-3 |
| D-2 | fills a NULL lens column on an extraction only where a quote names the users | T-3; OR-1 |
| D-3 | the scan contract exercised: full text, a reading against every active parameter, `record-scan` per source; re-grades `verified` only on a full scan if OR-11a | T-1a; OR-16, OR-25, OR-11a |
| D-4 | promotes the adjudicated non-English observations to aliases; adjudicates the rest; `terms_used` half after T-6b | none (first half); OR-17 |
| D-5 | blind double extraction and model/effort comparison; raters are separate sessions the owner launches; output is measurement, not corpus | T-1a; OR-15, OR-18 |
| D-6 | element pointers | T-7 |
| D-7 | re-grades NULL and `untraced` roots; registers external roots | T-8; OR-20 |
| D-8 | seeds quantities from observed phrases in the held codes; never from the old Part 4 index | D-3 (its open pass supplies the observations; without it only `mint-term-from-catalogue` remains); OR-13; T-6b for buckets; OR-17 |
| S-1 | runs the engine over every parameter with extractions × each lens the rows carry, applies, and renders to `$TMPDIR` | T-5, D-1, D-3; OR-22 for its one cell |

Merge order, absent rulings: **T-1a, T-6a, D-4 (first half)** can start now; everything else waits on the ruling named. With rulings: T-1a, T-6a, T-2, T-3, T-4, T-1b (as ruled), T-5, then 4.4 (if its registration condition can be met), T-6b, T-7, T-8; data PRs as their needs are met, S-1 last of them; 4.1 after T-8.

---

## 6. What this plan declines

Report §7.1 (K-1 to K-14) is the list; each has its instead. Those most likely to be retried: traversing the crossing maps for lens routing (K-1); columns for conditions, branches, spread or selected bound (K-2); seeding from the old Part 4 index (K-3); a divergence tolerance or a percent sensitivity in code (K-4); an engine-written synthesis approach (K-5); a parity check between `extraction_status` and `source_scans` (K-8); backfilling `evidence_sources.language` (K-9); `UPDATE` of `search_executions` (K-10); `run_checks.py --all` to re-confirm (K-14). Also not built: a `claimed_unit` CHECK (Appendix A, finding 18), `search_indices` unless OR-9 names indices, per-lens direction (OR-21), cross-parameter synthesis tables (R17).

## 7. Order dependencies and the unknowns

Report §7.2 holds the order that breaks if sequenced wrongly; the one-line forms: T-2 before T-1a, T-5 before T-2 to T-4, D-1 before T-1a, D-2 before T-3, S-1 before D-1, two `RULE_VERSION` bumps in parallel branches, and a data PR open beside a tooling PR that changes the blob. The unknowns (report §8, U-1 to U-10) each name what settles them; U-4 is an owner or doctrine question with no command, and U-7 is OW-1 (§4).

## 8. Done

This plan is finished when all of these hold, each by its command:

1. T-1a to T-5 and T-8 are merged, and T-6a and T-6b, and T-7 if OR-14 is yes.
2. D-1 to D-5 and D-8 are merged, and D-6 and D-7 if their tooling is.
3. S-1 has rendered the live cells to `$TMPDIR`, with branches, code floors, flags and gaps present for the cells that have them.
4. The owner's battery (§9) is re-asked and every row's proof is green, or its last column names the ruling or limit that keeps it open.
5. The regression script (WR-4) shows every difference expected by §5 and none other.
6. `python3 workplan/pipeline-state-graph/walkability.py data/guidebook.db` prints no `NO PATH` line in either zigzag section (declared and populated). Today the only such lines are the ten `*<->render` lines (five pairs, each in both sections). Any pair that prints NO PATH after S-1 is named in S-1's record with its cause, and the owner rules it a residual. The directional matrix (up, down, skip, recvFK, sendFK) is reported with it, and no cell falls below its value at H-0; its zeros between research and the later stages are structural (no foreign key joins them) and are not a criterion. If OW-1 is no, the render lines stay and are named residuals.
7. Whether item 6 is a gate is OW-2. If yes, a registry entry runs `walkability.py` and fails on item 6; if no, item 6 is a command run at the end of each phase (simplification plan 4.4 says the same of it).
8. The aggregate change is measured (`git diff --shortstat <the commit before H-0>..origin/main -- scripts schemas .github skills ':!scripts/migrations'`) and reported to the owner with each PR's exception text. This plan does not promise it falls: the deletions available are those the PRs name, and step 4.4's is conditional (§2).

## 9. The owner's battery as the acceptance test

The questions put on 2026-10-22 are the measure of what is needed. Item 4 of §8 is this table re-run: each question is asked again of the finished system, and the proof is the report §6.1 row (red on 2026-10-22, green expected). The last column is what the work does **not** settle.

| the question (short) | resolved by | proof it is green | not settled here |
|---|---|---|---|
| Stress test all directions; attempt to render | T-5, S-1 | WR-4 regression; R1–R5 (R6 if OR-7); if OW-1 is yes, a path for each specification↔render pair; S-1's render of live cells | OW-1, OW-2; a cell with no live determination renders as a gap, by design |
| Competing rows; a gradient of conflicting values across tiers | T-4 | G1–G4, G8, G12, G13 assertions | OR-4, OR-6 |
| Cross-referencing; testing a parameter by related ones; how specifications are assembled | T-2 and D-1 (the cross-parameter `condition_on` edge); T-1a (derived arithmetic refused at write); T-4 (divergence, the Co-1 role) | N9, N10; `SELECT COUNT(DISTINCT parameter_id) FROM source_value_extractions` above 1; a branch row whose `other_parameter_id` differs from its `parameter_id` | cross-parameter synthesis tables stay deferred (R17, revisited after D-1) |
| Ratios, percentages, slopes: a common base? | T-1a, D-1 | N1–N8; the report's repair-set query prints only rows left alone on purpose | the unit of a source measuring along the slope is left alone, by design (E2) |
| A steeper slope allowed under one metre | T-2, D-1, T-5 | B1–B4; R5 | OR-2 |
| Rest landings | D-1, D-8, T-7 | `SELECT COUNT(*) FROM source_value_extractions WHERE parameter_id = 12` above 0 | a landing parameter exists only if a source states one |
| Rails, ramp surfaces, locations | D-8, T-7, D-6 | `v_element_page` for TERM-089 lists them | OR-14; a categorical quantity such as location has no direction and composes no value |
| Different access needs; are needs, identities and ICF codes directed appropriately | T-3, D-2 | L1–L5; the AUT, BLIND, ADHD and d450 cells `pending` with a gap naming the lens (A-EFFORT with a "finding only" gap); the two shas differ | OR-1; the medical lens stays empty until its registry is filled (RULINGS R16) |
| Qualitative information, clauses, exceptions, conditionals | T-5 (claim text verbatim), T-2, D-1 | a `stated` cell with a NULL value prints its governing claim sentences | OR-2 |
| Are all jurisdictions, languages and academic bodies searched | T-6a, T-6b | the C6 tests; coverage reached per parameter through admissions | academic bodies stay unmeasured unless OR-9 names the indices |
| Stepping values up and down | T-4 (leave-one-out note, F-tests) | M16; the F-tests | — |
| Non-English retrieval; correct terms and aliases | retrieval is already handled; D-4, T-6b | `alias_provenance_audit.py` attested above 0 after D-4; refused promotions listed in the session record | AR, BN, HI, SW (OR-12) |
| A robust, value-free list of slugs and parameters populating both | D-8 | `stress/listing.py` (committed with the report) regenerates the list; every new term carries an observation or an approval ref and passes the value screen; the hits the list prints for existing names are each dispositioned in D-8's session record | OR-13; the owner has not chosen between the two seeding routes; one existing slug is a real hit, and the screen stays unchanged (K-12), so that name needs the owner |
| Can the pipeline be trusted to read a source; what it records; what it finds beyond the slug | T-1a, T-1b, D-3 | `SELECT status, COUNT(*) FROM v_scan_ledger GROUP BY 1` shows READ-NOTHING-FOUND above 0; `scan_debt.py` shows the batch out of NOT-READ | OR-11a, OR-16, OR-25 |
| Do model and effort change what is recorded | D-5 | an agreement table per model pair, computed by the script | unknown until D-5 runs (U-1) |
| Citation mining | already handled | `citation_mining_completeness.py` prints CLEAN with `EXAMINED:` above 0 | OR-20 |
| The throughlines and extrapolations E0–E13 | E0 T-7, D-6; E1, E2 D-1; E3 T-1b; E4, E7, E10 T-5; E5 T-8, D-7; E6 T-4, T-5; E8 T-4; E9 T-6b; E11 D-5; E12 H-0; E13 T-4 | the report §6.1 rows | OR-14, OR-19, OR-5, OR-8, OR-10; E4: `search_executions.harm_finding` is flagged on some searches and read only as a count by `research_batch_dod.py`, so it reaches no row or render, and neither the report nor this plan gives it a reader [GAP: whether it needs one is open] |

## 10. Checks run on this file

A script extracted every backticked token ending in `.py`, `.md`, `.yaml`, `.sh`, `.json` or `.tsv`, tested it for existence (bare filenames resolved with `git ls-files`), and tested each cited view and table against `sqlite_master`; the only absences are the objects this plan proposes (`render_cells.py` and four views). The two stage-map readers were read directly (`build_graph.py:144`, `walkability.py:30`). The owner-commissioned antagonist pass then recomputed the counts and re-read the sources.
