# Antagonist pass 1 — attack on `scratchpad/adjudication.md` (ADJ-01 to ADJ-10)

Read-only. Repository at `origin/main` `71b7c58`; DB opened `mode=ro` (schema read live). Every line number below was read at that commit; locate by the quoted text. Ledger = `references/project-standards.md`.

## Verdicts

| ID | Verdict | One line |
|---|---|---|
| ADJ-01 | WOUNDED | Quotes are verbatim. But the 2026-08-24 ruling RENAMED the layer; it did not retire it. The owner kept the layer as `icf_demands` on 2026-08-25. The retiring act is R35, a delegated ruling. The annotation also cites §5.1–§5.8 numbering the file does not have, and sends to history the one sentence that says Co-1 anchors ●. |
| ADJ-02 | WOUNDED | The annotation's "The schema and converter files of §1.1 no longer exist" is false: `schemas/evidence_source.py` exists. "populations array … (migration 071)" is misattributed. The note also turns a live pipeline-contract anchor into a pointer to history without saying so. |
| ADJ-03 | SURVIVES | (a) holds. (b) holds but leaves out the owner's own OD-63 render words, which bear directly on the question. |
| ADJ-04 | FALSE (proposed order and approval class; the evidence is accurate) | Rank 3 (delegated resolutions) sits above doctrine and CLAUDE.md, which inverts the owner's typed 2026-11-25 words. Rank 2 (a merge counts as approval) has no owner words behind it. The decision-protocol line writes an unratified [ASSUMPTION] exception into §2.4. The DR note misstates §11 property 3 and re-ratifies sections of a DG-NON record. |
| ADJ-05 | SURVIVES | Verified. One wrong line: the rule-10 quote is at `:7583`, not `:7584`. |
| ADJ-06 | WOUNDED | Facts verified. But the 2026-11-20 (third) entry lists rule 9 among the texts "the owner approves", so DELEGABLE is wrong as recorded. "Replace `:208-211`" leaves unclear whether `:211-212` (the `ci.yml` concurrency clause) survives. |
| ADJ-07 | WOUNDED | Says "five sentences" but lists six locations. Says the fixes "go ahead regardless", yet the same ledger entry's ACTION (1) forbids rewriting CLAUDE.md and reserves the tier/Co-1 definitions and rule 9 to the owner. |
| ADJ-08 | WOUNDED | (a)–(d) verified against data and ledger. The intro presents a recorder [ASSUMPTION] as "ACTION (sixth)". (e) invents a merge-as-confirmation route for a one-way, DG-NON population-code retirement. |
| ADJ-09 | WOUNDED | 09a's "T-120 … already carry exactly this" is FALSE for tier-system §8, §9, §10 and the §1 T6 row. 09a presents OD-64's recorder status line as owner words. 09b is not a strict contradiction, its replacement re-pins the floor, and it misses the contract's "Opus-only". 09d's count is wrong. The classes for 09e, 09f, 09h, 09j and 09l contradict the adjudicator's own rule, decision-protocol §2.4 or R30. 09g, 09i and 09k survive. |
| ADJ-10 | WOUNDED | "Tier ladder: conflict only in T3 gloss and type list" is false: Co-2 co-primacy is split across homes. The marker-home list omits the schema CHECK. "The DR note points to it" is false: ADJ-04's DR note points to nothing. |

---

## Per-item detail (worst defects first within each item)

### ADJ-04 — the authority order (FALSE as proposed)

1. **Delegated resolutions placed above doctrine and CLAUDE.md, against the owner's words.**
   - Proposed order: rank 3 is "Delegated resolutions"; rank 4 is "Ratified records — decision records, ledger RULEs, canonical governance documents"; rank 5 is "CLAUDE.md".
   - Owner, typed, 2026-11-25 (ledger `:8485`, under "Owner statements 2026-11-25"): *"as always refer to doctrine/mission/claude.md etc for guidance as required"*.
   - ACTION (4) of the same entry (`:8496`): "A delegate rules against the doctrine and rules the owner has recorded (`governance/mission-and-epistemics.md`, `CLAUDE.md`, `governance/tier-system.md`, `governance/decision-protocol.md`, the ledger)".
   - OD-79 (`:8503`) limits the grant to "decisions of schema, method and ordering that satisfy methods the owner has already ruled".
   - The record therefore puts delegated resolutions BELOW doctrine and CLAUDE.md. The proposed sentence inverts that, and a session reading it would let a delegated resolution override `tier-system.md`.
   - Command: `git grep -n -F "as always refer to doctrine" -- references/project-standards.md`.

2. **Rank 2, "the merge of a pull request whose body names a change as the owner's to approve by merging", has no owner words.**
   - Its only source is a recorder bullet (`:8232`: "the pull request description names it as the part the owner approves by merging") and agent commit messages (`94dbaed`: "Proposed wording: the owner approves it by merging").
   - The (sixth) entry's own reading says the opposite of a merge mandate (`:8557`): "it does not by itself authorise merging a pull request, which the harness reserves to the owner's own ask".
   - Placing this above delegated resolutions creates an approval channel no ruling grants. ADJ-08e then relies on it.
   - Command: `git grep -n -i 'by merging' -- references/project-standards.md governance CLAUDE.md decisions` (one hit, `:8232`, recorder text).

3. **The decision-protocol line promotes an [ASSUMPTION] into a canonical exception to §2.4.**
   - Proposed: "They never reach §2.4 except where the owner's words name the question."
   - The "except" clause is the recorder's reading at `:8556`, marked [ASSUMPTION] and "unratified except where the owner's words state them" (ACTION (4), `:8562`).
   - decision-protocol `:71-73` says these types are "always DG-NON". Adding an exception to the non-delegable list changes the delegation doctrine itself, so it is not DELEGABLE (D-OP). It is OWNER-ONLY (§2.4 item 1 framing; §2.2 D-DOCT DG-NON).
   - The same line also hand-types a list of grants, "grants of 2026-11-13, 2026-11-19 and 2026-11-25". That list:
     - omits the founding "Owner delegation 2026-11-12" (`:5384`);
     - omits "Owner delegation 2026-10-14" (`:4425`) and "Owner ruling 2026-09-11 — adjudication delegated for a named set" (`:2860`);
     - names "2026-11-13", whose heading is an "Owner question" (`:6286`), not a grant.
   - Such a list goes stale with the next grant (rule 7a).
   - Command: `grep -n '^## .*\(deleg\|Deleg\)' references/project-standards.md`.

4. **"(One sentence; replaces one; adds no rule.)" is false.** The order is seven ranks, two of which (2 and the 3-over-4 placement) appear in no ruling. That is new doctrine about authority, inserted beside rule 0. The owner-approves list of the 2026-11-20 (third) entry (`:8209`) names rule 0. Separately, "replace `:20-23`'s sentence" is ambiguous: `:20-21` also carries "This file holds **process, workflow and rules only**; every volatile fact … is derived, never stated", which a literal replacement of lines 20-23 deletes.

5. **The DR note misstates its warrant and re-ratifies a DG-NON record.**
   - Note: "The four-document read-set (§8), "Everything else is superseded" (§A) and §B's "OPERATIVE" rows are spent: §11 property 3 already says so".
   - §11 property 3 (DR `:636-641`) says only that the successor-prohibition CHECK is spent and "A successor plan is no longer build-rejected". It says nothing about §8 or §A.
   - The note then declares "What still binds here: §1.4 (items as leads), §7, … §12.0 as amended, and §4's acceptance criterion".
     - That is a fresh list of binding sections, written by an agent into a decision record whose header reads "**Delegation:** DG-NON — work-product inclusion/exclusion and trajectory are owner-only" (DR `:87-88`).
     - §1.4 rule 1, "No item name becomes a slug by strip" (DR `:178`), was qualified by the owner on 2026-11-06 (`:5019`): "yes, use the 93 items with stripped values as a basis". The note re-asserts it without that qualifier.
   - "the owner has since named the remediation plan as the work" states as fact what `:8491` marks [ASSUMPTION] ("the owner did not name a file").
   - Class: OWNER-ONLY, not DELEGABLE.

6. **ADJ-10 says "ADJ-04: one sentence in CLAUDE.md, the DR note points to it".** ADJ-04 item 3's text contains no pointer to the CLAUDE.md sentence. It restates. That makes two homes, the CLAUDE.md order and the DR note, plus a third restating OD-79's reach in decision-protocol (rule 5).

7. **Item 2, the `:538` replacement, duplicates `:539`.** `:539` already routes "Latest rulings | the tail of `references/project-standards.md`". A second row pointing at the same tail is a second home. The smaller fix is to delete row `:538` or point it at `:539`.

Evidence check: the DR quotes at `:3`, `:17-25`, `:48`, `:89-92`, `:323-329`, `:563`, `:578`, `:593`, `:601` and `:636-641` and the CLAUDE.md quotes at `:20-23` and `:538` are verbatim. The quote at `:7243` splices the ledger HEADING ("fold the term-resolution plan into the remediation plan") into the owner's words, which are "fold plan into remediation plan and ensure they are commensurate with this newest plan having priority in conflicts" (`:7247`). Minor, but the fragment inside the quote marks is not the owner's.

Minimality: the conflict the item proves (CLAUDE.md `:538` routes to a spent plan) is closed by deleting that row. The rank list, the DR note and the decision-protocol line are over-reach.

### ADJ-09 — the twelve smaller items, each re-verified

- **09a — WOUNDED (HIGH).**
  - Quotes `:7195`, `:7265` and `:7327` are verbatim, as is the tier-system `:64-66`, `:90-94`, `:98`, `:100` and `:113` staleness.
  - The claim that fails: "T-120 item 2a … and T-117 … already carry exactly this … Recommend running T-120." T-120 item 2a (`workplan/2026-11-12-bidirectional-pipeline/tasks/T-120-doctrine-amendments-and-deletions.md:68`) names, for tier-system, only "`governance/tier-system.md` §5 and the line that lists markers". The TERM plan row for tier-system (`TERM-RESOLUTION-PLAN.md:41`) names lines 20 and 21 only.
  - So these stay stale after T-120: §8's band table `:90-94`; `:96`; `:98`; `:100` ("a cell whose entire basis is T4–T6 takes ○", which contradicts "T4 only half circle"); §10 `:113`; the §1 T6 row `:22`.
  - §9 `:105` ("Scoping reviews … → T3 … supporting (● band)"; T3 is ◐ under OD-57) is not listed by the adjudicator at all.
  - Separately, "OD-64: triangle for every grey basis" is presented as the owner's words. It is the recorder's status line (`:7424`). The owner typed "2 triangle for all" (`:7401`), and "for all is read as every grey basis" is an [ASSUMPTION] (`:7414`). The interim note covers only §5's heading.
  - Commands:
    - `sed -n '68p' workplan/2026-11-12-bidirectional-pipeline/tasks/T-120-doctrine-amendments-and-deletions.md | grep -o 'tier-system.md. §5[^;]*'`
    - `grep -n 'supporting (● band)' governance/tier-system.md`
- **09b — WOUNDED (MEDIUM).**
  - The owner's words at `:609` are verbatim.
  - But the rule entry's own ACTION (3) (`:608`) reads the floor as "Opus-class or above, which includes Fable-class", and `:604` records that "`fable` and `opus` satisfy the `best_practice_synthesis` floor". On the record's reading, "Only Opus-class" is narrow wording, not a contradiction.
  - The replacement "(`opus` or `fable`, decision-protocol §4.2)" closes the class list. ACTION (4) says "Do not re-pin the floor to whatever model is current".
  - It also adds a fact ("writes a determination (`specifications`)") that T-120 item 3 already owns. ADJ-09b and T-120 item 3 would then both edit CLAUDE.md `:381-382` (collision).
  - Missed homes: `governance/pipeline-contract.yaml:275` "Opus-only (rule #2)" (a true contradiction of "can be fable as well") and `:281`.
- **09c — SURVIVES, one omission.**
  - Mission `:42-46` and `:177`, evidence-architecture `:121` and the OD-48 quote at `:7995` are verbatim.
  - The [UNVERIFIED] is resolvable: T-120 `:67` reads "`governance/mission-and-epistemics.md` (commitment 2 and Test 3 point to §0 …", so T-120 does reach test 3.
  - L6 contrary record not cited: the Unification entry (`:7958`) already decided that the RULE "Universal design is co-extensive with code compliance" "is not superseded: no owner word of 2026-11-14 contradicts it". The owner question about commitment 5 should name that earlier finding.
- **09d — WOUNDED (LOW).** "delete the four version numbers". decision-protocol `:5` carries three ("Sonnet 4.6", "Opus 4.6", "Opus 4.6"). A hand-typed count, wrong (rule 7a).
- **09e — SURVIVES.** Verified with `git ls-files | grep co0007` (both under `workplan/_superseded/`). Class: the adjudicator's own `:7` says "Doctrine files remain the owner's to merge"; mission is doctrine, so DELEGABLE contradicts that for the two mission paths. Missed caller: `governance/doctrine-recheck.md:5` and `:306` cite the same dead path (OM-08).
- **09f — SURVIVES on facts** (`:92`, `:112`, `:131`, `:153`, `:155` verbatim). Class: evidence-architecture is CANONICAL doctrine (`:246`), so by the adjudicator's own `:7` it is an owner merge, not DELEGABLE.
- **09g — SURVIVES.** `:593`, `:594`, `:5520` and `:5971` are verbatim.
- **09h — SURVIVES on facts** (mission `:99`; `schemas/enums.py:112-120`). The pointer to `enums.py` is right because `evidence_sources.evidence_type` carries no CHECK (read live), so rule 8's CHECK-first rule has nothing to read. Class: it edits the mission file, so DELEGABLE contradicts the adjudicator's `:7`.
- **09i — SURVIVES.** decision-protocol `:73-84` and CLAUDE.md `:501-502` are verbatim. (The list sits at `:501-502`; `:503` is the next bullet.)
- **09j — WOUNDED (MEDIUM, class FALSE).**
  - Facts: CLAUDE.md `:369` and tier-system `:19` verified.
  - Class: the edit changes the stated definition of a tier. decision-protocol §2.4 item 3 ("Evidence-tier definitions") is always DG-NON, and the 2026-11-20 (third) entry (`:8209`) says "The owner approves … the tier and Co-1 definitions". It is OWNER-ONLY, not DELEGABLE.
  - The replacement also leaves the Co-2 omission on the same line untouched (OM-03).
- **09k — SURVIVES.** `ls … | tail -1` prints `v10_9`; `sort -V` prints `v10_14`.
- **09l — WOUNDED (LOW).** The facts hold (`max(decision_id)` D-0188, D-0170 `ACTIVE`, R30 at RULINGS `:72`). R30 itself allocates the decision-protocol edit as "agent; decision-protocol §5 owner merge". DELEGABLE contradicts the ruling the item rests on.

### ADJ-01 — the axis layer (WOUNDED)

1. **The 2026-08-24 ruling is mischaracterised (L2).**
   - The ledger RULE (`:799-806`) says the layer "holds **ICF-anchored access needs**, and must be named for that". The owner's words, "I don't want axis to be used", are about the NAME.
   - The next day the owner ruled the layer "is renamed **`icf_demands`** … and it is NOT folded into `access_needs`" (`:1103-1105`; DATE `:1142` "owner ruling").
   - So the owner's later words kept the layer under a new name. The executed retirement of the 17-row table is R35 (RULINGS `:248`), a delegated ruling adopted under the 2026-10-14 delegation.
   - The proposed annotation repeats migration 109's header ("retired … again 2026-08-24") and tells the owner that three owner rulings retired the layer. Only R3 (2026-08-18) says "retired". This is also one warrant counted as three (L3).
   - Command: `sed -n '1103,1106p;1142p' references/project-standards.md`.
2. **The annotation's section numbers do not exist.** §5 holds numbered items 1–8, not §5.1–§5.8 (`sed -n '317,367p' governance/functional-taxonomy.md`). A reader cannot find "§5.7" by search.
3. **Co-1 sentence sent to history (L7).** "§5.7" (item 7, `:363-364`) reads "Strength semantics unchanged … Co-1 = tier 1 = eligible to anchor ● claims". The second sentence agrees with OD-57 ("● T1, T2, Co-1, Co-2") and is the only line in the file saying Co-1 anchors ●. The annotation lists all of "§5.7" as history.
4. **§5.6 (non-DOI intake) is in neither list.** It is the route that keeps DPO and oral-history evidence (Co-1) from being filtered out (`:356-362`). The adjudicator left it [UNVERIFIED], and the annotation's silence reads as "history" by elimination.
5. The pair edit to CLAUDE.md `:542` removes the "Entity model" key without a replacement. ADJ-02's note says the live model is `sqlite_master`, and no routing row says so.

Approval class (ALREADY-SETTLED): acceptable for R3's retirement, but the "owner rulings 2026-08-24 and 2026-09-13" clause must not be presented as retirement rulings. Evidence otherwise verified: handoff `:68`, `:89-92`; ledger `:3398`, `:4425`, `:575`, `:567`, `:5927`, `:7688`; migration 109 `:14-15`; staged file absent (`test -e` fails); `axes` and `situations` absent from `sqlite_master`; `identity_icf_map.mapping_confidence` present.

### ADJ-02 — conceptual-model (WOUNDED)

1. **The annotation says "The schema and converter files of §1.1 no longer exist (the converters are under `_archived/scripts/convert/`)".** `git ls-files | grep '/evidence_source.py$'` prints `schemas/evidence_source.py` (ENT-02, `:19`). The adjudicator's own evidence list correctly names five files; the annotation generalises to six (L1).
2. **"the `populations` array is gone (migration 071)".** Migration 071 drops `population_code` (`071_parameter_at_base.sql:9`). The "populations array" was a field of the deleted `specification.py`, not a DB column.
3. **Cross-document consequence not stated.** `governance/pipeline-contract.yaml:286-287`, the specification stage anchor, cites "conceptual-model.md:90 ("BPC synthesis produces specifications"), restored by D-0167" as its authority. The note makes that a pointer into "the A3 sign-off record, not the live entity model". The contract also cites "ENT-02" at `:136`. Neither is named.

Evidence `:25`, `:35`, `:71`, `:81`, `:92` and `:100` is verbatim; migration 107 `:2-6` is verbatim; `_archived/references/README.md:22-23` is verbatim.

### ADJ-08 — open owner questions (WOUNDED)

- Intro: "ACTION (sixth) says the questions are not to be put again before the work goes on." That sentence is the recorder's [ASSUMPTION] at `:8557`, not ACTION (`:8562`), which says only that an Opus-class instance rules and a different instance checks.
- (a) GAP-379 `OPEN`. Rows 53, 57 and 61 (LPA, TALL and BAR, e120) are `pending`. The gap text's last correction says "answered by keeping the rows … (the coordinator's reading, to be confirmed at review)". `base_icf` e120 has title source `access_need_icf.note`. All verified. SURVIVES.
- (b) Rows 13, 14 and 26 are `pending`, warrants "No record read stated this link". Verified. SURVIVES.
- (c) `:8012-8013` and `:8600` verbatim. SURVIVES.
- (d) `:8596` verbatim. The class is correctly OWNER-ONLY (owner meaning, OD-79). SURVIVES.
- (e) **WOUNDED (MEDIUM, L5).**
  - "Smallest course: no question now. The owner's merge of T-102's pull request, whose body names the retirement, is the confirmation (rank 2 of ADJ-04)."
  - The merge route is not in the record (see ADJ-04 finding 2). OD-83 already names its approval-ref as the owner's OI-13 words (`:8608`).
  - The substance is a population-taxonomy act (§2.4 item 2, "always DG-NON"; OD-79 excludes it). It answers OI-77, which the 2026-11-16 correction put to the owner with ACTION (2), "Do not run T-102's retirement of `SCI` before the owner answers OI-77" (`:7727`), and it is one-way ("restoring SCI needs a compensating migration", `:8608`).
  - The widening of the grant to SCI is the [ASSUMPTION] at `:8556`.
  - The adjudicator should say plainly: a delegated resolution closes an owner question on a population code, irreversibly, on a recorder reading. A merge does not cure that.

### ADJ-07 — the CLAUDE.md rewrite proposal (WOUNDED)

- "five sentences in current CLAUDE.md contradict owner words": the list names six locations (`:381-382`, `:372`, `:538`, `:542`, `:208`, `:501-503`).
- "the five one-sentence fixes above go ahead regardless". The entry the item relies on, 2026-11-20 (third), carries ACTION (1) (`:8214`): "Do not rewrite `CLAUDE.md` until the owner approves the content above". It also lists (`:8209`) "The owner approves the goal sentence, rule 0, rule 9, the tier and Co-1 definitions, and the fate of the layer model". The `:372` marker gloss is a tier/marker definition and rule 9 is named, so neither "goes ahead regardless".
- The merge-as-approval premise for `94dbaed` and `53ada81` appears only in "Not reached". It belongs in the verdict.
- Commits verified: `94dbaed`, `9fa3307` and `74e6458` are in `4f12d50^1..4f12d50^2`; `53ada81` is an ancestor of `origin/main`.

### ADJ-06 — rule 9 (WOUNDED, LOW)

- Facts verified: `.claude/settings.json:43-46`; CLAUDE.md `:208-211`.
- `git grep -n -i subscri -- references/project-standards.md` returns nothing (re-run). `workplan/2026-09-23-pr-audit-resolution.md:53` restates "(owner instruction)", not verbatim words.
- Class: rule 9 is on the 2026-11-20 (third) owner-approves list.
- The name-mismatch premise is [UNVERIFIED] here: this subagent's tool list exposes no `claude-code-remote` tools to compare.

### ADJ-03 — mission and "population" (SURVIVES)

- (a) `:40`, `:62`, `:78` and `:101-103` are verbatim; `:7536` is a heading, with the owner's words at `:7540`, verbatim.
- (b) Not cited, and contrary-relevant: the owner's OD-63 words (`:7399`): "on the render page itself, we just have the minimum, mode, median and maximum colour coding the jurisdiction code bodies". This is a render rule by owner words, which bears directly on "median as default", and it makes the "No" branch stronger than the item admits.
- `:6796` is the heading; the quote is at `:6800`.

### ADJ-05 — rule 10 (SURVIVES)

PR 243 is merge `4f12d50`, 2026-11-20, and contains `9fa3307` and `74e6458`. Readings `:8231` and ACTION `:8235` are verbatim. Quote location: `:7583`, not `:7584`. No later ledger line relaxes rule 10 (`awk 'NR>8240 && /rule 10/'` finds only `:8468`, which applies it).

### ADJ-10 — facts with more than one home (WOUNDED)

- "The tier ladder | … Conflict only in CLAUDE.md's T3 gloss (ADJ-09j) and mission's type list (ADJ-09h)". False; see OM-03 and OM-04.
- "The marker table | Homes found" omits the schema home, which rule 8 makes primary: `specifications.marker` CHECK (`marker IN ('●','◐','○') AND (regulatory_stratum_only = 0 OR marker = '○')`). See OM-10.

---

## OMISSIONS

Approval classes follow decision-protocol §2.4 and OD-79.

**OM-01 — tier-system §8, §9, §10 and the §1 T6 row keep the pre-2026-11-14 bands, and T-120 does not reach them.**
- Proof:
  - `governance/tier-system.md:92` "**● Full** | T1, Co-1, T2, Co-2, T3-clinical".
  - `:93` "**◐ Partial** | T4, T5".
  - `:94` "**○ Weak** | T3-grey, T6 …, an unretrievable (`UNVERIFIED`) source".
  - `:100` "a cell whose entire basis is T4–T6 takes ○ even where T4/T5 sources are present".
  - `:105` "Scoping reviews … → T3 … supporting (● band)".
  - `:113` "Firm guidance/white-paper without method → T3-grey (○ weak)".
  - `:22` "T6 anchors a **weak-band (○)**" (consistent as to T6, but still the band vocabulary).
  - Against: OD-57 (`:7327`, the table at `:7265`); "T4 only half circle" (`:7195`); "2 triangle for all" (`:7401`). T-120 `:68` names tier-system "§5 and the line that lists markers" only.
- Fix: T-120 item 2a adds "tier-system §1 T6 row, §8 table and the `:98`/`:100` sentences, §9 `:105`, §10 `:113` point to §5". Until then, one dated note under §8's heading, not only §5's.
- Class: ALREADY-SETTLED-BY-OWNER-WORDS; owner merges (doctrine, §2.4 item 3).

**OM-02 — CLAUDE.md §6, mission and tier-system §5 gloss ◐ as "policy/standards only", and the "Unmarked is an error" list has no ⚠.**
- Proof:
  - CLAUDE.md `:372` "**◐** policy/standards only … Unmarked is an error".
  - mission `:136` "◐ (policy/standards only)".
  - tier-system `:65` "`◐` policy or standards basis only, not primary evidence: T4, T5".
  - Since OD-57, ◐ carries T3 non-grey primary research, which is not policy or standards. ⚠ replaces the circle (U7, `:7876`: "no, triangle instead if the value is coming from grey or unverified"), so a ⚠-only cell is "unmarked" by CLAUDE.md's own sentence.
- ADJ-09a and ADJ-07 call `:372` "the ○ gloss" only. T-120 item 2a's pointer line would cure CLAUDE.md, but the adjudicator never says ◐ is wrong.
- Fix: replace `:372` with "Markers: the table in `governance/tier-system.md` §5 (●, ◐, ○, and ⚠ in place of a circle). Unmarked is an error."
- Class: owner (tier and marker definitions; 2026-11-20 (third) `:8209`).

**OM-03 — Co-2 is not stated as co-primary with T2 in the two homes a session reads first.**
- Proof:
  - The ledger RULE (`:17`) says "Co-2 = OT professional body CPGs (co-primary with Tier 2)".
  - `governance/evidence-architecture.md:42` says "**Co-2** — OT professional-body CPGs, co-primary with T2".
  - `references/methodology-evidence-hierarchy-mapping.md:29` says "Co-primary with Tier 2".
  - Mission `:93` says "parallel to Tier 2".
  - But `governance/tier-system.md:18` (the operative ladder) states no co-primacy, and its T2 row `:17` lists "occasionally `co2` for community-of-professional synthesis", which files Co-2's evidence type inside T2.
  - CLAUDE.md `:369` says only "**Co-2** OT professional-body CPGs", while the same line marks Co-1 "**co-primary with T1**".
  - The owner's 2026-11-26 typed words ("Co-2 is co-primary with tier 2") are [UNVERIFIED]: no committed file carries them. The 2026-07-era ledger RULE already does.
- Fix: CLAUDE.md `:369` "**Co-2** OT professional-body CPGs, **co-primary with T2**"; tier-system `:18` add "Co-2 ranks alongside T2"; delete "occasionally `co2` …" from `:17`.
- Class: OWNER-ONLY (tier definitions, §2.4 item 3), settled by owner words (ledger `:17`, and the 2026-11-26 statement once recorded).

**OM-04 — decision-protocol §2.4 item 3 omits Co-2 from the non-delegable tier definitions.**
- Proof: `governance/decision-protocol.md:77` "Evidence-tier definitions (1–6 + Co-1)". Co-2 is a tier track (ledger `:17`; tier-system `:18`). As written, Co-2's definition is delegable by omission.
- Fix: "(1–6 + Co-1 + Co-2)".
- Class: OWNER-ONLY.

**OM-05 — the pipeline contract pins the synthesis floor to Opus only.**
- Proof: `governance/pipeline-contract.yaml:275` anchor "'best_practice_synthesis / ISW; PI rule #9 (9-step); Opus-only (rule #2)'"; `:281-282` "authored at the ratified capability floor (Opus-class), never by a lower tier". Against: owner 2026-07-25 "best_practice_synthesis can be fable as well" (`:609`); `:608` ACTION (3) "Opus-class or above, which includes Fable-class"; decision-protocol `:149-150`. The anchor also names a table absent from `sqlite_master`.
- Fix: `:275` "… Opus-class or above (rule #2; includes Fable-class)".
- Class: ALREADY-SETTLED-BY-OWNER-WORDS; DELEGABLE as wording (D-OP).

**OM-06 — the pipeline contract says `ratified: false`; the ledger says the owner ratified it.**
- Proof: `governance/pipeline-contract.yaml:3` "ratified: false"; `:4-7` "Ratifying the corrected contract is owner decision OD-17". Against: ledger `:7986-7987` "OD-17: the corrected contract is ratified (the owner's act; its condition, T-022 merged, is met) / OD-17 STATUS: ANSWERED BY THE OWNER"; the contract's own `:395-396` "OD-17 ratified the contract before it was made". The ratification rests on the [ASSUMPTION] at `:7983` that "all" includes OD-17 ("the owner has not been shown the contract diff in this session").
- Fix: set `ratified: true` with a comment pointing at the ledger entry, or ask the owner to confirm first because the record marks the reading unratified.
- Class: OWNER-ONLY (the owner's act).

**OM-07 — the contract's judgment and synthesis anchors contradict the owner's spine, with no task to fix them.**
- Proof: `governance/pipeline-contract.yaml:185` judgment anchor "the 4-state determination machine + convergence + directness (evidence-architecture.md §5)". Against the owner's 2026-08-27 spine, quoted in the contract's own note `:382-388`: "directness belongs to `judgment`, convergence to `synthesis`, and the determination machine to `specification`". `:391-396`: "has NO task … The rule change itself is an OPEN POINT for the owner". `:286-287` specification anchor rests on conceptual-model `:90` (made history by ADJ-02).
- Fix: `:185` anchor "directness and the tier verdict (owner spine 2026-08-27)"; specification anchor "the determination machine (evidence-architecture.md §5)". Delete the conceptual-model citation.
- Class: OWNER-ONLY (the contract states it is an open point for the owner).

**OM-08 — the doctrine-recheck criterion asserts a cadence the owner abolished, and its gate checks something else.**
- Proof: `governance/pipeline-contract.yaml:361-362` "A doctrine recheck fires at every stage transition and every 25 sessions". Against DR `:601-604` ("the frozen recheck counter … and the "any doctrinal revision" recheck trigger are removed") and DR `:616-617` (item 4 "**ABOLISHED**"). The registered gate (`governance/check-registry.yaml:642-652`) runs `scripts/doctrine_recheck.py --cross-ref`, which validates cross-references and does not test cadence. A green gate here passes having examined none of what the criterion claims. `governance/doctrine-recheck.md:24` ("§1.1 Periodic — every 25 working sessions") and `:317` (the counter) restate the abolished cadence. `:5` and `:306` cite the dead `workplan/workplan-co0007-v3.md`.
- Fix: criterion "Work-product's doctrinal_basis cross-references resolve (DR-2026-08-19 §10 retains `--cross-ref` only)". One dated note atop doctrine-recheck.md §1.
- Class: DELEGABLE (the owner already signed §10; this is the record catching up).

**OM-09 — tier-system's marker section is anchored on a skill that does not exist.**
- Proof: `governance/tier-system.md:63` "`skills/guidebook-auditor_SKILL.md` §4.2 inline quality markers map to the canonical ladder"; also `:5`, `:70-72`, `:81`. `git ls-files | grep -i guidebook-auditor` prints nothing (not archived either; the live skill is `skills/evidence-auditor_SKILL.md`). §5 is the home T-120 makes canonical for markers, so its first sentence must not point at nothing.
- Fix: `:63` "The markers map to the canonical ladder as follows:"; leave §6 and §7 as provenance with "(skill since deleted)".
- Class: DELEGABLE (pointer; no definition changes), owner merges the doctrine file.

**OM-10 — the schema CHECK that holds the marker vocabulary contradicts the owner's table and is missing from ADJ-09a and ADJ-10.**
- Proof: `specifications.marker` CHECK, read live: `marker IN ('●', '◐', '○') AND (regulatory_stratum_only = 0 OR marker = '○')`. It admits no ⚠ (U7, OD-64), and it forces ○ on every regulatory-stratum-only cell, including a T4-only cell that the owner's "T4 only half circle" makes ◐. By CLAUDE.md §4 and rule 8 the CHECK, not prose, is the vocabulary's home. T-120 `:121` assigns the CHECK to T-117. The adjudication's home lists (ADJ-09a, ADJ-10) omit it.
- Fix: add "`specifications.marker` CHECK (T-117)" to ADJ-10's marker row.
- Class: ALREADY-SETTLED; schema change by T-117 (DELEGABLE D-SCHEMA under OD-79).

**OM-11 — decision-protocol points to capture fields deleted on 2026-10-14.**
- Proof: `governance/decision-protocol.md:69` "Departures are visible in the decision record's `delegation` field and `delegation_rationale` field"; `:31` "cross-references the secondary category in §3 capture fields"; `:13` "the canonical capture format (§3)". Against its own change log `:188`: "Register (§5), CS8 activation (§6), validator (§7), the required-fields table and the decision-record notation deleted with the register (RULINGS R30, R47)". §3 holds no fields.
- Fix: `:69` "Departures are stated in the ledger entry that records the decision."; delete "in §3 capture fields" at `:31`.
- Class: owner merge per R30 ("decision-protocol §5 owner merge"); content DELEGABLE.

**OM-12 — the DR's §A still sends a working session to a superseded runbook.**
- Proof: DR `:13` "A session about to work | §A → §3 (order) → §12 (the runbook) → run it"; `:4` "It is the only planning artifact a session needs to read". Against DR `:778` "§12.1 … **SUPERSEDED 2026-09-10** … left below as a historical record only". ADJ-04's DR note does not cover §A's routing table.
- Fix: fold into the DR note: "§A's routing rows and the claim at `:4` are spent; for current work see the newest ledger ACTION lines."
- Class: OWNER-ONLY (DR is DG-NON, `:87-88`).

---

## CORRECTIONS TO PROPOSED TEXT

1. **ADJ-01 annotation.**
   - Replace "The axis layer this document is built on is retired: owner rulings 2026-08-18 (R3, …), 2026-08-24 and 2026-09-13 (…), executed by …" with: "The axis layer this document is built on is retired: owner ruling 2026-08-18 (R3, `workplan/2026-08-18-handoff-next-session.md`); the owner's rulings of 2026-08-24 and 2026-09-13 forbid the word as a layer name and `AX-` as an ICF code (`git grep -n -F "I don't want axis to be used"`, `git grep -n -F "should never ever exist anywhere"`); the retirement was executed under delegated ruling R35 by `scripts/migrations/109_drop_axes.sql`."
   - Replace the section list with: "Read §2, the axis half of §3.3, §4, §5 items 1–4 and 8, the first sentence of §5 item 7, §6–§8 and §9.2–§9.8 as history. Not touched: §0.5 (except `population_axis_map` and `situations`, both dropped), §3.1, §3.3's diagnosis-optional and naming paragraphs, §5 item 5, §5 item 7's 'Co-1 = tier 1 = eligible to anchor ● claims', and §9.1. §5 item 6 (non-DOI intake) is not adjudicated here."
2. **ADJ-02 annotation.** Replace "The schema and converter files of §1.1 no longer exist (the converters are under `_archived/scripts/convert/`)" with "Of §1.1's schema files only `schemas/evidence_source.py` exists; the converters are under `_archived/scripts/convert/`". Replace "the `populations` array is gone (migration 071)" with "the `populations` field of the deleted Specification schema is gone, and migration 071 dropped `population_code` from `specifications`".
3. **ADJ-04 item 1.** Do not insert the seven-rank order. If the owner wants a sentence: "The owner's words govern (rule 0). Delegated resolutions are made against the doctrine, this file and the ledger, and never bind what decision-protocol §2.4 reserves (owner, 2026-11-25: "as always refer to doctrine/mission/claude.md etc for guidance as required"). A recorder's [ASSUMPTION] is not the owner's words." Class: OWNER-ONLY.
4. **ADJ-04 item 3 (DR note).** Delete "§11 property 3 already says so" and the "What still binds here" list. Replace with: "§8's read-set and §A's routing are spent (successor plans exist; see the newest ledger ACTION lines). This DR's OD-1 to OD-12 are numbered apart from the remediation register's OD-01 onward; cite them as "DR-2026-08-19 OD-n"." Class: OWNER-ONLY.
5. **ADJ-04 item 4.** Drop it, or replace with a pointer that adds no exception and no list: "Delegated resolutions and their reach: the ledger (search `RESOLVED UNDER DELEGATION`; OD-79)." Class: owner merge.
6. **ADJ-09b.** Replace with "Only an Opus-class model or above (which includes Fable-class; decision-protocol §4.2) writes `specifications`." Coordinate with T-120 item 3 so the sentence is edited once.
7. **ADJ-09d.** "delete the three version numbers on line 5".
8. **ADJ-09j.** "**T3** lower-control primary (clinical or grey) · **Co-2** OT professional-body CPGs, **co-primary with T2**". Class: OWNER-ONLY.
9. **ADJ-09a interim note.** Place it under §5's heading AND §8's heading, naming §9 `:105` and §10 `:113`. Quote OD-64 as the owner typed it: "2 triangle for all" (with the recorder's reading marked as such).
10. **ADJ-08 intro.** Replace "ACTION (sixth) says the questions are not to be put again" with "the recorder's reading of the (sixth) statement, unratified, is that the questions are not to be put again".
11. **ADJ-08e.** Replace "satisfied by merge" with "OWNER-ONLY; OD-83 answers OI-77 under a delegation whose reach over population codes is a recorder [ASSUMPTION], and the retirement is one-way. Ask, or leave T-102's SCI step stopped."
12. **Approval classes to change to owner merge or OWNER-ONLY:** ADJ-06 sentence 1, ADJ-09e (mission paths), ADJ-09f, ADJ-09h, ADJ-09j, ADJ-09l, ADJ-04 items 1, 3 and 4.

## Self-consistency defects

- ADJ-09a ("no new text; T-120 carries it") versus ADJ-07 ("the five one-sentence fixes above go ahead regardless", including `:372`): two proposals for the same line.
- ADJ-09b versus T-120 item 3: both rewrite CLAUDE.md `:381-382`.
- ADJ-10 ("the DR note points to it") versus ADJ-04 item 3 (no pointer).
- ADJ-01's `:542` row drops "Entity model"; ADJ-02's note names `sqlite_master` as the live model, but no routing row carries it.
- The adjudicator's `:7` ("Doctrine files remain the owner's to merge") versus DELEGABLE on 09e, 09f and 09h.

## Not reached / unverified

- [UNVERIFIED] The owner's 2026-11-26 typed words ("Co-2 is co-primary with tier 2"; the reorganisation framing): no committed file holds them.
- [UNVERIFIED] Whether `permissions.deny` matching normalises MCP server names (ADJ-06). This subagent exposes no remote tools to compare.
- The transcripts were not searched for rule 9's 2026-09-23 words.
- `governance/population-taxonomy.md`, `evidence-methodology.md` and `armature_v4.md` were not read (also outside the adjudicator's scope).
- [NULL: tier-system.md and decision-protocol.md re-examined for axes, items and the medical lens presented as live; nothing found, which agrees with the adjudicator's NULL.]
- [NULL: ADJ-05's claim that no later owner word relaxes rule 10: the ledger after `:8240` was examined; nothing found.]

## Summary (under 200 words)

The adjudication's quotations are almost all verbatim, and its database facts hold. Its defects are in what it builds on them.

- ADJ-04 proposes an authority order that ranks delegated resolutions above doctrine and CLAUDE.md. That contradicts the owner's 2026-11-25 instruction to refer to doctrine and CLAUDE.md.
- ADJ-04 also invents merge-as-approval and writes an unratified [ASSUMPTION] into decision-protocol §2.4 as DELEGABLE.
- ADJ-09a tells the owner that running T-120 fixes the marker table. T-120 does not reach tier-system §8, §9, §10 or the §1 T6 row.
- Several classes (09j, 09l, 06, and the DR note) are DELEGABLE where §2.4, R30 or the DR's own DG-NON header reserve them to the owner.
- ADJ-01 presents the 2026-08-24 renaming ruling as a retirement. ADJ-02's annotation contains a false clause.
- Twelve omissions are proven (OM-01 to OM-12), including:
  - Co-2 co-primacy missing from tier-system and CLAUDE.md;
  - "Opus-only" in the pipeline contract;
  - `ratified: false` against OD-17;
  - the contract's judgment anchor;
  - a doctrine-recheck gate that checks something other than its criterion;
  - a marker section anchored on a deleted skill.

File: `/tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/antagonist-1.md`
