# Antagonist 2: attack on the combined adjudication (adjudication.md, adjudication-2.md)

Read-only. Repository HEAD `71b7c58`, `PRAGMA user_version` 167 (derive: `python3 -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('pragma user_version').fetchone()[0])"`). Ledger = `references/project-standards.md`. Line numbers are as read at that HEAD; locate by the quoted text. `scratchpad/antagonist-1.md` did not exist when this pass started or finished, so nothing here repeats it.

## 1. Verdict table

| ID | Verdict | One-line reason | Correct class (if different) |
|---|---|---|---|
| ADJ-01 | WOUNDED | Part table sound; but "retired by owner words in three rulings" is false: the owner's 2026-08-24/25/27 rulings renamed and kept the layer, 2026-09-13 left its survival "owner-gated"; the retirement is R35 (`agent`) under the 2026-10-14 delegation | OWNER-ONLY (owner merge), not ALREADY-SETTLED |
| ADJ-02 | SURVIVES | Migration 107 and owner reason verified; minor: banner uses ⚠ (see OM-07) | — |
| ADJ-03(a) | SURVIVES | Owner still says "populations" | — |
| ADJ-03(b) | SURVIVES | Real tension; recorder's supersession is [ASSUMPTION] | — |
| ADJ-04 | WOUNDED | Evidence verified; rank 4 (DR beside or above canonical doctrine) has no owner words; decision-protocol edits need an owner merge | item 1: OWNER-ONLY; item 4: owner merge |
| ADJ-05 | SURVIVES | PR 243 carries `9fa3307`; merged 2026-11-20 | — |
| ADJ-06 | WOUNDED | Facts right; class wrong: the ledger reserves rule 9 to the owner (L8209) | OWNER-ONLY |
| ADJ-07 | SURVIVES | ACTION (1) at L8214 binds; but misses L8209's reservation list, which bears on every CLAUDE.md edit in both files | — |
| ADJ-08a | SURVIVES | DB read: GAP-379 OPEN; e120 rows pending; each identity keeps e115/e150/e155 | — |
| ADJ-08b | SURVIVES | Three live pending rows; cost given as a query, not a count | — |
| ADJ-08c | SURVIVES | OD-67/OD-87 lines verified | — |
| ADJ-08d | SURVIVES | Correctly marks the delegated reading as not owner meaning | — |
| ADJ-08e | SURVIVES | SCI `active`, WHEEL absent, GAP-111 OPEN (DB read) | — |
| ADJ-09a | SURVIVES | "Run T-120" is the smallest change; its line list misses tier-system.md:105 | — |
| ADJ-09b | WOUNDED | Diagnosis right; replacement text false ("writes a determination"): the 2026-09-09 ruling says the determination is computed and keeps the Opus floor on synthesis separate | — |
| ADJ-09c | SURVIVES | Medium; commitment 5 question legitimate | — |
| ADJ-09d | SURVIVES | `decision-protocol.md:5` pins versions against §4.2 | — |
| ADJ-09e | WOUNDED | Only 2 of 12 governance files citing `workplan-co0007-v3*` named | — |
| ADJ-09f | SURVIVES | Three figures verified verbatim | — |
| ADJ-09g | SURVIVES | Collision verified (DR :593-594 vs ledger OD-10/OD-11) | — |
| ADJ-09h | SURVIVES | `evidence_sources.evidence_type` has no DB CHECK, so `schemas/enums.py` is the vocabulary's only home | — |
| ADJ-09i | SURVIVES | Pointer widens owner reservation; safe direction | — |
| ADJ-09j | WOUNDED | Right defect; class wrong (tier definition, decision-protocol §2.4 item 3, L8209); misses `owner-browser.yaml:107`, which has the same error | OWNER-ONLY |
| ADJ-09k | SURVIVES | `tail -1` gives v10_9; `sort -V` gives v10_14 | — |
| ADJ-09l | WOUNDED | R30 itself says "decision-protocol §5 owner merge" | owner merge |
| ADJ-10 | SURVIVES | Descriptive | — |
| ADJ2-A | WOUNDED | Table correct; proposed §5 drops OR-23/OR-23b; broadens OR-22b; "band() implements this table; it is the only code home" false; companion edits leave tier-system :98, :105, :113 contradicting §5 and orphan the OR-23 callout; "every place" list misses at least six homes; a second text competing with T-120 item 2a | content settled; owner merges (OD-57 registration: DG-NON) |
| ADJ2-B | WOUNDED | L17 verified; sweep misses six homes; OR-6c question moot for selection (harm test of 2026-11-14) and arguably answered by OR-6c's "two sources of the same tier" given `tier=2` | OWNER-ONLY (tier definition; L8209) |
| ADJ2-C1 | SURVIVES | Correctly attributes retirement to R35 under delegation | — |
| ADJ2-C2 | WOUNDED | Content right; its quotation "the item-layer deletion (2026-09-01) stands" is the extract's paraphrase of an [ASSUMPTION], not ledger text | — |
| ADJ2-C3 | SURVIVES (as revised) | But still in the approval list (#22) after being declared no conflict | drop from list |
| ADJ2-C4 | WOUNDED | "Equivalent to ADJ-04" is false; (a) ranks every DR above all governance doctrine, with no owner words; (d) contradicts ADJ-04's note on which DR sections bind | (a) OWNER-ONLY |
| ADJ2-C5 | WOUNDED | Spent suspension right; exception text writes the [ASSUMPTION] column scope as an owner rule | existence ALREADY-SETTLED; scope OWNER-ONLY |
| ADJ2-C6 | SURVIVES (as revised) | — | OWNER-ONLY (L8209) |
| ADJ2-C7 | SURVIVES (as revised) | — | — |
| ADJ2-C8 | WOUNDED | Q1's options are false on the DB; Q2's cost is wrong (three rows, not two); left uncorrected after "confirming" ADJ-08a | — |
| ADJ2-C9 #1 | FALSE | The fix resurrects the convention the owner killed on 2026-08-27 ("It is dead") and would unprotect `v_coverage_priority` | — |
| ADJ2-C9 #2 | SURVIVES | see F4 | — |
| ADJ2-C9 #3 | WOUNDED | Pointing at the CHECK still yields `not_applicable`; the doc would point to a value it forbids | — |
| ADJ2-C9 #4 | SURVIVES | Matches 2026-08-24 "never bare codes"; leaves "never population umbrellas" (OM-18) | — |
| ADJ2-C9 #5 | SURVIVES | Owner words L4928 verified; misses tier-system :19 and :21 (OM-02) | — |
| ADJ2-C9 #6, #7 | SURVIVES | History; no change | — |
| ADJ2-D | UNVERIFIABLE (partly WOUNDED) | Rows spot-checked hold; "MOB family resolved" while WHEEL/WALKAID/LLD are not minted in `base_taxonomy_identity` | — |
| ADJ2-E | WOUNDED | Only OD-14 is a proven overreach; OD-05 applied the owner's order and referred the edge back; OD-43 was overtaken by an owner answer, not an overreach; R35's "owner-gated" conflict dismissed too quickly | — |
| ADJ2-F1 | FALSE | "Stale" and ALREADY-SETTLED are wrong: OD-17's inclusion in "Ratify all" is an [ASSUMPTION] whose breadth "is the first to confirm"; the owner's condition (read the contract) is unmet; OD-17 is one of "the owner's acts" | OWNER-ONLY |
| ADJ2-F2 | WOUNDED | Owner words verified; the contract's own note calls the rule change "an OPEN POINT for the owner"; the synthesis anchor reintroduces the dead name `best_practice_synthesis`; contradicts F1 on whether the note was ratified | OWNER-ONLY |
| ADJ2-F3 | SURVIVES | `db.py` reads `contract.translation.default_stage`; regex finds nothing | — |
| ADJ2-F4 | WOUNDED | Ruling right; text keeps the dead table name, names two classes against ACTION (4) "do not re-pin", conflicts with pass 2's own confirm-table text; misses three more homes | — |
| ADJ2-F5 | WOUNDED | Diagnosis right; the proposed criterion keeps an obligation that cannot fire, keyed on project stages that C8 Q14 says the workflow has left | — |
| ADJ2-F6 | WOUNDED | "Marker only" is inference; OD-10 ("'provisional' = thin evidence") collides with the 2026-11-14 "thin" (⚠); the criteria it says "stand" contain "weak-band" text that contradicts T4 ◐ | — |
| ADJ2-F7 | WOUNDED | Stage table right; "the marker shown is `specifications.marker`" contradicts OD-59 and the mixed-value ruling (each finding keeps its own marker); no conflict requires the clause | drop |
| ADJ2-F8 | SURVIVES | — | — |
| ADJ2-F9 | WOUNDED | CLAUDE.md L270 rightly found; misses `stage-map.yaml:83` and `:28`, which restate the dead convention, so "they agree" is false | — |
| Extractor spot-checks (pass 2) | SURVIVES | Items 1–3 confirmed against source | — |
| Confirm/overturn table | WOUNDED | ADJ-04 "equivalent" false; approval list uses texts the table overturned (L381, DR note); C8 not reconciled with ADJ-08 | — |
| ORGANISATION / approval list | WOUNDED | #3 and #9 are false fixes; #12 and #22 answer no conflict; #2 and #20 contradict the confirm table | — |

## 2. Per-item detail

### ADJ-01 (WOUNDED; class)
The claim (adjudication.md:28): "The axis layer is retired by owner words in three rulings". What the ledger says:
- 2026-08-24 (L797-820) is about the word: "I don't want axis to be used"; "Axis is a term that we should be able to use freely". Its ACTION treats the rename as "D-SCHEMA and owner-gated". It does not retire the layer.
- 2026-08-25, owner (L1102-1142): "The layer presently called `axes` is renamed **`icf_demands`** … NOT folded into `access_needs`" (DATE: "owner ruling, selecting `icf_demands` and refusing the fold"). That keeps the layer.
- 2026-09-13 (L3504-3508): "what the demand layer should be called — and whether it survives at all now that real ICF codes carry the lens — is owner-gated."
- R35: `workplan/pipeline-state-graph/RULINGS.md:77`: "| R35 | Axes (C-017) | Ruled retired; … | high | agent | 1.4 |".

So the retirement rests on a delegated resolution, R35 under the 2026-10-14 grant, together with the R3 summary in a workplan. It does not rest on three owner rulings. The proposed banner repeats the misattribution ("retired: owner rulings 2026-08-18 (R3 …), 2026-08-24 and 2026-09-13"). That is a delegated resolution presented as an owner ruling. ADJ2-C1 states it correctly ("RULINGS R35 … under the owner's delegation"), and pass 2 still "confirmed" ADJ-01 and said its text "supersedes" C1. Also, R3 (2026-08-18) predates the owner's 2026-08-25 keep-and-rename ruling, so under rule 0 R3 is the superseded record.

### ADJ-04 / ADJ2-C4 (WOUNDED)
Every DR line cited checks out (:3, :17-25, :48, :89-92, :305, :323-329, :563, :578, :593-594, :636-637). The defect is the order:
- ADJ-04 rank 4: "ratified records … the later on a point winning".
- C4: "4. Ratified decision records, including DR-2026-08-19 … 5. `governance/` doctrine. 6. CLAUDE.md."

These are not "equivalent" (confirm table). C4 puts every DR above mission-and-epistemics.md, which is DG-NON doctrine (decision-protocol §2.4 item 1). No owner statement ranks DRs against doctrine. Pass 1 flagged the point itself ("medium … mission doctrine is DG-NON"). A sentence that sets the project's authority order, written next to rule 0, is owner territory.

The two DR history notes also disagree on which sections still bind:
- ADJ-04: "§1.4 …, §7 …, the write-path discipline of §12.0 as amended, and §4's acceptance criterion".
- C4(d): "§1.4, §6, §7 and §12.0 … §A, §3, §8 and §9 are history".

The approval list (#20) uses C4(d), while the confirm table says "Use its fuller DR note".

### ADJ-06 / ADJ2-C6 (class)
Ledger L8209 (2026-11-20 third): "The owner approves the goal sentence, rule 0, rule 9, the tier and Co-1 definitions, and the fate of the layer model. A session may reorder and reword process rules, traps and command lists." Neither file cites it. A DELEGABLE rewrite of rule 9's enforcement sentence contradicts it. The deny entries are verified at `.claude/settings.json:43-46`. Whether permission matching normalises server names is [UNVERIFIED]; this subagent's tool list does not expose the remote tools.

### ADJ-09b, ADJ2-F4, C9#2 (the synthesis floor)
The ruling is verified at ledger L606-609: "Answer the synthesis-floor question by class: Opus-class or above, which includes Fable-class" and "(4) Do not re-pin the floor to whatever model is current". The 2026-09-09 ruling (L2711-2713) says: "Nor does this touch the Opus floor on `best_practice_synthesis` … only the `specifications` clause, and only as to whether a machine may derive the state."
- ADJ-09b's "writes a determination (`specifications`)" is therefore false.
- F4's text ("Only Opus-class or Fable-class models … write `best_practice_synthesis`") keeps a name that is not in `sqlite_master`; the only match is the view `v_best_practice`. It also lists two classes where the ruling sets a floor.
- Pass 2's confirm-table text is the accurate one, yet the approval list (#2) points to F4.
- The same defect appears in T-120 item 3, which would make CLAUDE.md read "Only Opus-class models write `specifications`". Neither adjudicator noticed this (OM-20).
- Homes neither file lists: `governance/project-instructions-v10_14.md:104` ("only Opus"), `skills/evidence-metadata-rehabilitation_SKILL.md:26` ("(Opus only)"), `skills/functional-deficit-researcher_SKILL.md:201` ("Opus only").

### ADJ-09e (incomplete)
`git grep -l "workplan-co0007-v3" -- governance` lists twelve files: adversarial-use-framework, audience-priority, co1-operational, decision-protocol, doctrine-recheck (`:5`), legal-regulatory, migration-survival, mission-PROVISIONAL, mission-and-epistemics, pi-revision-co, pre-stage-a-decisions, workplan-adoption. Two are named.

### ADJ-09l (class)
`RULINGS.md:72`: "R30 … ledger the single home | high | agent; decision-protocol §5 owner merge". The proposed append to decision-protocol is an owner merge, not DELEGABLE.

### ADJ2-A (markers): the current rule from the ledger
The current rule, from owner words (newest governs):
- ● T1, T2, Co-1, Co-2; ◐ T3, T4; ○ T5, T6. Sources: "i think empty for code, half for tier 3/4 …" (L6944); "empty for 5/6" (L6973); "Co-1 stays full, Co-2 full too" (L6989); applied by "od57 yes" (L7303; status L7328).
- ⚠ (U+26A0, no FE0F) replaces the circle, never beside it, for a grey, unverified or thin basis: L7053, L7071, L7039; ACTION L7078 "do not write both".
- Every grey basis, T3 grey included: "2 triangle for all" (L7401; "OD-64: triangle for every grey basis" L7424; status L7425).
- Thin: "doesn't directly concern someone but is conjecture" (L7087). Not thin: a vetted clinician judgment (L7105) and a clinician's or academic's derivation (L7141). Thin: the project's own inference (L7123) and a mixed value (L7159; ACTION L7168 "show the findings with their circles; mark the combined value ⚠").
- Mixed cell: the showcased value carries its own source's grade, with ⚠ only where that value's basis is grey, unverified or thin ("od59 yes" L7307; L7319; status L7334).
- T4-only basis ◐ ("T4 only half circle", L7195), overriding the ○ of 2026-10-30 (L4873) for T4. The code-derived flag of 2026-10-30 is untouched.
- A floor claim a study confirms *by absence* takes that study's band (OR-22b, L6183).
- An unretrievable source anchors only with a valid academic route (OR-23, L4725, L4758), or, for T4–T6, a registry citation by jurisdiction, standard number and clause (OR-23b, L6186).
- Derived figure: floor of the mean of the band ordinals (L3306, L3337), for `figure_role='derived'`.

What the owner left undecided, verified:
- Whether every PROXY grade makes a value thin (L7093).
- How vetting is recorded, and the single unvetted opinion (L7111).
- Where the warning is shown, at least as to source versus cell (L7013).
- The standard of proof in the harm test (L7184, "What it does not decide").
- OD-56(3), the mark of a provision of presence: the ledger gives it to render (T-037), not to the owner (L6628, "render's (T-037, after T-060)").
- Pass 2's open point 1 ("the ledger says nothing") is wrong in part: L7125 reads, as an [ASSUMPTION], "a derivation made by the project is thin". It is unratified, not silent.
- Missing from pass 2's list: OD-10 ("'provisional' = thin evidence", L5980) set against the 2026-11-14 "thin" that takes ⚠. Those are two meanings of one word in force at once.

Proposed §5 text, line by line:
- "`schemas/tier_derivation.py` `band()` implements this table; it is the only code home": false twice. `band()` (L102-117) implements the old table: T3 clinical FULL, T3 other WEAK, T5 PARTIAL. Other code homes: the `specifications.marker` CHECK (`marker IN ('●','◐','○') AND (regulatory_stratum_only = 0 OR marker = '○')`, which admits no ⚠ at all), `floor_mean()`, and `assess_cell._confirmed_bands` (L4758).
- "A code value confirmed by a verified study takes the confirming study's marker": broader than OR-22b, which is "a floor claim a study confirms by absence".
- No bullet carries OR-23/OR-23b. The companion edit "Keep the 2026-10-29 OR-23 callout … change 'earns no band above ○' to 'carries ⚠'" edits text that is not in the callout (L96). The phrase is in the §8 table row L94 that the same companions delete, and the callout's anchor ("the ○ row") disappears with it.
- "Thin is a property of a value's basis, not of a source" and "any synthesis step beyond what one source states" are [ASSUMPTION] readings (L7073, L7125) written as rule, so ALREADY-SETTLED overclaims them.
- The companions do not touch tier-system.md:98 ("T3-clinical alone is full band"), :105 ("supporting (● band)" for T3 scoping reviews) or :113 ("T3-grey (○ weak)"). Those would contradict the new §5 inside the same file. Lines :22 and :49 keep "⚠ Superseded", so ⚠ would carry two meanings in one file.

The "every place" list misses:
- `skills/run-pipeline_SKILL.md:160, :396, :400, :439`
- `references/methodology-evidence-hierarchy-mapping.md:157-165`
- `governance/evidence-methodology.md:289` ("at weak (○) code-derived strength only")
- `governance/pipeline-contract.yaml` register-invariants ("no above-weak-band best-practice language on regulatory-stratum cells") and no-regulatory-stratum-stated ("render as weak-band best practice only")
- `governance/armature_v4.md:35` ("● … tiers 1–6")
- the architecture legends (OM-06)

T-120 item 2a already names most of these, so pass 2 adds a second, narrower text beside an existing task (CLAUDE.md §8: reuse what exists). The CLAUDE.md §6 pointer line itself is accurate and is what OD-57 named ("replacing the ○ gloss in `CLAUDE.md` §6").

Census checks:
- "⚠ has three meanings" holds: marker (L7062/L7078); "Superseded" banner (`tier-system.md:22`, `:49`, `population-taxonomy.md:9`); audit status (`skills/evidence-auditor_SKILL.md:83-92` "⚠️ UNSTATED", "⚠️ UNCERTAIN_REVIEW"; `content-gap-analyzer_SKILL.md:22`). The census listed only the first two in its sentence.
- Differing circle legends in at least six files hold: CLAUDE.md:372, tier-system:64-66, owner-browser:111, mission:136, armature_v4:35, navigation-modes:301, page-templates:23, schema-reconciliation:56.
- The proposed text addresses neither the banner meaning nor the audit-flag meaning of ⚠, nor the five architecture/armature legends. Pass 1's own banners add three more "⚠ SUPERSEDED IN PART" uses.

### ADJ2-B (Co-2)
L17 verified: "Co-2 = OT professional body CPGs (co-primary with Tier 2)". Homes the edit misses:
- `governance/evidence-methodology.md:49` ("parallel to Tier 2")
- `schemas/enums.py:30` and `:109-110` ("parallel to Tier 2, per T-03")
- `governance/mission-PROVISIONAL.md:64` ("Co-2 is parallel to Tier 2")
- `CLAUDE.md:369` (Co-2 without "co-primary", while Co-1 has it)
- `governance/owner-browser.yaml:107`
- `governance/tier-system.md:11` ("two parallel community-knowledge tracks")

The repository uses "parallel" and "co-primary" as synonyms: `co1-operational.md:56` "parallel co-primary tiers … Co-2 sits beside Tier 2"; `evidence-methodology.md:30` "two co-primary parallel tracks". So the conflict is one of wording, and the proposed ledger ACTION "(2) Correct the three passages named" would leave at least six.

Code: Co-2 is `tier=2` (`TIER_MAP`, `("co2", SCOPE_INTRINSIC): 2`), so `band()` gives ● and nothing depends on a separate Co-2 tier. `assess_cell.py:1131-1404` does treat `co2` as its own convergence axis (`axes_co2`), and a co-primary wording change does not touch that. There are 0 `co2` rows in `evidence_sources` (DB read), so no data moves.

OR-6c question: the owner-affirmed OR-6c text includes "(the same applies to two sources of the same tier)" (part-6 L7-40; source L6164-6215). The harm test (L7180-7182) says "neither the tier nor the stratum of a value decides which value is best". The question is moot for selection, which pass 2's own "What does not change" bullet already says.

Class: Co-2's status is a tier definition (decision-protocol §2.4 item 3; L8209), so the owner merges it.

### ADJ2-C2 (quotation)
Pass 2 quotes "the item-layer deletion (2026-09-01) stands" as ledger text (2026-11-06, L5005-5031). It is the part-5 extract's paraphrase (`ps-clean/part-5.md:91`). The source L5024 reads, inside an [ASSUMPTION]: "The deletion of the item layer (2026-09-01) stands". This is minor, but it shows the verdict leaning on the extract and on a recorder reading.

### ADJ2-C5 (qualitative exception)
Owner words (L8269-8271): "permission to hand edit as required for specific columns"; "make transparent and record your hand fixes". The column scope ("qualitative judgment or wording"; the excluded "identifiers, keys, vocabularies, counts and bibliographic fields") is "[ASSUMPTION …] the owner named no column list, and the list is not decided here" (L8276). ACTION (2) adds "ask". The proposed CLAUDE.md text states that scope as "(owner, 2026-11-21)". It also leaves CLAUDE.md rule 10 ("never patched with hand SQL disguised inside the batch's data migration") unreconciled.

### ADJ2-C8
Q1 claims "(a) Yes, one triple per identity. Cost: three rows" and "(b) No. Cost: the body-size group keeps no environmental ICF coverage". The DB says otherwise: the e120 rows already exist as `pending` for LPA, TALL and BAR, and each identity also holds e115, e150 and e155 (`select identity_code,need_code,icf_code,state from identity_need_icf where need_code='A-SIZE'`). So Yes is three reviews and No loses no coverage; ADJ-08a is right. For Q2, the class-C pairs are three rows (BRAIN×A-NOSPEECH ×2, COM×A-LOWLOAD ×1), not "two reviews".

### ADJ2-C9 #1 (FALSE)
The proposed replacement: "a view reading one stage plus `base` is not counted as crossing". Ledger L2306-2308 (owner, 2026-08-27): "**This ends the 'not a stage' convention entirely.** That convention was agent-coined … It is dead. `base` is stage 1." The entry's own consequence: "+28 foreign keys are reclassified as cross-stage … `v_coverage_priority` — base + research … a **protected cross-stage pointer** … **Do not delete it.**"

The proposal restores the dead convention and unprotects the very view the ruling protects. The extract kept this ("The 'not a stage' convention is dead", part-2:265). CLAUDE.md is wrong; the contract (`base` anchor quoting the owner) and the ruling are right. The fix is to delete L270.

### ADJ2-E
- OD-05 (L5452-5456) is a faithful application of the owner's 2026-09-28 order ("forbids admitting out-of-bucket evidence before exhaustion"), and it "Referred back to the owner" the edge OD-34 later answered. It is not an overreach.
- OD-43 was a delegated reading, checked, then answered differently by the owner (L6580). That is a disagreement, not condition (e).
- Only OD-14 is a proven overreach, self-declared (L5747-5752).
- On R35: 2026-09-13 made survival "owner-gated" (L3508). Saying "rule 0 favours the later grant" assumes the 2026-10-14 grant ("§4 items") reached an owner-gated question. That is unproven, and it is a third risk to list.

### ADJ2-F1 (FALSE)
- L7983: "[ASSUMPTION: 'all' includes OD-17 … the owner has not been shown the contract diff in this session]".
- ACTION (3), L8034: "Treat every [ASSUMPTION] above as unratified except where the owner's words state it; the breadth of 'all' is the first to confirm."
- The owner's condition (L6066): "Ratify after T-022 merges, once I have read the corrected contract". The status line L7986 cites only the first half.
- L5392 reserves OD-17 as one of "the owner's acts".

So the ratification of OD-17 is an unconfirmed reading, and the header is not "stale". The `ratified: false` value is the one state the record supports. The header comment is stale for other reasons: its DR preconditions on the doctrine token and ci.yml gate were removed by DR §10 item 4 (DR :601-605).

### ADJ2-F2
Owner words verified: L1454 for the spine; L1885-1886 for "delivers a verdict … what tier"; L7526 for "yes lens in judgment". The contract's own correction (L392-396) says: "The rule change itself is an OPEN POINT for the owner: OD-17 ratified the contract before it was made." F2 overrides that recorded open point and classes the change DELEGABLE. Its synthesis anchor writes `best_practice_synthesis`, which T-120 item 3 sweeps out. F1 says the note post-dates the ratification; F2 says the note was "ratified with adjudication item 68". The two cannot both hold.

### ADJ2-F5
Verified:
- `scripts/doctrine_recheck.py` has 0 matches for PERIODIC, STAGE_TRANSITION or counter.
- The DR (L601-604) removed the counter and retained `--cross-ref`.
- `schemas/doctrine_recheck.py:195-206` still validates PERIODIC and STAGE_TRANSITION records, which F5 does not mention.

The proposed criterion keeps "The 25-session periodic cadence … is not enforced" in a contract criterion. That is an obligation recorded as unable to fire, which is the DR's "dead odometer" again.

### ADJ2-F6
OD-10 (L5980-5983): "'provisional' = thin evidence"; "A cell's `provisional` keeps the computed meaning of thin evidence". The 2026-11-14 entries define "thin" as a cause of ⚠. F6 cites OD-10 as agreeing, but it is the collision: is every `provisional` cell "thin", and so ⚠? F6's other support, "tier-system §8: 'T3-grey alone is weak band and `pending`'" (L98), sits in a sentence whose first half ("T3-clinical alone is full band") is now wrong and is left untouched by A. The two criteria F6 says "stand" carry "render as weak-band best practice only", which contradicts T4 ◐.

### ADJ2-F7
OD-59 and L7161-7168: "the source's own finding, shown by itself … keeps its circle … mark the combined value ⚠". Render therefore shows per-finding markers, which are not `specifications.marker`, a cell-level column whose CHECK has no ⚠. F7 found no conflict, yet proposes a clause on an UNENFORCED criterion. That is apparatus no conflict requires.

### ADJ2-F9
`governance/stage-map.yaml:83` (2026-11-13, T-018): "its other foreign keys point into `base`, which is not a stage, so the table crosses no stage". `:28`: "`cross-stage` is not a stage either". The convention ruled dead is being used to judge a table's stage. "They agree" is false.

## 3. OMISSIONS (neither file lists)

| ID | Proof (file:line, quoted) | One-line fix | Class |
|---|---|---|---|
| OM-01 | `governance/tier-system.md:105` "they are *supporting* (● band)" for T3 scoping and narrative reviews, against ◐ T3 (OD-57) | Drop the parenthesis or point to §5 | ALREADY-SETTLED (owner merge) |
| OM-02 | `tier-system.md:19` T3 "occasionally `standard_eb`" and `:21` T5 "`standard_eb`", against `TIER_MAP` (`standard_eb` → 2 or 4 only) | Typical-type column points to `schemas/tier_derivation.py` `TIER_MAP` | OWNER-ONLY (tier definition) |
| OM-03 | Co-2 "parallel" or missing co-primary: `evidence-methodology.md:49`, `schemas/enums.py:30,:109`, `mission-PROVISIONAL.md:64`, `CLAUDE.md:369`, `owner-browser.yaml:107` | Extend B's sweep | OWNER-ONLY |
| OM-04 | `owner-browser.yaml:107` "T3 is grey primary work" (same defect as ADJ-09j) | Same wording as ADJ-09j | OWNER-ONLY |
| OM-05 | `governance/armature_v4.md:35` "● (filled circle) = specification supported by direct evidence (tiers 1–6 …). ○ … inferred" | Pointer to tier-system §5 | ALREADY-SETTLED (owner merge) |
| OM-06 | `architecture/navigation-modes.md:301` "● = stated evidence, ◐ = provisional evidence, ○ = pending review"; `page-templates.md:23`; `schema-reconciliation.md:56` (marker read as cell state; census 7g dropped) | Point the legend to tier-system §5; state separately | DELEGABLE (architecture, SUPERSEDED IN PART files) |
| OM-07 | ⚠ meaning "Superseded" at `tier-system.md:22`, `:49`, `population-taxonomy.md:9`; audit flags at `evidence-auditor_SKILL.md:83-92`, `content-gap-analyzer_SKILL.md:22`; pass 1's proposed banners add three more | Banners and flags stop using ⚠ once it is a marker state | DELEGABLE (prose); owner merges doctrine files |
| OM-08 | `governance/held-tensions.md:20` "`governance/population-taxonomy.md` (CANONICAL)" and `:380` "CANONICAL", against `population-taxonomy.md:2` "SUPERSEDED (population code set)" (census 3b dropped) | One dated note in held-tensions | OWNER-ONLY (RATIFIED doctrine; population taxonomy) |
| OM-09 | Skills naming item codes: `cross-reference-resolver_SKILL.md:37` ("see item G-03", validates item headings), `toc-editor_SKILL.md:56,:89` (J-01 as live example), `voice-style_SKILL.md:109,:252`, `adversarial-research_SKILL.md:294-312` (census 7c dropped); CLAUDE.md §1 requires checking that skills do not presuppose the item layer | Mark or delete the item-code examples | DELEGABLE (skills are code-adjacent, §8) |
| OM-10 | `CLAUDE.md:90` "(`ci.yml:257`)": line 257 is `with: {node-version: "20"}`; the check runs at `ci.yml:274`. `CLAUDE.md:350` names `index.html`, which is untracked (`git ls-files` count 0) | Replace the line pointer with the job name `commit-msg`; drop `index.html` | DELEGABLE |
| OM-11 | `governance/stage-map.yaml:83` "`base`, which is not a stage, so the table crosses no stage"; `:28` "not a stage either", against the owner's 2026-08-27 "It is dead" | Restate as base stage; re-judge `extraction_lens_links` crossing | ALREADY-SETTLED |
| OM-12 | `project-instructions-v10_14.md:104` "only Opus"; `skills/evidence-metadata-rehabilitation_SKILL.md:26` "(Opus only)"; `skills/functional-deficit-researcher_SKILL.md:201` "Opus only" | Floor wording "Opus-class or above" (PI may lag by design; the skills may not) | ALREADY-SETTLED |
| OM-13 | `evidence-methodology.md:247` single_axis "Tier 4–6 only. No convergence or divergence assessment is possible", against "OD-43: agreement between any two kinds of evidence counts as convergence" (owner, L6580); `:289` "at weak (○)" against T4 ◐ | Carry in T-068/T-120 | ALREADY-SETTLED |
| OM-14 | `pipeline-contract.yaml` register-invariants "no above-weak-band best-practice language on regulatory-stratum cells" and no-regulatory-stratum-stated "render as weak-band best practice only", against "T4 only half circle" | T-120 item 2a names them; add to the approval list | ALREADY-SETTLED |
| OM-15 | OD-10 L5980 "'provisional' = thin evidence" against the 2026-11-14 thin = ⚠ cause (L7087, L7078) | Owner question: is the `provisional` "thin" the ⚠ "thin"? | OWNER-ONLY |
| OM-16 | Ledger L8209 reserves rule 0, rule 9 and the tier and Co-1 definitions in CLAUDE.md to the owner; neither file uses it in classing CLAUDE.md edits | Reclass ADJ-06, C6, ADJ-09j, B (CLAUDE.md part) | — |
| OM-17 | `skills/run-pipeline_SKILL.md:396` "at the weak band **○**", `:400` "still at ○", `:439` "a code-only one at ○", `:160` "marker ○"; `references/methodology-evidence-hierarchy-mapping.md:163` "○ \| Grey, expert consensus, thin base …" | T-120 item 2a sweep | ALREADY-SETTLED |
| OM-18 | `CLAUDE.md:378` "never population umbrellas", against owner 2026-11-21 "3 to umbrella and to specific, yes" (L8290) and 2026-11-12 (fourteenth) advocacy-group lens | Owner question or narrowed wording | OWNER-ONLY (population taxonomy) |
| OM-19 | Ten governance files beyond ADJ-09e cite `workplan/workplan-co0007-v3*.md` (now `workplan/_superseded/`), e.g. `doctrine-recheck.md:5` | Path fix | DELEGABLE |
| OM-20 | T-120 item 3: "`best_practice_synthesis` … in CLAUDE.md §6 … becomes `specifications`" would yield "Only Opus-class models write `specifications`", against owner 2026-09-09 "you have to compute it" (L2690) | Amend T-120 item 3 before running it | DELEGABLE (task file) |

Census findings dropped by both adjudications: OM-06, OM-08, OM-09, OM-10, and the 41 NET retired-vocabulary hits (census §5; e.g. `governance/project-instructions-v10_14.md` with 5 `audit.yml` hits, and `governance/migration-survival.md:79,:176` `UNVERIFIED-1`).

One census finding is itself FALSE: the "22 duplicated skill files flat vs .claude". `.claude/skills/*/SKILL.md` are symlinks (`git ls-files -s .claude/skills/run-pipeline/SKILL.md` gives mode `120000`; `ls -la` shows `SKILL.md -> ../../../skills/evidence-auditor_SKILL.md`). There is one home, and the census's per-copy "last commit" dates are of the links. Neither adjudication acted on it, correctly.

## 4. CORRECTIONS TO PROPOSED TEXT

1. **C9 #1 (CLAUDE.md L270).** Replace the proposal with: delete the line "Convention: `base` is not a stage, so a view reading one stage plus base crosses nothing." Nothing replaces it; `base` is stage 1 (owner, 2026-08-27).
2. **ADJ-01 banner.** Replace "The axis layer this document is built on is retired: owner rulings 2026-08-18 (R3, …), 2026-08-24 and 2026-09-13 (…), executed by …" with "The axis layer this document is built on is retired by a delegated resolution (RULINGS R35, under the owner's delegation of 2026-10-14), after the owner's 2026-08-24 ruling against the term and the 2026-09-13 statement of the three vocabularies ("access needs, ICF codes, disability identities"); executed by …". Write the heading as "SUPERSEDED IN PART 2026-11-26", without ⚠ (OM-07). The same applies to the ADJ-02 and ADJ-04 banners.
3. **A, §5 last bullet.** Replace "`schemas/tier_derivation.py` `band()` implements this table; it is the only code home." with "Until T-117 lands, `schemas/tier_derivation.py` `band()` and the `specifications.marker` CHECK implement the earlier table; the table above governs."
4. **A, OR-22b bullet.** Replace with "A floor claim that a verified, retrieved study confirms by absence takes that study's marker (OR-22b)."
5. **A, add a bullet.** "An unretrievable source anchors only with a valid academic route (OR-23, 2026-10-29) or, for T4–T6, a registry citation by jurisdiction, standard number and clause (OR-23b); with one it carries ⚠; without one it anchors nothing."
6. **A, "Not yet ruled".** Add "whether a `provisional` cell ('thin evidence', OD-10) is 'thin' in the ⚠ sense". Remove "the mark of a provision of presence", which OD-56 assigns to render (T-037). Mark the thin bullets' extensions as "[recorder's reading]".
7. **A, companion edits.** Add the replacements for tier-system.md:98 (drop "T3-clinical alone is full band and"; keep the state clause), :105 (drop "(● band)") and :113 (replace "(○ weak)" with "(⚠)"). Re-anchor the OR-23 callout to §5, since the §8 table row it cites is deleted. Better still, run T-120 item 2a, which already names the wider set; do not keep two texts.
8. **F4 / C9 #2 / ADJ-09b (CLAUDE.md L381-382).** "Only a model at the Opus-class-or-above floor (DR-2026-06-10; owner 2026-07-25: Fable included) authors judged synthesis text; a determination is computed, not written (owner, 2026-09-09)." Contract L281: "(Opus-class or above)". Do not name `best_practice_synthesis`.
9. **F2 synthesis anchor.** Remove "best_practice_synthesis authored at the Opus-class-or-above floor"; use "judged synthesis text authored at the Opus-class-or-above floor".
10. **F1.** Keep `ratified: false`. Replace the comment with "# OD-17: the 2026-11-19 status line rests on an unratified reading that 'Ratify all' included it (ledger L7983; ACTION (3): 'the breadth of all is the first to confirm'); the owner's condition, reading the corrected contract, is recorded unmet."
11. **C8 Q1.** "(a) Yes: the three pending e120 rows are reviewed to `stated` citing your entry. (b) No: three retirements; each identity keeps its other A-SIZE environmental codes (derive: `select identity_code,icf_code from identity_need_icf where need_code='A-SIZE' and retired_at is null`)."
12. **C8 Q2.** Cost: "one retirement per row the query in ADJ-08b prints".
13. **C5.** "Exception (owner, 2026-11-21): a session may correct by hand, in a data migration, a cell in a column the owner counts as qualitative (which columns is the owner's, still open: ask), recording the old value, new value, reason and session in the migration header and the gap's resolution." Add the same exception's pointer to rule 10.
14. **B, proposed ledger ACTION (2).** "Correct every passage calling Co-2 'parallel to Tier 2' or leaving Co-2 out of the evidence-tier definitions (derive: `git grep -n -i -E 'co-?2.{0,80}parallel' -- CLAUDE.md governance schemas`)." Drop the OR-6c [ASSUMPTION] or mark it moot for selection under the 2026-11-14 harm test.
15. **F7.** Withdraw.

## 5. APPROVAL LIST (smallest change first; FALSE items excluded)

| # | Change | Class | Confidence |
|---|---|---|---|
| 1 | Delete CLAUDE.md L270 (correction 1) | ALREADY-SETTLED | high |
| 2 | `stage-map.yaml:83` and `:28` stop calling `base` "not a stage" (OM-11) | ALREADY-SETTLED | high |
| 3 | CLAUDE.md L467 `sort -V` (ADJ-09k) | DELEGABLE | high |
| 4 | CLAUDE.md L90 line pointer to the job name; drop `index.html` at L350 (OM-10) | DELEGABLE | high |
| 5 | `decision-protocol.md:5` strip version pins (ADJ-09d) | ALREADY-SETTLED | high |
| 6 | CLAUDE.md L378 "bare axis codes" to "bare codes" (C9 #4) | DELEGABLE | high |
| 7 | CLAUDE.md L381-382 floor sentence (correction 8) | ALREADY-SETTLED | high |
| 8 | CLAUDE.md L372 marker pointer (A) | ALREADY-SETTLED (OD-57 named it) | high |
| 9 | CLAUDE.md §8 sign-off list to pointer (ADJ-09i) | DELEGABLE | high |
| 10 | CLAUDE.md L538 row and `orient.md:25` (ADJ-04 item 2 / C4 b,c) | DELEGABLE | high |
| 11 | CLAUDE.md L373 cell states pointer (C9 #3), noting the CHECK still admits `not_applicable` | DELEGABLE | medium |
| 12 | CLAUDE.md §6 T3 gloss and `owner-browser.yaml:107` (ADJ-09j, OM-04) | OWNER-ONLY | high |
| 13 | Rule 9 enforcement sentence (ADJ-06) | OWNER-ONLY | medium |
| 14 | `.claude/settings.json` deny names (owner applies) | OWNER-ONLY | low [UNVERIFIED matching] |
| 15 | `workplan-co0007` path fixes across twelve governance files (ADJ-09e, OM-19) | DELEGABLE | high |
| 16 | `mission-and-epistemics.md:99` type list to pointer (ADJ-09h) | DELEGABLE | high |
| 17 | `evidence-architecture.md` :92, :131, :155 hand-typed figures (ADJ-09f) | DELEGABLE | high |
| 18 | Contract L281, `pipeline-operations.md:57`, two skills (F4, OM-12) | ALREADY-SETTLED | high |
| 19 | Amend T-120 item 3 so it does not write "write `specifications`" (OM-20) | DELEGABLE | high |
| 20 | Contract doctrine-recheck criterion: delete the dead cadence clause (F5) | DELEGABLE | medium |
| 21 | Run T-120 item 2a with corrections 3-7 folded in, or approve the corrected §5 (A, OM-01, OM-05, OM-14, OM-17) | content ALREADY-SETTLED; owner merges | medium |
| 22 | Co-2 co-primary wording across all homes plus the ledger entry (B corrected, OM-03) | OWNER-ONLY | high |
| 23 | CLAUDE.md §4 qualitative exception (correction 13) | existence settled; columns OWNER-ONLY | medium |
| 24 | `conceptual-model.md` banner (ADJ-02), heading without ⚠ | DELEGABLE | high |
| 25 | `functional-taxonomy.md` banner (correction 2) | OWNER-ONLY (owner merge, migration 109) | high |
| 26 | `held-tensions.md` note on population-taxonomy (OM-08) | OWNER-ONLY | medium |
| 27 | One DR-2026-08-19 history note (choose one list; attestation required) | owner merge | medium |
| 28 | Contract stage anchors (F2), the contract's own "OPEN POINT" | OWNER-ONLY | medium |
| 29 | CLAUDE.md L21-23 authority sentence (ADJ-04 item 1 / C4 a) | OWNER-ONLY | medium |
| 30 | `decision-protocol.md` §0 note on the frozen `decisions` table (ADJ-09l) | owner merge (R30) | medium |
| 31 | tier-system L15, L19, L21 typical-type cells (C9 #5, OM-02) | OWNER-ONLY | medium |
| 32 | Owner questions: ADJ-08a-e, Q16 (median), Q17 (commitment 5), OM-15 (two "thin"s), OM-18 (umbrellas), C8 Q5-Q9, Q13, Q14 | OWNER-ONLY | — |

Excluded as FALSE or unneeded: C9 #1 as written; F1 as written (`ratified: true`); F7; C3 / approval #22 (no conflict, by pass 2's own revision).

## 6. Not reached / UNVERIFIED
- ADJ2-D: only about eight rows were re-checked (p1:487, p1:867, p2:27/49, p7:449, p2:299, p4:241 partly, and the medical and item groups); the rest are [UNVERIFIED].
- ADJ-08c and ADJ-08d were checked against their cited lines only. ADJ-09c's U1/U2 lines were not re-read in full.
- Whether harness permission matching normalises MCP server names (ADJ-06): not verifiable from this subagent.
- Branch protection (C8 Q14) was not checked against GitHub.
- Extract spot-check: ten entries compared (L797-820, L1102 via part-1 L1140, L2298-2345, L2684-2731, L3304-3339, L4869-4882, L4922-4941, L5384-5398, L6164-6215, L7001-7017, L7967-8035, L8263-8282). All are faithful on the rule-bearing sentences except two:
  - (a) part-7 renders OD-17 as ratified with only "[owner not shown the diff]", dropping that OD-17's inclusion in "all" is itself the assumption;
  - (b) part-5:91 compresses an [ASSUMPTION] into a phrase pass 2 then quoted as ledger text.
  - The 2026-08-24 and 2026-08-25 axis entries in part-1 correctly show the layer renamed and kept, which pass 1 did not draw on.

## 7. Summary
The marker table pass 2 states is the owner's, and the CLAUDE.md §6 pointer is sound. The proposed tier-system §5 text is not: it drops OR-23/OR-23b, broadens OR-22b, falsely calls `band()` the only and current code home, leaves tier-system :98/:105/:113 contradicting it, and competes with T-120 item 2a, which already sweeps more homes. Two pass-2 items are false:
- C9 #1 would revive the "base is not a stage" convention the owner declared dead.
- F1 would set `ratified: true` on a status line the ledger itself says rests on an unconfirmed reading.

Pass 1 misattributes the axis retirement (a delegated R35) to owner rulings that in fact renamed and kept the layer. Several CLAUDE.md edits are mis-classed DELEGABLE despite L8209's reservation of rule 9 and the tier definitions. The Co-2 sweep misses six homes. Twenty omissions are listed.

File: /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/antagonist-2.md
