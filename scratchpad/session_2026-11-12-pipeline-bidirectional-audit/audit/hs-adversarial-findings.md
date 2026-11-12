# HS-2 — Adversarial findings on both legs, with corrections

_Handshake leg, 2026-11-12 (UTC), HEAD `186defb`, `PRAGMA user_version` 125. Every count is given with its command; re-run before relying on any (rule 7a)._

## 0. Verdict first

**Both legs are sound on what they looked at and wrong, or silent, on what decides the objective.** The bottom-up leg's measurements reproduce: every query and engine run re-executed here returned what it reported. The top-down leg's quotations are accurate: every quote checked sits at the cited line. The failures are of reach:

1. **Neither leg caught that the engine contradicts two live owner rulings on who a determination is for** (F-01, F-02). BU saw the mechanism and could not know the ruling; TD knew a ruling of the same message and did not carry its operative clause.
2. **TD did not read the ledger span that fixes the key, the lenses and the mobility split**, and its ledger is short by at least eighteen requirements (F-07). Three of its headline sentences are wrong as written (F-04, F-05, F-06).
3. **BU never opened `workplan/`**, so it missed the walkability instrument the owner ordered registered, the draft render contract, and the reason render is absent (F-03, F-12). It ran none of the blocking specification checks; one of its inferences about them is now confirmed by run, and one of its "correct" findings is wrong (F-10).
4. **No test in either leg could go red.** Every result is a positive observation. The one negative test run here (a determination for the wrong population, pushed through three checks) passed green (F-01).

**Canonical database hash.** `sha256sum data/guidebook.db`:
- before this leg's first command: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d`
- after seven engine runs on scratch copies and every audit run above: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d`
- at the end of this leg: recorded in the hand-back; unchanged at the time this file was written.

All stress tests ran on copies under `/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/hs/`. Audits were pointed at a copy with `GUIDEBOOK_DB_PATH` inline. No repository file other than the four `hs-*.md` outputs was written; no git command that changes state was run.

Counts in this file: findings `grep -c '^### F-' <this file>`; corrections `grep -c '\[CORRECTION' <this file>`; claims re-verified `grep -c '^| V[0-9]' <this file>`.

---

## 1. Findings, worst first

### F-01 A determination for the wrong people passes every gate. Both legs missed that it contradicts a ruling. [VERIFIED]
- **Run.** `cp data/guidebook.db $S/p3_DEAF.db; python3 scripts/assess/assess_cell.py --db $S/p3_DEAF.db --emit-sql $S/p3_DEAF.sql --parameter-id 3 --slug accessible-circulation-geometry --identity DEAF --session session_2026-11-12-hs-stress --stamp '2026-11-12 04:00' --report-json $S/p3_DEAF.json`
- **Result.** Ramp gradient × Deaf and hard-of-hearing people: `provisional`, marker `○`, maximum 5 %, 27 governing sources, 35 governing extractions. `select x.identity_code, count(*) from specification_extraction_links l join source_value_extractions x using(extraction_id) where l.role='governing' …` on the `BLIND` and `ALL` copies returns `[('MOB', 35)]`. The same answer came back for `BLIND`, `ALL`, `MOB` and the access need `A-REACH`; only the hash differs.
- **Gates on that copy.** `validate_evidence_state.py` → `PASS: 15 records checked`; `derivation_handshake_integrity.py` → `VERDICT: CLEAN`, `determinations: 1`; `extraction_follow_up_audit.py` → `PASS`, `live determinations: 1`.
- **Ruling contradicted.** PS:4630: "a figure reaches a determination only through the lens tags written on that figure, so D-0184 stands"; PS:4657: "No, ALL reaches only an ALL determination"; PS:4614: "Do not store table rows for parameters when there is a missing lens".
- **Against BU.** It reported the mechanism (problem 3) and rated it third. It is first: every determination the engine can write today is of this kind. BU did not test whether any check could notice.
- **Against TD.** REQ-073, REQ-074 and REQ-077 quote the same owner message and never state the gather rule; no acceptance test of TD's goes red on this (AT-34 tests only the `ALL` and medical cases).
- [CORRECTION: TD, ledger — add the requirement "a figure reaches a determination only through its own lens tags" (HS-A02), class LEDGER reading of an owner answer.] [CORRECTION: BU, ranking — problem 3 is the worst defect, and it is a contradiction of a ruling, not only a capability fact.]

### F-02 The mobility split was ruled on 2026-08-25 and never executed; every determination, and four-fifths of the judgment rows, sit on the superseded code. Both legs missed it. [VERIFIED]
- PS:1184-1230: "`MOB` is split … not to be relitigated … do not write new `MOB` rows"; PS:1291-1296: "yes, AMB and WHEEL to fan out … `MOB` is superseded". The ruling's own reason is that ramp gradient is opposed between ambulant people and wheelchair users.
- `select identity_code, count(*) from source_value_extractions group by 1` → `MOB` 170 of 214; `select * from base_taxonomy_identity` holds `MOB` active and neither `AMB` nor `WHEEL`; Q1: all eight determinations are parameter 3 × `MOB`, which is ramp gradient.
- `grep -n -E '\bAMB\b|\bWHEEL\b' references/project-standards.md` shows no line after PS:1299 that withdraws, defers or executes it.
- **Against TD.** It lies in PS:1146-2547, which TD read in part. **Against BU.** It used `MOB` as its test lens without asking whether the code is live doctrine (it could not, by its brief).
- Population taxonomy is owner-gated; the ruling exists, its execution details (whether `MOB` survives as an additive tag; part-time wheelchair users) were left to "owner confirmation". OWNER DECISION REQUIRED (HS-3 OD-14).

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
4. **REQ-096.** "Authored at the Opus floor" where the ledger says "Opus-class or above, which includes Fable-class" (PS:609).
- [CORRECTION: TD AT-04 — conditional on OW-1c.] [CORRECTION: TD §3 head — rule 1 is [I], not [R].] [CORRECTION: TD REQ-096 — class wording per PS:609.]

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

### F-15 The engine cannot determine two cells independently. [VERIFIED]
- Seven scratch runs for seven different cells each allocated `specification_id` 9, and the pending one `GAP-103`. BU found this with two; it is general. Until ids are allocated at capture or replay, "dynamic" means one cell per merged pull request.

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
- No negative test anywhere; no verb exercised on a scratch copy except the engine; no capture → migration → rebuild round trip.
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
| V27 | TD | the quotations at these cited lines (PS:4385, 4947, 4729, 4731, 4761, 5011, 5019, 5206, 5182, 5184, 5188, 4655, 4835, 2690, 4614, 4991, 3687, 4833, 3540, 4472, 4723, 5194, 4580, 4598, 3737, 3980, 4683, 4657, 4926, 4840, 4844, 3644, 4667, 5126, 4834, 4673, 5204, 5154, 4713, 5076, 5088, 4679, 4396, 4381, 4979, 4843, 4938, 4826 and others) | `grep -n -F`; three that wrap a line read with `sed -n` (PS:1048, 4295, 874) | all present |
| V28 | TD | PC:2-3 `PROPOSED`, `ratified: false`; synthesis and specification entries circular | read | same; conclusion corrected (F-04) |
| V29 | TD | IG:11 relays O7 and O8, "none is in the ledger yet" | read | same; O1–O6 overlooked (F-06) |
| V30 | TD | memory notes at the cited lines | `grep -n -F` | same |
| V31 | TD | C-06 set difference | TD's own command | same |
| V32 | TD | C-14: both architecture documents `ACTIVE` and item-coded | `head`; `grep -c -E 'item_code|e-08'` → 6 and 18 | same |
| V33 | TD | its four counts | TD's commands | same |
| V34 | coordinator | four owner statements of 2026-11-12 | `grep -c -F` in the transcript and ledger | present at PS:5222-5228, 5247, 5262 |

### 2.7 Commands used for figures new to this leg

```
# retained artefacts per live source (48 / 23 / 10 of 58)
python3 -I - <<'PY'
import sqlite3, json, glob, os, collections
c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
live={r[0] for r in c.execute("select ref_id from evidence_sources where superseded_by_ref_id is null")}
disk,derived=set(),set()
for m in glob.glob('retrieval-log/*/manifest.jsonl'):
    for line in open(m,encoding='utf-8'):
        try: r=json.loads(line)
        except Exception: continue
        ref=r.get('ref_id')
        if ref not in live: continue
        a=r.get('artefact') or ''
        p=a if os.path.exists(a) else os.path.join(os.path.dirname(m), os.path.basename(a))
        if os.path.exists(p): disk.add(ref)
        if r.get('derived_from'): derived.add(ref)
print(len(live), len(disk), len(derived), len(live-disk))
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
6. [CORRECTION: TD AT-04, conditional on OW-1c; TD §3 rule 1 is inference; TD REQ-096 wording per PS:609.]
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

- `sessions/` was not read; searches there were by `grep -r` on chosen terms only. No ruling is reported absent on that basis.
- `governance/evidence-methodology.md`, `time-model.md`, `tier-system.md`, `conceptual-model.md`: cited sections located by grep, not read through.
- `scripts/db.py` and `assess_cell.py`: the gather functions, the name screens and the verb list were read; the rest was not.
- Not run: `run_checks.py` in any mode, `migration_reproducibility`, `test_db_integrity`, `schema_reference_audit`, the capture and migration tools, any `db.py` write verb.
- `origin/ramp-spec-pages-work` (the old static generator) was not fetched.
