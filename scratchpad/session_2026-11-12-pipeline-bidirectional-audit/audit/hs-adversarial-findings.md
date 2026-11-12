# HS-2 — Adversarial findings on both legs, with corrections

_Handshake leg, 2026-11-12 (UTC), HEAD `186defb`, `PRAGMA user_version` 125. Every count is given with its command; re-run before relying on any (rule 7a)._

## 0. Verdict first

_Amended 2026-11-12 after an independent antagonist pass (`fa-antagonist-objections.md`). Its objections (count: `grep -c -E '^\| FA-[0-9]{2} ' fa-antagonist-objections.md`) were each re-run; every one held at least in part. The dispositions are in §5, and every claim that changed is listed in `fa-corrections-for-suite.md`. Where this leg was wrong it says so in the finding._

**Both legs are sound on what they looked at and wrong, or silent, on what decides the objective.** The bottom-up leg's measurements reproduce: every query and engine run re-executed here returned what it reported. The top-down leg's quotations are accurate: every quote checked sits at the cited line. The failures are of reach:

1. **Neither leg caught that the engine's treatment of the lens contradicts the owner's answer on `ALL` and the ledger's reading of the OR-1 answer, or that the mobility split the owner ratified was never executed** (F-01, F-02). BU saw the mechanism and could not know the ruling; TD knew a ruling of the same message and did not carry its operative clause.
2. **TD did not read the ledger span that fixes the key, the lenses and the mobility split**, and its ledger is short by at least eighteen requirements (F-07). Three of its headline sentences are wrong as written (F-04, F-05, F-06).
3. **BU never opened `workplan/`**, so it missed the walkability instrument the owner ordered registered, the draft render contract, and the reason render is absent (F-03, F-12). It ran none of the blocking specification checks; one of its inferences about them is now confirmed by run, and one of its "correct" findings is wrong (F-10).
4. **Neither leg ran a test that could go red.** Every result of theirs is a positive observation. This leg pushed a determination for the wrong population through three specification checks, which passed, and in its first pass called that "every gate". That was wrong: the blocking `test_db_integrity`, which the first pass did not run, exits 1 on the same copy at criterion C10, for unverified governing sources. No gate tests the lens; one gate stops the cell for another reason (F-01). The repository does hold seeded-defect tests for the other specification rules (F-18).

**Canonical database hash.** `sha256sum data/guidebook.db`:
- before this leg's first command: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d`
- after seven engine runs on scratch copies and every audit run above: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d`
- at the end of the first pass: the same.
- before and after the resolution pass (further engine runs and the check runs of §5, all on fresh copies under `…/scratchpad/hs2/`): `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d`.

All stress tests ran on copies under `/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/hs/`. Audits were pointed at a copy with `GUIDEBOOK_DB_PATH` inline. In the first pass no repository file other than the four `hs-*.md` outputs was written. Later passes also wrote `fa-corrections-for-suite.md`, `hs-stress-audit.md` and `stress/RETAINED.md`, and annotated one sentence of `bu-capability-inventory.md`. No git command that changes state was run in any pass.

Counts in this file: findings `grep -c '^### F-' <this file>`; corrections `grep -c '\[CORRECTION' <this file>`; claims re-verified `grep -c '^| V[0-9]' <this file>`; antagonist objections by severity and disposition, the commands at the head of §5.

---

## 1. Findings, worst first

### F-01 No gate tests the lens: a determination for the wrong people passes the three specification checks and is stopped only by an unrelated criterion. Both legs missed that the behaviour contradicts the record. [VERIFIED; title and body amended, FA-02, FA-10, FA-21]
- **Run.** `cp data/guidebook.db $S/p3_DEAF.db; python3 scripts/assess/assess_cell.py --db $S/p3_DEAF.db --emit-sql $S/p3_DEAF.sql --parameter-id 3 --slug accessible-circulation-geometry --identity DEAF --session session_2026-11-12-hs-stress --stamp '2026-11-12 04:00' --report-json $S/p3_DEAF.json`
- **Result.** Ramp gradient × Deaf and hard-of-hearing people: `provisional`, marker `○`, maximum 5 %, 27 governing sources, 35 governing extractions. `select x.identity_code, count(*) from specification_extraction_links l join source_value_extractions x using(extraction_id) where l.role='governing' …` on the `BLIND` and `ALL` copies returns `[('MOB', 35)]`. The same answer came back for `BLIND`, `ALL`, `MOB` and the access need `A-REACH`; only the hash differs.
- **Checks on that copy.** `validate_evidence_state.py` → `PASS: 15 records checked`; `derivation_handshake_integrity.py` → `VERDICT: CLEAN`, `determinations: 1`; `extraction_follow_up_audit.py` → `PASS`, `live determinations: 1`.
- **The gate the first pass did not run.** `GUIDEBOOK_DB_PATH=$S/p3_DEAF.db python3 scripts/tests/test_db_integrity.py; echo $?` → `RESULTS: 55/56 checks passed`, `FAILED: [C10] no published cell rests on an unverified or disputed source`, `1`. The same on 3 × `MOB` and 12 × `BLIND`; exit 0 on a copy of `main` and on a `pending` cell (7 × `DEAF`). C10 reads live rows (`scripts/tests/test_db_integrity.py:545-561`) and fires because four governing sources are not `VERIFIED` (`REF-01013`, `REF-01014`, `REF-01016`, `REF-01026` on the 3 × `MOB` copy), which the ledger records as intended (PS:4544). It fires equally for the correct lens, so it is not a test of the lens. **"Passes every gate" was false; this leg ran three checks and generalised.**
- **What the 35 rows are.** Tagged `MOB`; all from T4–T6 instruments (`select e.tier, e.evidence_type, count(*) …` → standards 2, national frameworks 8, codes 25); `device_class` NULL or `not_device_scoped`; none of their `claim_text` mentions a wheelchair. They are regulatory ramp provisions. The first pass called them "wheelchair evidence"; that was wrong.
- **What is contradicted, by warrant class.** OWNER: "No, ALL reaches only an ALL determination" (PS:4657); "Do not store table rows for parameters when there is a missing lens … for when the parameter is not relevant" (PS:4614). LEDGER reading, not owner speech: "a figure reaches a determination only through the lens tags written on that figure, so D-0184 stands" (PS:4630, prefaced at PS:4628 "The readings below are the assistant's and are marked").
- **Against BU.** It reported the mechanism (problem 3) and rated it third. It is first: every determination the engine can write today gathers without regard to lens. BU did not test whether any check could notice, and described the rows as "wheelchair evidence".
- **Against TD.** REQ-073, REQ-074 and REQ-077 quote the same owner message and never state the gather rule; no acceptance test of TD's goes red on this (AT-34 tests only the `ALL` and medical cases).
- [CORRECTION: TD, ledger — add the requirement "a figure reaches a determination only through its own lens tags" (HS-A02), class LEDGER reading of an owner answer.] [CORRECTION: BU, ranking — problem 3 is the worst defect, and it is a contradiction of a ruling, not only a capability fact.]

### F-02 The mobility split was ruled on 2026-08-25 and never executed; every determination, and four-fifths of the judgment rows, sit on the superseded code. Both legs missed it. [VERIFIED]
- PS:1184-1230: "`MOB` is split … not to be relitigated … do not write new `MOB` rows"; PS:1291-1296: "yes, AMB and WHEEL to fan out … `MOB` is superseded". The ruling's own reason is that ramp gradient is opposed between ambulant people and wheelchair users.
- `select identity_code, count(*) from source_value_extractions group by 1` → `MOB` 170 of 214; `select * from base_taxonomy_identity` holds `MOB` active and neither `AMB` nor `WHEEL`; Q1: all eight determinations are parameter 3 × `MOB`, which is ramp gradient.
- `grep -n -E '\bAMB\b|\bWHEEL\b' references/project-standards.md` shows no line after PS:1299 that withdraws, defers or executes it.
- **Against TD.** It lies in PS:1146-2547, which TD read in part. **Against BU.** It used `MOB` as its test lens without asking whether the code is live doctrine (it could not, by its brief).
- The codes and the fate of `MOB` are ratified (PS:1291-1296: "Settles the two questions the split design … put to the owner"; "`MOB` is superseded") and are not to be asked again; the first pass re-asked them and was wrong (FA-14). What is open is narrower: how the figures and grades written under `MOB` since are carried (`select count(*) from source_value_extractions x join evidence_sources e using(ref_id) where x.identity_code='MOB' and e.tier>=4` of them come from T4–T6 instruments, which have no participants to judge by), and how part-time wheelchair users are named in a gap (HS-3 OD-14). All eight stored determinations are already retired.

### F-03 The stage-pair gate and the view mapping the owner ordered on 2026-10-29 do not exist as gates; BU did not find the instrument, TD recorded the requirement as if it stood. [VERIFIED]
- PS:4731 "Yes, register it"; PS:4761 "registered as the stage-pair gate, by one registry entry that fails when a stage pair has no path"; PS:4729 "Yes, map views to a stage".
- `grep -c walkability governance/check-registry.yaml` → 0. `grep -n views governance/stage-map.yaml` → comments only ("STILL OWED"). `python3 workplan/pipeline-state-graph/walkability.py; echo $?` → 0, with `NO PATH` printed for every pair ending at render.
- BU's direction matrix was built by hand from reading; the repository already holds an instrument that computes it from foreign keys and view bodies. BU's self-attack item 6 admits it did not search `workplan/`.
- [CORRECTION: TD, REQ-006 and REQ-017 — status is "ruled, unexecuted", not a standing capability.] [CORRECTION: BU §H — cite `walkability.py` as the derivation; the hand-built matrix is the fallback.]

### F-04 TD's headline "the pipeline contract is … unratified" rests on a stale header. [VERIFIED]
- `sed -n '3p' decisions/DR-2026-07-13-pipeline-contract.md`: "ACCEPTED (doctrine) — owner ratification 'Yes, ratify ALL recent work', 2026-07-21", with an owner-action precondition outstanding. PS:585: "always assume I Ratify if I merge it unless I explicitly note otherwise", whose ACTION is to flip stale `PROPOSED` text.
- TD read neither. It classed every CONTRACT warrant as resting on a `PROPOSED`, `ratified: false` file (TD §0 item 5, §0.1).
- What stands: the contract is forward-only, and its synthesis and specification entries contradict the owner's order (C-11). What falls: "unratified" as a reason to discount REQ-019, REQ-024, REQ-050, REQ-087, REQ-095.
- [CORRECTION: TD §0 item 5, §0.1 CONTRACT class, C-11 — the instrument was ratified on 2026-07-21; the YAML header is the stale text (HS-A06). Later owner rulings still override its content.]

### F-05 TD's "nothing in the prose says … whether a determination varies by jurisdiction" is false in part. [VERIFIED]
- PS:372 (session rule, 2026-04-07): "mechanical cooling capability is required as a designed-in feature … in hot-humid tropical contexts", conditioned on a named list of jurisdictions. PS:381: physics-based parameters "transfer universally", the spatial model "does not transfer to collectivist cultures". `specifications.cultural_claim_anchor` exists for it (`PRAGMA table_info(specifications)`).
- These are LEDGER rules of March–April, not owner quotes, and none makes jurisdiction part of the key. They do say a determination can be conditional on climate and culture, which C-03 should have put to the owner beside its own reading.
- TD disclosed that it read the schema listing (self-attack 5). Its reading "no jurisdiction and no language in the key" matches what that listing shows. The requirement may have been fitted to the schema; treat C-03's reading as unproven.
- [CORRECTION: TD §0 item 2 and C-03 — add the climate and cultural-context rules as evidence that variation is contemplated; the reading stays an assumption.]

### F-06 TD's "'dynamically' otherwise has no owner gloss" overlooks the statement it cites two lines away. [VERIFIED]
- `sed -n '11p' workplan/pipeline-state-graph/IDEAL-GRAPH.md`: O1 "a walkable pipeline all directions that can dynamically scrape mine organize and sort all relevant information from any source for any parameter regardless of search slug"; O3 "dynamic information collection"; O6 "the less hard coded, the better". TD cited O7 and O8 from the same line.
- Relayed, so thin. But the gloss it gives is collection across every parameter whatever the slug, with as little code as possible, and the statements of 2026-11-12 say the same (PS:5224, PS:5226, PS:5262). The brief's D2 ("a run is initiated for an arbitrary request cell") is the assistant's decomposition; the owner's own "dynamic" is about deriving, defining, collecting and finding. Section 3.9's request object is therefore further from the owner's words than TD said.
- [CORRECTION: TD §0 item 3, C-08, C-18 — cite O1, O3, O5, O6 and the 2026-11-12 statements; O6 supports "data, not code" where TD said only rule 8 did.]

### F-07 TD's ledger is short by at least eighteen requirements, most from the span it did not read. [VERIFIED for each line cited]
Listed with verdicts in HS-1 §2 (HS-A01 to HS-A18). The ones that change the plan: the mobility split (PS:1184); the lens-tag gather rule (PS:4630); "Ensure that medical gets filled out" (PS:2863); the research-target registry (PS:1967); the three building tables (PS:2056); merge implies ratification (PS:585); harm asymmetry for conflicts between groups (PS:210); freshness and currency (PS:539); the rendered-document gate (PS:588); design scale and the Person-Mode hand-off (PS:170-221). TD also omits the chain behind REQ-072: "exactly one" lens per row (2026-08-28, PS:2493 block) → "at least one" (D-0182) → "each relevant model" (PS:4614).
- [CORRECTION: TD §1 — add HS-A01 to HS-A18; record the three-step supersession under REQ-072.]

### F-08 TD is inconsistent with itself in four places. [VERIFIED by reading TD]
1. **AT-04 against REQ-084.** AT-04: "No table at … render holds an author name, a title, a DOI or a year." REQ-084: the render table holds "complete prose, bibliographic information". Both cannot pass unless the render table is a derived cache; that is OW-1c, unanswered.
2. **§3.6 cold entry against REQ-074.** "Where evidence is insufficient it answers with a pending determination and a gap" against "no row at all for a lens the parameter is not relevant to" and the ledger reading "none for a lens that no figure carries" (PS:4630). TD names the conflict (C-13) and still writes both as requirements.
3. **REQ-012 is marked [R].** The three rules at the head of TD §3 are each labelled as ruled; rule 1 ("re-entry adds, it never rewrites") stands on REQ-012, which TD's self-attack 3 calls session reasoning the owner did not make. The live writers do the opposite at three edges (HS-1 REQ-012).
4. **REQ-096.** "Authored at the Opus floor" where the ledger says "Opus-class or above, which includes Fable-class" (PS:608).
- [CORRECTION: TD AT-04 — conditional on OW-1c.] [CORRECTION: TD §3 head — rule 1 is [I], not [R].] [CORRECTION: TD REQ-096 — class wording per PS:608.]

### F-09 BU reports grep-derived "no reader" lists as VERIFIED, against a standing rule. [VERIFIED]
- PS:663: "Do NOT use grep … to establish it, and do not report a hit count as a finding." BU §G.3 and §G.5 rest on `grep` for names, and §G.5 concedes over-reporting.
- Re-derived for the views by SQL shape rather than name: `grep -rn -E '(FROM|JOIN)\s+v_(best_practice|determination_provenance|item_provenance|pending|divergence|code_floor_only|source_reach_all)' --include=*.py --include=*.html --include=*.js scripts schemas .claude workplan` → no line. The finding stands for views. It is still a text search, so INFERRED.
- [CORRECTION: BU §G.3, §G.5 — status INFERRED; §G.5 (verbs whose output nothing reads) is not established.]

### F-10 BU says the quote normaliser is "correct for … kana". It is not. [VERIFIED on the live function]
- `import retrieval_log; retrieval_log.normalise_quote('スロープ')` → `'スローフ'`. NFKD splits the voicing mark from the kana and the function drops combining marks, so プ, ブ and フ collide, as do が and か. Hebrew pointing and Greek tonos go the same way.
- Confirmed on the live function, where BU used a copy: the two Hindi sentences BU tested normalise identically (`रपकढलन112सअधकनह`); Thai tone and vowel marks are dropped; Arabic-Indic digits are not folded.
- Consequence: the write-time verbatim check (CLAUDE.md §5(c)'s artefact) accepts a misquote differing only in vowel signs or voicing in Devanagari, Bengali, Thai, Arabic, Hebrew and Japanese kana.
- [CORRECTION: BU §D.3, §D.5 — strike "kana" from the scripts handled correctly; add kana voicing, Hebrew and Greek marks.]

### F-11 BU's inference about the blocking specification validator is now observed. [VERIFIED]
- `GUIDEBOOK_DB_PATH=$S/live.db python3 scripts/validate_evidence_state.py` → `OK cell-state machine: 8 cells, 5 convergence rows`, `PASS: 13 records checked`, `EXAMINED: 13`, exit 0. All eight cells are retired (Q1). `run_checks.py` cannot see this: the examined count is non-zero.
- [CORRECTION: BU §F row "validate_evidence_state" — result VERIFIED, not INFERRED.]

### F-12 BU ranks "render does not exist" first without the two facts that change what it means. [VERIFIED]
- `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md` §1: "The render apparatus was deleted (`ea8b9635`, RULINGS R1, 2026-10-14): the owner's target is dynamic rendering from the database." Absence is the ruled state, not decay.
- `workplan/2026-10-30-ramp-spec-pages/RENDER-CONTRACT-parameters-3-and-12.md` (DRAFT, unratified) already specifies elements E0–E16, rules C1–C11 and invariants I1–I6 against live columns, and names its own blockers (E2.scope: no table holds the jurisdiction scope; E8: `gaps` has no parameter key). `workplan/2026-10-23-pipeline-resolution-workplan.md` holds tasks T-1 to T-7.
- The defect is the missing replacement and two unanswered owner prompts (OW-1b, OW-1c), not missing code. A plan that restates either document breaches the 2026-08-19 rule to search for existing work first (PS:636-639).
- [CORRECTION: BU §0 problem 1, §E — state that render was deleted on ruling and that a draft contract exists.]

### F-13 A provincial code is stored under its country. [VERIFIED]
- `select ref_id, jurisdiction, pub_title from evidence_sources where pub_title like '%Ontario%'` → `REF-01013`, `CA`, "Ontario Building Code — O. Reg. 163/24, s.3.8.3.4 Ramps". The enum has no sub-national member. A comparison table (REQ-069) would print Ontario's value as Canada's, beside or instead of the national model code.
- TD named sub-national instruments as a gap (C-03); neither leg found the live case.

### F-14 The research scope is in no table, and the view that says what is owed owes what the owner scoped out. [VERIFIED]
- `select count(*), sum(scope_status is not null) from lang_jur_map` → 70, 0. `select count(*) from v_research_scope` → 70. The view's own comment: a NULL scope "is owed".
- OR-12a (PS:4696) scoped out Arabic, Bengali, Hindi and Swahili; P1+P2+P3 (PS:5026) names 24 codes. Neither is data. BU reported the NULLs as "nothing refuses on it"; the stronger statement is that `db.py coverage` asks for research the owner forbade (PS:4295-4297).
- TD's set arithmetic for C-06 reproduces: bucket-only `['UN']`; P-only `['BE','CH','CN','DK','IT']`.

### F-15 Ids collide between separate scratch copies of one base, not between cells. [VERIFIED; amended, FA-09]
- The first pass said "the engine cannot determine two cells independently" and that "dynamic" meant "one cell per merged pull request". That was wrong.
- Four cells determined one after another on **one** scratch copy (3, 12, 4, 9 × `MOB`) took `specification_id` 9, 10, 11, 12 and gaps `GAP-103`, `GAP-104`; `python3 scripts/research/emit_batch_sql.py --scratch $S/multi.db --out $S/multi_batch.sql` wrote one delta of inserts with no update or delete.
- Each single-cell run on a **separate** fresh copy took `specification_id` 9, and each `pending` one `GAP-103`. That is true of any id a `db.py` verb allocates on a scratch copy; the engine's emitted header says to regenerate against the canonical database before replay (`scripts/assess/assess_cell.py:2183-2187`).
- Not tested by any leg: whether two separately captured copies fail at replay (`emit_data_migration.py`, `migrate_db.py` were not run).

### F-16 Independence: what each breach could have biased.
- **TD** read `dossier/26` and the table, key and view listings of `dossier/30` (row counts, no render writer, which tables are empty). Likely effects: C-01 and §3.7 are firmer about render's emptiness than prose alone supports; the C-03 reading matches the schema (F-05); REQ-071 names columns it saw.
- **BU** saw two ledger lines and the owner sentences quoted in the contract's `references:`. No finding traces to them.
- **This leg** read both in full before verifying, so it is not independent of either; its checks are re-runs and fresh tests, and its additions come from the ledger span and from `workplan/`.

### F-17 TD's five weakest warrants (for any antagonist to attack first).
1. REQ-003 (re-entry): a ledger paragraph adopting an antagonist finding; no owner sentence. Now partly relieved by PS:5222, which says "all directions at any stage" and still does not say what a backward run is.
2. REQ-008 and the strong form of REQ-016: an assistant's memory notes (`owner-rules/project-end-goal.md:15`, `contract-traceability-invariant.md:10`), verified to exist, not owner speech.
3. REQ-005: relayed, unrecorded (IG:11). The 2026-11-12 ledger entry records the objective but not O1–O8.
4. REQ-012: session reasoning; contradicted by live writers; the owner's rule is "do not copy", which is not "never update".
5. §3.9 (request object, five answer verbs) and REQ-071: assumptions; D2 itself is the assistant's.
Also: the C-03 reading; C-09's "evidence stage" reading (the ledger marks it `[ASSUMPTION]`, PS:4999).

### F-18 BU's blind spots.
- No blocking check run (`migration_reproducibility`, `test_db_integrity`, `schema_reference_audit`, `research_dod_session`); `validate_evidence_state` now run here.
- No negative test run by the leg; no verb exercised on a scratch copy except the engine; no capture → migration → rebuild round trip. The repository itself holds seeded-defect tests the leg did not find, covering four of the five other defects this leg first proposed to seed (a retired row surfaced by a view has none): `scripts/tests/test_validate_evidence_state_2_4.py` (run here: eleven seeded defects caught, `ALL PASS`), `scripts/tests/test_evidence_cell_state_2_3.py:221`, `scripts/tests/test_assess_cell_pilot.py:843-858` (run here: `PASS: all pilot-engine branch tests`). None seeds a wrong-lens determination.
- `assess_cell.determine` read to line 1598 of about 1770; `classify`, `derivation_handshake`, `_confirmed_bands` unread.
- Skills unread except `run-pipeline`. Now measured: `skill_vocabulary_audit` → `FAIL: 76 token(s) in 18 file(s)`; `multilingual-research` names `best_practice_synthesis`, `co1_pass_summary`, `jurisdiction_coverage`, `native_aliases`; `cross-population-conflict-mapper` teaches `DBL, MCAS, NEU, OFS, POTS, SENS, VIS`. The two skills that operate D3 research and conflict mapping presuppose structures and codes that no longer exist.
- `workplan/` and hooks unread (F-03, F-12).
- Scan data read as a debt count only. Missed: every scan is `method='pre-screen'`, none `full-read`, no open pass done (HS-1 §5.2).

### F-19 Things both legs missed.
| Item | State | Status |
|---|---|---|
| A question raised at a rendered cell that sends work back to judgment | no table, column or verb; nearest carriers are `determination_gates` (identity lens only, fixed verdict vocabulary, tier `NOT NULL`) and `adversarial_findings(subject_table, subject_key)` | VERIFIED (DDL) |
| The request itself | no row; a session's `commands.jsonl` is the only trace | VERIFIED |
| Design scale as part of a cell | `design_scale` CHECK (`universal`, `population`, `person`); engine output `universal` for an identity cell | VERIFIED |
| Time as a cause of re-entry (code reissued, freshness window passed) | columns never populated | VERIFIED columns; UNVERIFIED for `validate_temporal` |
| Language tags | two-letter, mixed case, no script or region subtag; `ZH` paired with `CN, SG` only while aliases carry `TW`; `NO` unsplit | VERIFIED (`select language, group_concat(jurisdiction) from lang_jur_map group by 1`) |
| Number formats | `claimed_value` holds `30,0`, `viisi prosenttia`, `0 to 12`, `1:6 to 1:14`; no thousands-separator, foot-inch or fraction handling | VERIFIED |
| Units | `claimed_unit` NULL on 41 of 122 rows for parameter 3; `ratio` and `rise:run ratio` both in use; `degrees` refused | VERIFIED |
| Translated titles | six columns, never written; no verb writes them | BU-VERIFIED |
| The owner queue lags the ledger | `governance/owner-browser.yaml` has no `answered` mark on OR-1c; PS:4922 answers it | VERIFIED |
| A check's own prose contradicts the database | `derivation_handshake_integrity` prints "specifications holds 0 rows … cannot accept a row until a parameter is minted" over 8 rows and 10 parameters | VERIFIED |
| Clause as a unit; parameter families; a finder for relations | absent (HS-1 §5) | VERIFIED |

### F-20 Hand-typed figures.
- **BU**: its front summary carries figures without a query id beside them ("140 (row, class) pairs", "457 of 580", "76 tokens in 18 files", "36 members"); each traces to a command in §D or §F, and each reproduced here. Acceptable under its stated grammar; a reader of the summary alone cannot re-derive them. Its header pins HEAD `64c10e2`; HEAD has moved since (`git log --oneline 64c10e2..HEAD`), touching no code or data (`git diff --stat 64c10e2 HEAD -- scripts schemas data governance` is empty).
- **TD**: quotes "24 countries plus two meta-codes" and "≥8" from doctrine and "14 languages" three ways, with a warning; its own counts are commands and reproduce (`grep -c '^| REQ-'` → 96; `'^### C-'` → 22; `'^- \*\*OWNER DECISION REQUIRED — yes'` → 13; `'^| AT-'` → 49).
- **The brief** this leg was given says "40 runnable queries"; that reproduces (`grep -c '^| Q[0-9]' bu-capability-inventory.md`), the ids running to Q41 with Q4 absent.

---

## 2. Claims re-verified (at least 25 required)

"Same" = this leg's run returned what the leg reported.

| # | Leg | Claim | Method here | Result |
|---|---|---|---|---|
| V01 | BU | Q1: 8 determinations, 0 live, `pilot-3`, all `3xMOB`; six views return 0 | query | same |
| V02 | BU | Q2: 56 tables, 12 empty | per-table count | same |
| V03 | BU | Q3: 10 active parameters, 2 directions, no direction source | query | same |
| V04 | BU | Q5: 203 searches; lens columns and `origin_pass_id` NULL on all | query | same |
| V05 | BU | Q6: gaps addressability NULL 106, NOT-ADDRESSABLE 4; `gap_mining` 0 | query | same |
| V06 | BU | Q7: 12 extractions on unverified sources | query | same |
| V07 | BU | Q8: 105 extractions with no covering reading | query | same |
| V08 | BU | Q9: 59 sources, 57 with an admission edge, 11 with a scan | query | same |
| V09 | BU | Q11: 43 captured tables; 14 not captured, `lang_jur_map` among them | `dbcore.writable_tables` | same |
| V10 | BU | Q12, Q13, Q14, Q15, Q16 | queries | same |
| V11 | BU | Q31: enum has 36 members | import | same |
| V12 | BU | Q32: 70 pairs, 19 languages, 48 jurisdictions, scope NULL on all; 19 pairs over 17 codes unreachable | query + enum | same |
| V13 | BU | Q33: 2382 aliases, 0 with an observation pointer, 996 `TRANSLATION` | query | same |
| V14 | BU | Q34, Q36, Q39, Q40 | queries | same |
| V15 | BU | engine ignores the lens (`assess_cell.py` gather) | read lines 235-322; four lens runs | same; extended to `DEAF`, `ALL`, `A-REACH` |
| V16 | BU | 12 × `MOB`: `provisional ○`, no value | scratch run | same |
| V17 | BU | 7 × `DEAF`: `pending` + `GAP-103` | scratch run | same |
| V18 | BU | `_VALUE_BEARING_NAME`, `_name_tokens` behaviour | live `db` module | same |
| V19 | BU | `normalise_quote` collisions | live `retrieval_log` module | same, and wrong on kana (F-10) |
| V20 | BU | `validate_evidence_state` passes on retired rows | run | confirmed (F-11) |
| V21 | BU | `derivation_handshake_integrity` prints a false sentence | run | same |
| V22 | BU | `verified_scan_integrity` FAIL 140 over 212; `scan_debt` 457 of 580; `skill_vocabulary_audit` FAIL 76 in 18 | runs | same |
| V23 | BU | registry: 75 checks, 30 blocking, 43 advisory, 2 informational | YAML load | same |
| V24 | BU | five contract criteria with `check: null` | YAML load | same |
| V25 | BU | no render code, `parts/` moved, no `site/` or `specs/` | `ls` | same |
| V26 | BU | 72 verbs | `grep -c 'add_parser(' scripts/db.py` | same |
| V27 | TD | the quotations at these cited lines (PS:4385, 4947, 4729, 4731, 4761, 5011, 5019, 5206, 5182, 5184, 5188, 4655, 4835, 2690, 4614, 4991, 3687, 4833, 3540, 4472, 4723, 5194, 4580, 4598, 3737, 3980, 4683, 4657, 4926, 4840, 4844, 3644, 4667, 5126, 4834, 4673, 5204, 5154, 4713, 5076, 5088, 4679, 4396, 4381, 4979, 4843, 4938, 4826 and others) | `grep -n -F`; three that wrap a line read with `sed -n` (PS:1048, 4295, 874) | present, except four references corrected in §5 (FA-26): "5 is three" is at PS:2419; the Fable-class wording at PS:608; "prompts for research to target" at PS:1968; PS:5206 carries different words from PS:5019 |
| V28 | TD | PC:2-3 `PROPOSED`, `ratified: false`; synthesis and specification entries circular | read | same; conclusion corrected (F-04) |
| V29 | TD | IG:11 relays O7 and O8, "none is in the ledger yet" | read | same; O1–O6 overlooked (F-06) |
| V30 | TD | memory notes at the cited lines | `grep -n -F` | same |
| V31 | TD | C-06 set difference | TD's own command | same |
| V32 | TD | C-14: both architecture documents `ACTIVE` and item-coded | `head`; `grep -c -E 'item_code|e-08'` → 6 and 18 | same |
| V33 | TD | its four counts | TD's commands | same |
| V34 | coordinator | four owner statements of 2026-11-12 | `grep -c -F` in the transcript and ledger | present at PS:5222-5228, 5247, 5262 |

### 2.7 Commands used for figures new to this leg

```
# retained artefacts per live source: prints (live, with a file on disk, with a text-extraction or
# extraction record, with only other derived records, with none). A page render or a bibliography
# extract is not a text layer (FA-11).
python3 -I - <<'PY'
import sqlite3, json, glob, os, collections
c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
live={r[0] for r in c.execute("select ref_id from evidence_sources where superseded_by_ref_id is null")}
disk,text,other=set(),set(),set()
for m in glob.glob('retrieval-log/*/manifest.jsonl'):
    for line in open(m,encoding='utf-8'):
        try: r=json.loads(line)
        except Exception: continue
        ref=r.get('ref_id')
        if ref not in live: continue
        a=r.get('artefact') or ''
        p=a if os.path.exists(a) else os.path.join(os.path.dirname(m), os.path.basename(a))
        if os.path.exists(p): disk.add(ref)
        if r.get('derived_from'):
            (text if r.get('derivation_kind') in ('text-extraction','extraction') else other).add(ref)
print(len(live), len(disk), len(text), len(other-text), len(live-disk))
PY
# lens tags of the governing rows of a scratch determination
#   select x.identity_code, count(*) from specification_extraction_links l join source_value_extractions x using(extraction_id)
#   where l.role='governing' and l.specification_id=(select max(specification_id) from specifications) group by 1
```

---

## 3. Corrections, collected

1. [CORRECTION: TD, ledger, add HS-A02 (lens-tag gather rule) and HS-A01 (mobility split).]
2. [CORRECTION: TD §0 item 5 and CONTRACT class, the contract was ratified 2026-07-21; the header is stale.]
3. [CORRECTION: TD §0 item 2 and C-03, climate and cultural-context rules exist; the jurisdiction-neutral reading is an assumption that matches a schema TD had seen.]
4. [CORRECTION: TD §0 item 3, C-08, C-18, O1/O3/O5/O6 and the 2026-11-12 statements gloss "dynamic" and "hard-coded".]
5. [CORRECTION: TD §1, add HS-A03 to HS-A18; record the three-step history of the lens CHECK under REQ-072.]
6. [CORRECTION: TD AT-04, conditional on OW-1c; TD §3 rule 1 is inference; TD REQ-096 wording per PS:608.]
7. [CORRECTION: TD REQ-006, REQ-017, ruled and unexecuted.]
8. [CORRECTION: TD C-17, the objective is now in the ledger (PS:5218-5241); O1–O8 still are not.]
9. [CORRECTION: BU §0, problem 3 ranks first and contradicts PS:4630, PS:4657, PS:4614.]
10. [CORRECTION: BU §0 problem 1 and §E, render was deleted on ruling; a draft contract and a workplan exist.]
11. [CORRECTION: BU §D.3 and §D.5, the normaliser is not correct for kana, Hebrew or Greek marks.]
12. [CORRECTION: BU §F, `validate_evidence_state` result verified by run.]
13. [CORRECTION: BU §G.3 and §G.5, INFERRED; §G.5 not established.]
14. [CORRECTION: BU §H, derive the matrix from `walkability.py`; add that the stage-pair gate is unregistered.]
15. [CORRECTION: BU §A.3 and §F, scans: none is a full read and no open pass is recorded.]

## 4. What this leg could not read or run

_Added by the resolution pass:_ `test_db_integrity`, `validate_verification_consistency`, `adjudication_integrity`, the three test files named in F-18 and `emit_batch_sql.py` were run on scratch copies. The stress run then exercised `emit_data_migration.py`, `migrate_db.py --rebuild`, `run_checks.py --selftest` and `run_checks.py --changed-from origin/main --explain` on scratch copies (HS-5 B-38, B-40, B-54). Round 3 ran every battery (`--battery <name> --all`): all PASS (HS-5 B-82). Still not run by anyone: `run_checks.py --all` in one call; `research_dod_session` with a session set. Not established: which retained artefacts are a source's full text; whether the workplan's task order (T-1a → T-2 → T-3) is forced or only planned.


- `sessions/` was not read; searches there were by `grep -r` on chosen terms only. No ruling is reported absent on that basis.
- `governance/evidence-methodology.md`, `time-model.md`, `tier-system.md`, `conceptual-model.md`: cited sections located by grep, not read through.
- `scripts/db.py` and `assess_cell.py`: the gather functions, the name screens and the verb list were read; the rest was not.
- Not run by this leg: `run_checks.py` in any mode, `migration_reproducibility`, `schema_reference_audit`, `emit_data_migration.py`, `migrate_db.py`, any `db.py` write verb. (`test_db_integrity` and `emit_batch_sql.py` were run in the resolution pass; the stress run exercised the write verbs and the migration tools, HS-5.)
- `origin/ramp-spec-pages-work` (the old static generator) was not fetched.

---

## 5. Resolution record (antagonist pass of 2026-11-12) — the complete record for all four `hs-*` files

Each objection was re-run by this leg on fresh scratch copies (`…/scratchpad/hs2/`) or re-read at the cited lines before disposal. Disposition vocabulary: **upheld** (the objection failed; why), **amended** (how), **withdrawn**, **referred to owner**. Every objection held at least in part; none is upheld against the antagonist.

Tally, by command (run in the folder holding this file):

```
for sev in blocking material minor; do for d in upheld amended withdrawn 'referred to owner'; do printf '%s %s: ' "$sev" "$d"; grep -c -E "^\| FA-[0-9]{2} \| $sev \|.*\*\*$d" hs-adversarial-findings.md; done; done
```

A row with two dispositions (amended, and one part referred or withdrawn) is counted under each.

| FA id | severity | objection (lens) | evidence (this leg's re-run) | disposition |
|---|---|---|---|---|
| FA-01 | blocking | IMP-04's live-only `EXAMINED:` turns blocking checks red on `main` (redness) | `run_checks.vacuity_failure(c,'EXAMINED: 0')` returns a failure string for `validate_evidence_state`, `adjudication_integrity`, `validate_verification_consistency` (all blocking, `min_items: 1`); `scripts/run_checks.py:264-266` returns `FAIL` on it | **amended**: IMP-04 is report-only; the token and the floors are untouched; AT-54 restated |
| FA-02 | blocking | "passes every gate" is false (subject) | fresh copies: 3 × `DEAF`, 3 × `MOB`, 12 × `BLIND` → `test_db_integrity` exit 1, `[C10]`; 7 × `DEAF` (pending) and a copy of `main` → exit 0; four governing sources not `VERIFIED` | **amended**: F-01 retitled and extended; HS-1 §0 and §6; HS-3 §0, R-5, R-6. This leg was wrong. |
| FA-03 | blocking | the four unlinked skills have readers (existence) | `sed -n 71p .claude/agents/antagonist.md`; `grep -n -E 'adversarial-research\|integrity-protocol' governance/pipeline-contract.yaml` → 105, 113, 312, 314; `scripts/audit/claims_docket.py:3,134`; `scripts/validate_verification_consistency.py:94`; `governance/decision-protocol.md:59`; `sync_claude_skills.py --check` names a missing `description:` line as the cause | **withdrawn**: the deletion; HS-1 §7 row removed. This leg was wrong. |
| FA-04 | blocking | "first wave doable now, no owner decision" contradicts its own entries (consistency) | read against IMP-01, 03, 04, 05, 07, 08, 10, 11; `grep -n extra schemas/pipeline_contract.py` → 14, 23, 31, 39 | **amended**: HS-3 §0 and §3 rebuilt; the doable-now list is IMP-02, 03a, 04, 06, 12, 13 (two values), 23, T-1a, T-6a |
| FA-05 | material | IMP-08 drops the workplan chain and the ruled link table (prior work) | PS:4926, 4934-4941 read; workplan T-1a/T-2/T-3 text and §7 read; `grep -rn "def parse_bound" scripts` → `assess_cell.py:624` | **amended**: IMP-08 is T-3 with its chain; IMP-40 added for the link table |
| FA-06 | material | IMP-16 rests on superseded text and proposes what exists (supersession) | PS:4560 read; `grep -n STORED_ANSWER scripts/assess/assess_cell.py` → 1772; `scripts/dbcore.py:406-409`; `test_assess_cell_pilot.py` → PASS | **withdrawn**: IMP-16 |
| FA-07 | material | OD-16 is answered on the record (supersession) | PS:4546 read; workplan WR-2 read | **withdrawn**: OD-16; IMP-08's gate line corrected |
| FA-08 | material | negative fixtures already exist (prior work) | `test_validate_evidence_state_2_4.py` → eleven "caught", `ALL PASS`; `test_evidence_cell_state_2_3.py:221`; `test_assess_cell_pilot.py:843-858`; all three registered, advisory, `tests` battery | **amended**: IMP-10 is the one missing fixture; AT-55 restated; F-18 corrected |
| FA-09 | material | cells do not collide on one copy (redness) | four runs on one copy → ids 9–12, `GAP-103`, `GAP-104`; `emit_batch_sql.py` wrote one delta | **amended**: F-15, HS-1 §0 D2 and REQ-025; IMP-11 and AT-56 **withdrawn**. This leg was wrong. |
| FA-10 | material | the governing rows are not "wheelchair evidence" (fidelity) | on the 3 × `DEAF` copy: tiers 4–6 only; `device_class` NULL 11, `not_device_scoped` 24; `claim_text like '%wheelchair%'` → 0 | **amended**: F-01, HS-1 §6, HS-3 IMP-08; BU §0 problem 3 annotated |
| FA-11 | material | "23 hold a text layer" miscounts (count) | `derivation_kind` per live source: `text-extraction` 17, `extraction` 3, `page-render` 3, `pdf-bibliography` 2, `render` 1; 20 sources with a text-extraction or extraction record; on-disk extensions tallied | **amended**: HS-1 REQ-022, REQ-098, §5.2; HS-3 OD-23, AT-65; the §2.7 comment |
| FA-12 | material | IMP-07 is not the ruled gate and is red on `main` (fidelity) | stage map: render holds `weighting_profile`; instrument prints `NO PATH` on 10 lines; workplan §8 items 6–7; PS:4761 | **amended**: IMP-07 sequenced after a render view; an interim form **referred to owner** (OD-26) |
| FA-13 | material | REQ-074's second example is not a "not relevant" case (fidelity) | parameter 7 is reverberation time; PS:4630 assumption and PS:4648 ACTION read | **amended**: example withdrawn; verdict kept on ramp gradient × `DEAF` with its basis marked inferred; AT-52 restated |
| FA-14 | material | OD-14 re-asks what PS:1291-1296 ratified (owner gate) | PS:1291-1311 read; 107 of the `MOB` figures from tier ≥ 4 (query in F-02); `select count(*), sum(retired_at is not null) from specifications` → 8, 8 | **amended**: OD-14 narrowed; IMP-20 rewritten; F-02's last bullet. This leg was wrong. |
| FA-15 | material | the brief's verb-list grep drops verbs (count) | grep → 59; AST walk → 72 | **amended**: HS-4 Document 7 uses the AST command |
| FA-16 | material | the brief forbids text-search facts and prescribes them; HS-1 marks such facts verified (consistency) | read; registry and stage map re-derived by YAML load; view bodies read for `retired_at` | **amended**: HS-4 §1.1 item 7 reworded and its commands replaced where a structure exists; HS-1 rows given structural evidence or lowered to inferred |
| FA-17 | material | AT-50 and AT-51 pass vacuously after the fix (redness) | parameter 3 tags: `MOB` 116, `SCI` 3, `MS` 2, NULL 1, no `DEAF`, no `ALL`; 3 × `MOB` links 122 figures, 6 not `MOB`; 9 × `ALL` links 12 `ALL` and 4 `MOB` | **amended**: both tests restated on non-empty subjects |
| FA-18 | material | Wave 4 "no gate" and the IMP-17/19 dependency are wrong (consistency) | read | **amended**: HS-3 §3 and the five entries |
| FA-19 | material | IMP-24 reverses what the workplan declines and misdescribes the live column (prior work) | `scripts/db.py:3385-3389`; workplan T-6a and §6 (K-9, K-10); T-6a's done-when counts differ today | **amended**: IMP-24 is T-6a extended to three writers; no back-fill; AT-74 restated |
| FA-20 | material | `--slug`, `reasoning_doc_citations`, `opus_reviewed` have readers (existence) | `assess_cell.py:1963-1969`, `2224-2228`; `git grep -l reasoning_doc_citations -- scripts schemas governance skills .claude`; `scripts/db.py:2947`, `governance/conceptual-model.md:122` | **withdrawn** for `--slug`; **amended** for the other two (sweep-gated candidates) |
| FA-21 | material | the lens-tag rule is classed as owner speech in three files (warrant class) | PS:4628 read | **amended**: HS-1 §0, F-01, HS-3 §0 and IMP-08, HS-4 §0 and Document 2 |
| FA-22 | material | a fourth check examines retired rows; `adjudication_integrity`'s subject is sources (subject) | `validate_verification_consistency` → "5 stated/provisional", `EXAMINED: 5`; `adjudication_integrity` → `EXAMINED: 59`, readiness line "8 determination(s)" | **amended**: IMP-04 names four checks correctly |
| FA-23 | minor | wrong cross-references (existence) | read | **amended** |
| FA-24 | minor | "in two places" is a typed count that disagrees with the table (count) | the file's own command | **amended**: HS-1 §0 |
| FA-25 | minor | `NO PATH` is ten lines; only pending runs allocate a gap (count) | `walkability.py` piped to `grep -c 'NO PATH'` → 10; `gap_register_id` NULL on the 3 × `DEAF` copy | **amended**: HS-1 REQ-006, REQ-025 |
| FA-26 | minor | four line references (fidelity) | `grep -n -F` → 2419, 608, 1968; `sed -n 5206p` | **amended**: HS-1; V27; HS-4 |
| FA-27 | minor | HS-A09's command returns a hit (subject) | the command → `claims_docket.py`; `ls` of the two named gate files fails | **amended**: command replaced |
| FA-28 | minor | OD-22's command lists section names (existence) | run; the prompts are under `decisions` | **amended**: command corrected |
| FA-29 | minor | AT-69's instrument and count (redness) | query → 33 rows in 27 strings | **amended**: AT-69 uses the query |
| FA-30 | minor | OD-04 omits the owner's later answer (supersession) | `grep -n -F 'Yes it is P1+P2+P3'` → 4835, 5026 | **amended**: OD-04 carries it and asks only what it covers |
| FA-31 | minor | "all three are tooling" (consistency) | read | **amended**: HS-3 §0 |
| FA-32 | minor | `v_item_provenance` is not a subset (subject) | view bodies read; on the four-cell copy the two views return different counts | **withdrawn**: the deletion |
| FA-33 | minor | brief: "three audit files"; appends after a closed round; scratchpad outputs (consistency) | read | **amended**: HS-4 §0, §2 order, §1.1 item 8 |
| FA-34 | minor | `re_entry:` is a code change (existence) | `grep -n extra schemas/pipeline_contract.py` | **amended**: IMP-03 split |

---

## 6. Resolution record, confirmation pass (`fa-confirmation.md`)

The antagonist's confirmation found the amended files accurate enough to build on and listed rows marked inaccurate (count: `grep -c '^|.*| inaccurate |' fa-confirmation.md`; by severity `grep -c '| material |$'` and `grep -c '| minor |$'` on the same file). Each was re-run or re-read by this leg. All held. Tally of this table: `grep -c -E '^\| K-[0-9]{2} \| material ' hs-adversarial-findings.md`, and the same with `minor`.

| # | severity | row of `fa-confirmation.md` | re-run evidence | disposition |
|---|---|---|---|---|
| K-01 | material | D-04: IMP-12 still orders "DELETE `gap_mining`" | `git grep -l gap_mining -- scripts schemas governance skills .claude ':(exclude)scripts/migrations'` returns the registry, two test files, two graph scripts, `db.py`, `dbcore.py`, a skill and governance files | **amended**: HS-3 IMP-12, HS-1 §7 |
| K-02 | material | S5: FC §4 incomplete | read against the 28 rows | **amended**: FC §4 rebuilt row by row |
| K-03 | material | D-12: AT-53 not restated | read | **amended**: AT-53 states the ruled gate |
| K-04 | material | D-05: IMP-40 and §0 cite an order the ledger does not state | PS:4934, PS:4938 re-read | **amended**: marked as this leg's sequencing in HS-3 IMP-40, §0, and FC C-07 |
| K-05 | material | D-08: "already seeds the other defects" | `grep -rn "v_best_practice\|v_pending" scripts/tests` returns a fixture stub only | **amended**: HS-3 IMP-10 and AT-55, HS-2 F-18, FC C-10: four of five; two fixtures missing |
| K-06 | minor | D-02: parameter 12 fails C10 on one source | fresh 12 × `MOB` copy: the R-6 query returns `REF-01016` only | **amended**: HS-1 REQ-024, HS-3 §0 |
| K-07 | minor | D-04: IMP-03a against OD-18 | read | **amended**: OD-18 narrowed |
| K-08 | minor | D-06: AT-76 "For: IMP-16"; FC C-08 on AT-20 | read | **amended** |
| K-09 | minor | D-09: HS-1 REQ-019 calls the collision a defect | read; and the stress run's `crosstopic.005` | **amended**: stated as the property of a scratch copy, with the stress evidence |
| K-10 | minor | D-12: brief's paraphrase of PS:4761 | `sed -n 4761p` | **amended**: HS-4 Document 2 |
| K-11 | minor | D-15: FC C-17 points at commands that are not there | read | **amended**: FC C-17 carries both commands |
| K-12 | minor | D-16: "three permitted searches" against a fourth | read | **amended**: four, the `sessions/` search named |
| K-13 | minor | D-17: Document 3 lacks the 9 × `MOB` run | read | **amended** |
| K-14 | minor | D-20: "three governance files" | the command returns four | **amended**: no number |
| K-15 | minor | D-21: three warrant labels | `sed -n '4542p;4667p'` | **amended**: HS-3 IMP-08, HS-4 §0 and Document 2 |
| K-16 | minor | D-28: Document 2 points at `queue` | YAML load: prompts under `decisions` | **amended** |
| K-17 | minor | D-33: "four rounds"; document 7's ids have no fold round | read | **amended**: six steps, Round 4b added |
| K-18 | minor | S4: Document 4's wave scope | read | **amended**: covers the doable-now table |
| K-19 | minor | S5: FC C-04 "nothing is deleted" and its affected ids | read | **amended** |
| K-20 | minor | S5: FC §3 omits OD-23 and AT-53 from "restated" | read | **amended** |
| K-21 | minor | S6: the §2.7 command prints 23, not 20 and 3 | amended command run: `58 48 20 3 10` | **amended**: the command now tallies the derivation kind |
| K-22 | minor | HS-2 line 22 and §4 stale sentences | read | **amended** |

The one row marked unverifiable (IMP-07's dependency on a mapped render view) is carried as [U] in the entry.
