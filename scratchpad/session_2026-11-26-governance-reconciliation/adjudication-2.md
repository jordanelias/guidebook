# Adjudication 2: conflict reconciliation across the governing documents

Second-pass adjudicator, 2026-11-26. Read-only on the repository; nothing here is applied. Every proposal goes to the owner item by item. The owner's framing (typed, 2026-11-26): "it IS conflict reconciliation". Each proposal below resolves a named conflict. The ORGANISATION section at the end only collects what those resolutions mean for the structure.

**First pass.** `scratchpad/adjudication.md` (items ADJ-01 to ADJ-10) was absent when this pass started and appeared before it finished. It was read in full, and its disputed claims were re-verified. Each of its items is confirmed or overturned in the section "First-pass items: confirmed or overturned", placed before ORGANISATION. Where the first pass was better evidenced, this file defers to it, and items C3, C6 and C7 below are revised there.

**Sources.** I read all seven extracts in full. I read CLAUDE.md, DR-2026-08-19, mission-and-epistemics.md and tier-system.md in full, and the other governing files where an item needed them. Every extract reading that a verdict depends on was checked against `references/project-standards.md` with `git grep -n -F` or `sed -n`. Line numbers are as of HEAD `71b7c58`. Re-derive them before you edit; never trust them.

**Approval classes.**
- OWNER-ONLY: the owner's call (decision-protocol §2.4, or owner meaning).
- DELEGABLE: an Opus delegate may approve it under the 2026-11-25 grant, within OD-79.
- ALREADY-SETTLED-BY-OWNER-WORDS: the owner's quoted words decide it, and only the text has to follow.

---

## Item table

| ID | One-line verdict | Approval class |
|---|---|---|
| ADJ2-A | **Settled.** The owner has ruled the marker rule as ● T1/T2/Co-1/Co-2; ◐ T3/T4; ○ T5/T6; ⚠ in place of the circle for any grey, unverified or thin basis. tier-system §5/§8, band(), CLAUDE.md §6, mission, evidence-architecture, the evidence-auditor skill and owner-browser.yaml still state the old rule. T-120 and T-117 have not landed. Six sub-points are still open. | ALREADY-SETTLED (restatement); OWNER-ONLY (six open sub-points) |
| ADJ2-B | The ledger already says "Co-2 … co-primary with Tier 2" (L17), and the 2026-11-26 statement restates it. mission says "parallel to Tier 2", and decision-protocol §2.4 item 3 leaves Co-2 out. | ALREADY-SETTLED (wording); OWNER-ONLY (whether Co-2 v T2 is "same rank" under OR-6c) |
| ADJ2-C1 | functional-taxonomy.md presents a live 17-axis layer that migration 109 dropped. Layer 1 is history; Layer 2's anti-umbrella rules still live in the ledger. | OWNER-ONLY (migration 109 left this to "an owner merge") |
| ADJ2-C2 | conceptual-model.md ENT-08 Item, and "item_code on Specification", are false. The item layer was dropped. | DELEGABLE (annotation applying owner rulings) |
| ADJ2-C3 | Revised after the first pass: there is no binding conflict. The owner still uses "populations" for groups. One optional wording change is offered, plus the first pass's "median as default" question. | OWNER-ONLY (optional) |
| ADJ2-C4 | The order of authority is stated in three places. CLAUDE.md §9, /orient and the DR's own §A/§8 wrongly send a session to the DR for "what to do now". | DELEGABLE |
| ADJ2-C5 | The rule-10 suspension covered one PR and is spent. A different, live owner exception (hand correction of qualitative cells, 2026-11-21) is missing from CLAUDE.md §4. | ALREADY-SETTLED |
| ADJ2-C6 | Revised after the first pass: rule 9 governs. Its enforcement sentence is stale, and the deny names in settings.json do not match this session's tool names (ADJ-06 confirmed). | DELEGABLE (sentence); owner applies settings |
| ADJ2-C7 | Revised after the first pass: a live but unapproved proposal, carried out in part by merges. Its ACTION "Do not rewrite `CLAUDE.md` until the owner approves" still binds the remainder. | OWNER-ONLY |
| ADJ2-C8 | Open owner-only questions, verified, put as plain questions with options and costs. | OWNER-ONLY |
| ADJ2-C9 | Other conflicts and stale statements (base "not a stage"; synthesis floor; stored not_applicable; grey at T1; stale pointers). | mixed (per row) |
| ADJ2-D | Cross-slice resolution of every [STATUS UNCERTAIN] and [CHECK] tag. Most are resolved; what remains is listed. | n/a |
| ADJ2-E | Delegation audit. Three proven cases, all already corrected in the ledger. No live delegated resolution is proven to decide a reserved matter against the owner's words. Two risks are flagged, unproven. | n/a |
| ADJ2-F1 | Contract header `ratified: false` is stale. OD-17 was ANSWERED BY THE OWNER on 2026-11-19 ("Sure, append. Ratify all."). The owner's own condition, to read the diff first, is recorded as unmet. | ALREADY-SETTLED (header); OWNER-ONLY (confirm, given the unmet read) |
| ADJ2-F2 | The judgment/synthesis/specification anchors contradict the owner's 2026-08-27 spine. The fix has no task. | DELEGABLE (applies owner words) |
| ADJ2-F3 | Translation default is `judgment` and fully carried out. Nothing still says synthesis. | no change |
| ADJ2-F4 | The floor is "Opus-class or above", Fable included. CLAUDE.md §6 and the contract's synthesis anchor are wrong; decision-protocol §4.2 is right. | ALREADY-SETTLED |
| ADJ2-F5 | The `doctrine-recheck` criterion conflates project stage (A→B→C) with pipeline stage, and states a 25-session cadence that has had no counter since 2026-08-19. The script checks neither. | DELEGABLE |
| ADJ2-F6 | The 2026-11-14 rulings change the marker and which value is best, not the cell's state. The ledger says nothing on state. The two state criteria stand. | no change (owner may ask) |
| ADJ2-F7 | The triangle's causes are derived across evidence, judgment and specification. The marker is computed once at specification; render must point to it. `register-invariants` stays unenforced until render exists. | DELEGABLE |
| ADJ2-F8 | The suspension lives only in the ledger. The advisory check cannot read it. It is spent. No change. | no change |
| ADJ2-F9 | The stage lists agree in CLAUDE.md §3, contract `stages:` and stage-map.yaml, apart from labels that are not stages. One internal contradiction in CLAUDE.md §3. | DELEGABLE |

---

## ADJ2-A — Markers and the triangle

**The owner's question (2026-11-26):** why does tier-system.md lack "the triangles"?

**Answer.** The triangle was ruled on 2026-11-14 and released by "od57 yes". Its homes have not been rewritten:
- tier-system.md was last changed on 2026-10-29 (`git log -1 --format=%ad -- governance/tier-system.md`).
- evidence-architecture.md has no `## 0.` (`grep -c -F '## 0.' governance/evidence-architecture.md` prints 0).
- `band()` still returns FULL for T3 clinical, PARTIAL for T5, and WEAK for T3 grey (`schemas/tier_derivation.py:102-117`).

T-120 (doctrine prose) and T-117 (band() and the marker CHECK) are written but not executed (`workplan/2026-11-12-bidirectional-pipeline/tasks/T-120-doctrine-amendments-and-deletions.md`, `T-117-marker-table-applied.md`). T-117 waits on T-068, T-102, T-119 and T-120 (`T-117…md:22`). The ledger's home list confirms it: "U7 → `governance/tier-system.md` §5 (T-120) and `schemas/tier_derivation.py` `band()` (T-117). … Where a home does not yet carry the text, the quoted entries govern" (Unification entry, ledger L7864-7964; extract part-7 L270).

**Verdict: the current marker rule, from owner words (rule 0, newest first).**

| Point | Owner words (verbatim) | Ledger |
|---|---|---|
| Table applied | "od57 yes" (to the registered question: "● T1, T2, Co-1, Co-2; ◐ T3, T4; ○ T5, T6; ⚠ in place of the circle for a grey, unverified or thin basis … and replacing the ○ gloss in `CLAUDE.md` §6") | L7303; question at L7265; `OD-57 STATUS: ANSWERED BY THE OWNER` L7328 |
| Built from | "i think empty for code, half for tier 3/4 as 4 is above jurisdiction code, full for tier 1/2?"; "empty for 5/6"; "Co-1 stays full, Co-2 full too" | L6944, L6973, L6989 |
| Triangle replaces circle | "no, triangle instead if the value is coming from grey or unverified"; "thin too" | L7053, L7071 |
| Glyph | "⚠️" then "except use the Unicode one" (U+26A0, no U+FE0F) | L7025, L7039 |
| Every grey basis, T3 grey included | "2 triangle for all" (OD-64: "triangle for every grey basis") | L7401; `OD-64 STATUS: ANSWERED BY THE OWNER` L7425 |
| Thin | "I think thin is when the evidence doesn't directly concern someone but is conjecture"; "this is not thin. a clinician has rendered a professional judgment that has been vetted by colleagues…"; "when we do cross referential analyses in synthesis and pair testing etc, we can make conjectures … we aren't clinicians so it is flagged as thin"; "derivation by a clinician or academic counts"; "because if it mixes then it's a new value proposed for something so it's conjecture because we don't have authority" | L7087, L7105, L7123, L7141, L7159 |
| Mixed-source cell | "od59 yes" (registered: "the showcased value carries the grade of its own source; ⚠ applies only where that value's basis is grey, unverified or thin") | L7273, L7307, L7334 |
| One-stratum cell | "T4 only half circle" (later than, and so overriding for T4, 2026-10-30's "Yes, keep the ○ band and flag" for a T4–T6-only cell) | L7195; L4873 |
| Marker carries provenance | "that's why we have the circles: we can say something is best practice but the empty circle makes it clear that it's not academically or clinically derived" | L6908 |
| Confirmed floor claim | OR-22b "The study's own band" | L6164-6215 |
| Derived figure | "yeah round down" (floor of the mean of band ordinals) | L3304-3339 |

**Status of OD-64.** Extract part-6 called OD-64 open. That is overturned: the last status line is `OD-64 STATUS: ANSWERED BY THE OWNER` (L7425). Extract part-7 reads it correctly.

**A finding the extracts dropped (affects approval class).** The OD-57 registration classes marker rules as evidence-tier definitions: "Q1 and Q3 set how an evidence tier is marked … which reach the evidence-tier definitions on the decision protocol's always-DG-NON list" (L7263). So the table is OWNER-ONLY, and the owner has decided it. Restating it in the doctrine files is ALREADY-SETTLED. The open sub-points below stay OWNER-ONLY.

**Still undecided (OWNER-ONLY), from the ledger:**
1. How ⚠ enters a derived figure's floor mean, and whether an arithmetic derivation the project makes (OD-40) is a "project inference" and so thin. The ledger says nothing.
2. Whether any PROXY grade makes a value thin, or only some (L7083-7097, "What it does not decide").
3. How vetting and an author's clinician or academic standing are recorded (L7101-7151).
4. A single clinician's unvetted opinion (L7101-7115).
5. What mark a provision of presence carries on an element page (OD-56 open part, L6616-6637).
6. The old ○ list's `[EXPERT CONSENSUS]` and `[UNSUPPORTED]` have no stated place.

A further consequence for T-117, not an owner question: the `specifications` marker CHECK "requires `regulatory_stratum_only = 0 OR marker = '○'`" (`T-117…md:57`). That contradicts "T4 only half circle". I cannot tell from the task file whether T-117 relaxes it for a T4-only cell; it has to.

**Every place that contradicts the rule.** Re-derive with the ledger's own command, `git grep -n -E '○.{0,60}(grey|thin|unverified)' -- CLAUDE.md governance skills scripts schemas`.
- `governance/tier-system.md`:
  - §5 L64-68 puts T3 clinical in ● and lists ○ as "grey … T6 … UNVERIFIED".
  - §8 table L90-94 puts T3-clinical in ●, T5 in ◐, and ○ for T3-grey and unretrievable.
  - L100 says "a cell whose entire basis is T4–T6 takes ○ even where T4/T5 sources are present".
  - §5, §6 and §7 point at `skills/guidebook-auditor_SKILL.md`, which does not exist (`ls` → missing).
- `CLAUDE.md:372`: "**○** grey, thin or unverified (the source could not be retrieved)".
- `governance/mission-and-epistemics.md:136`: "○ (grey, thin, or unverified because the source could not be retrieved)".
- `governance/evidence-architecture.md`: L21 (T4–6-only at ○), L120-121 (● band, regulatory determinations), L177 (register-map row "○ weak, code-derived", wrong for a T4-only cell), L187 (I4 translations from tier-system §5).
- `governance/owner-browser.yaml:111` and `:807`.
- `skills/evidence-auditor_SKILL.md:46-55`.
- `schemas/tier_derivation.py` `band()` docstring and logic (T-117).
- `scripts/audit/research_batch_dod.py:450` (comment).
- The ledger's Core Doctrine RULE at L26 is a frozen record. It is already superseded in prose by the Unification entry ("'A T4–6-only basis never renders best-practice language' — that sentence (U6) and that RULE's marker bands (U7)"). No edit.

**Proposed reconciliation: exact replacement for tier-system.md §5 (title and body):**

```markdown
## 5. Evidence markers

Owner rulings of 2026-11-14 govern this section and win where it differs from them (ledger: "Owner answers 2026-11-14 (fourteenth set)", OD-57 and OD-59; "(fifteenth set)", OD-64; and the entries they cite). The marker states are ●, ◐, ○ and ⚠ (U+26A0 WARNING SIGN, written without U+FE0F).

| Marker | Basis |
|---|---|
| ● | T1, T2, Co-1, Co-2 |
| ◐ | T3, T4 |
| ○ | T5, T6 |
| ⚠ | in place of the circle where the value's basis is grey (at any tier), unverified (the source could not be retrieved) or thin |

- A value carries ⚠ or a circle, never both. Grey, thin and unverified sources are kept, not excluded.
- **Thin** is a property of a value's basis, not of a source: the evidence does not directly concern the people the value is shown for, and the step across is conjecture (the owner's working view). Not thin: a clinician's professional judgment vetted by colleagues; a derivation by a clinician or an academic. Thin: the project's own inference (cross-referential analysis, pair testing, any synthesis step beyond what one source states), and any value mixing a source's finding with a project inference; each finding shown by itself keeps its own marker.
- **Sources that differ:** the value shown carries the marker of its own source, with ⚠ only where that value's own basis is grey, unverified or thin.
- **One stratum only:** a T4-only basis takes ◐; a T5- or T6-only basis takes ○. A code value shown as best carries its code source and the code-derived flag with the convergence-not-evidence caveat (§3).
- **A code value confirmed by a verified study** takes the confirming study's marker.
- **A derived figure** takes the floor of the mean of its inputs' circle ordinals (● 3, ◐ 2, ○ 1).
- Convergence changes no marker. Unmarked is an error.
- **Not yet ruled (owner):** how ⚠ enters a derived figure; whether every PROXY grade makes a value thin; how vetting and an author's standing are recorded; a single clinician's unvetted opinion; the mark of a provision of presence; where the former `[EXPERT CONSENSUS]` and `[UNSUPPORTED]` labels sit.
- `schemas/tier_derivation.py` `band()` implements this table; it is the only code home.
```

**Companion edits to tier-system.md** (the same conflict; ALREADY-SETTLED):
- In §8, replace the band table L90-94 with: "The bands are the markers of §5; they grade a claim and do not gate it."
- Replace L100's sentence "a cell whose entire basis is T4–T6 takes ○ even where T4/T5 sources are present" with: "a cell resting on T4 alone takes ◐, on T5 or T6 alone ○ (§5)."
- Keep the 2026-10-29 OR-23 callout (academic route), and change "earns no band above ○" to "carries ⚠".
- Delete the T3-split paragraph at L68.
- Replace the three `skills/guidebook-auditor_SKILL.md` pointers with "(the skill named here no longer exists)", or delete them.

**Minimal CLAUDE.md §6 edit** (rule 5: point, do not copy). Replace L372 with:

```
Markers: ●, ◐, ○ and ⚠ — which tier takes which, and when ⚠ replaces the circle, is `governance/tier-system.md` §5 (owner, 2026-11-14). Unmarked is an error.
```

If the owner wants the table visible in CLAUDE.md as well, use this instead: "Markers (owner, 2026-11-14; `governance/tier-system.md` §5): **●** T1, T2, Co-1, Co-2 · **◐** T3, T4 · **○** T5, T6 · **⚠** (U+26A0, no U+FE0F) in place of the circle for a grey, unverified or thin basis, never both. Unmarked is an error." That second form is a copy, and its cost is a second home.

The same pointer sentence replaces `mission-and-epistemics.md:136`'s marker clause. Point evidence-architecture.md L187, owner-browser.yaml L111 and evidence-auditor L46-55 at §5 too.

Approval: ALREADY-SETTLED for the table and the pointer form. OWNER-ONLY for the six open points. [CONFIDENCE: high on the table, medium on the T4-only overriding 2026-10-30, since the owner's "T4 only half circle" is later and more specific.]

---

## ADJ2-B — Co-2 co-primary with Tier 2

**The owner's words (2026-11-26, this session, typed):** "Co-2 is co-primary with tier 2."

**What the ledger already says.** Core RULE L17: "Co-2 = OT professional body CPGs (co-primary with Tier 2)". 2026-11-14: "Co-1 stays full, Co-2 full too" (L6989). The extract of part-6 reported "Co-2 full too" correctly.

**How each document phrases it:**
- `governance/tier-system.md:18`: a row of its own, with no co-primacy sentence. L16 has one for Co-1 ("Co-1 ranks alongside T1 …").
- `governance/mission-and-epistemics.md:93`: "**OT professional body CPGs** — parallel to Tier 2". L99 encodes "Co-2 records carry `tier: 2, evidence_type: co2`", which is consistent.
- `governance/evidence-architecture.md:42`: "**Co-2** — OT professional-body CPGs, co-primary with T2." Correct.
- `governance/decision-protocol.md:77`: "3. Evidence-tier definitions (1–6 + Co-1)". Co-2 is left out of the always-DG-NON list.

**What changes:** wording only (mission L93, tier-system L18, decision-protocol L77).

**What does not change:**
- The marker: both ● (OD-57).
- Selection of the best value: tier sets the marker and the weight, not eligibility (Unification U1; harm test "if so, research wins. if no, code wins").
- Encoding (`tier 2, evidence_type co2`).

**One open consequence (OWNER-ONLY).** OR-6c says divergence between different tiers states the higher figure, and that "Co-1 and T1 are same value", so a Co-1 v T1 divergence "waits for an approach written by an Opus-class session". Does a Co-2 v T2 divergence now count as same rank in the same way? The words "co-primary" match the Co-1/T1 wording. That is a reading, not a ruling.

**Proposed edits:**
- mission L93: replace "**OT professional body CPGs** — parallel to Tier 2" with "**OT professional body CPGs** — co-primary with Tier 2".
- tier-system L18: append to the last cell: "Co-2 is co-primary with T2 (owner, 2026-11-26: \"Co-2 is co-primary with tier 2.\")."
- decision-protocol L77: replace "3. Evidence-tier definitions (1–6 + Co-1)" with "3. Evidence-tier definitions (T1–T6, Co-1 and Co-2)".

**Proposed ledger entry** (append-only; not written):

```markdown
## Owner statement 2026-11-26 — Co-2 is co-primary with Tier 2

**Owner's words, quoted (typed):**

> "Co-2 is co-primary with tier 2."

**Readings.** [ASSUMPTION: the statement restates the Core Doctrine RULE ("Co-2 = OT professional body CPGs (co-primary with Tier 2)") and does not change the circle table, under which both carry ● — basis: the RULE and "Co-1 stays full, Co-2 full too" (2026-11-14)]. [ASSUMPTION, for the owner to confirm: as with Co-1 and T1 under OR-6c, a divergence between a Co-2 and a T2 figure states neither over the other and waits for an approach written by an Opus-class session — basis: the word "co-primary", matching the Co-1/T1 wording; not applied until confirmed].

**What this does.** Text calling Co-2 "parallel to Tier 2", or leaving Co-2 out of the evidence-tier definitions, is corrected where it stands: `governance/mission-and-epistemics.md` (the evidence-hierarchy table), `governance/tier-system.md` §1 (the Co-2 row), `governance/decision-protocol.md` §2.4 item 3.

**What it does not decide.** The OR-6c reading above.

CONDITION: any session ranking, marking or weighing a Co-2 source against a T2 source, or editing the tier ladder.
ACTION: (1) Read Co-2 as co-primary with T2. (2) Correct the three passages named. (3) Do not apply the OR-6c reading until the owner confirms it.
DATE: 2026-11-26 — owner statement (typed words, quoted above).
```

Approval: ALREADY-SETTLED (the wording and the entry). OWNER-ONLY (the OR-6c reading). [CONFIDENCE: high]

---

## ADJ2-C1 — functional-taxonomy.md's 17 axes and the retired axis layer

**Verdict.** `governance/functional-taxonomy.md:1-10` reads "Two-Layer Model (Axes × Profiles) … RATIFIED … Doctrine OPERATIVE", and at L125 "17 axes (Layer 1)". The database has no `axes` table: the live `sqlite_master` lists none named like `%axis%`/`axes%`. `scripts/migrations/109_drop_axes.sql:1-15` retired the layer "as one act (plan step 1.4; RULINGS R3 and R35)". Its header says "the documents R35 declares stale (D-0170, D-0184, functional-taxonomy) are not edited here and stay an owner merge."

**What retired it:**
- The owner's words on the term: "I don't want axis to be used" (2026-08-24, L800-820); "'AX-' for ICF should never ever exist anywhere." (2026-09-13).
- RULINGS R35 "Ruled retired" (`workplan/pipeline-state-graph/RULINGS.md:77`), made under the owner's 2026-10-14 delegation ("§4 … resolve them for me in a logical manner").

Layer 2's substance (anti-umbrella, design-equivalence exception, owner 2026-07-22/23) is live in the ledger.

**Proposed reconciliation.** Add one dated line under the Status block:

```
> **Historical as to Layer 1 (2026-10-14).** The axis tables were dropped by `scripts/migrations/109_drop_axes.sql` (RULINGS R35, under the owner's delegation of 2026-10-14); ICF codes with their names (`base_icf`), access needs and identities replace them (owner, 2026-09-13: "access needs, ICF codes, disability identities"). Layer 2's rules are the ledger's 2026-07-22 and 2026-07-23 entries; read the rest of this file as history.
```

Approval: OWNER-ONLY (the doctrine was ratified by the owner, and migration 109 reserved this edit to "an owner merge"). [CONFIDENCE: high]

---

## ADJ2-C2 — conceptual-model.md ENT-08 Item

**Verdict.** `governance/conceptual-model.md:25` lists "ENT-08 | **Item** | … DEFERRED to A6". L92 says "The `item_code` field on Specification already encodes this. Item is the Part 4 organizing unit." Both are false:
- `PRAGMA table_info(specifications)` has no `item_code`.
- The owner ruled 2026-08-26 "`items` is the render rollup", then 2026-08-27 that `items` is "retired as a table name outright".
- The item layer was deleted on 2026-09-01 ("the item-layer deletion (2026-09-01) stands", 2026-11-06, L5005-5031).
- Element pages are derived (OR-14, "never a container").

**Proposed reconciliation.** One line above §2.1:

```
> **ENT-08 Item is no longer an entity (owner, 2026-08-26 and 2026-09-01).** A determination is keyed on the canonical parameter; the item tables were dropped; an element page is derived from typed term pointers to its parameters' determinations (OR-14, 2026-10-29). Sentences here naming `item_code` or Item as an organising unit are history.
```

Approval: DELEGABLE (it applies owner rulings; it is not doctrine creation). [CONFIDENCE: high]

---

## ADJ2-C3 — mission-level "population" text and the lens ruling

**Revised: first-pass ADJ-03 (a) is confirmed below, so this is an optional wording change, not a conflict.** **Verdict (original).** `mission-and-epistemics.md:40` says "Population codes are organizing scaffolding". This contradicts:
- The owner on 2026-08-28: "we don't use the word 'population' though…".
- `population_code` retired in favour of lens columns (2026-08-28, D-0182). The lens set is three since the medical lens was deleted on 2026-11-16.
- `populations` renamed `base_taxonomy_identity` (2026-10-20).

"Population Mode" (L61) is the design-scale name (`design_scale` values), which the ruling does not reach.

Population Mode's "median as default" is superseded only in prose, by the Unification entry, and only as an [unratified reading]. Not proposed here.

**Proposed reconciliation.** In L40, replace "Population codes are organizing scaffolding" with "Identity, ICF and access-need codes (the three lenses) are organizing scaffolding".

Approval: OWNER-ONLY (decision-protocol §2.4 item 1, mission framing). [CONFIDENCE: medium; the 2026-08-28 ruling names tables, columns and codes, not prose]

---

## ADJ2-C4 — One order of authority

**Verdict, the clean order:**
1. A later owner statement (rule 0; "a later owner statement supersedes them on contact", 2026-11-19).
2. Owner rulings recorded in the ledger, newest first (`ANSWERED BY THE OWNER`; a merge ratifies what it carries unless noted, 2026-07-24).
3. Delegated resolutions (`RESOLVED UNDER DELEGATION`, check confirmed or not required), only within their grant and never against (1) or (2): conditions (a)–(e) of 2026-11-12, and OD-79.
4. Ratified decision records, including DR-2026-08-19 as the ledger amends it.
5. `governance/` doctrine.
6. CLAUDE.md.
7. Workplans, task files and skills, which bind only as they apply the above.

**Texts that state it wrongly or incompletely:**
- `CLAUDE.md:21-23` ranks the DR over CLAUDE.md "unless a live owner ruling has superseded the instrument". It omits the ledger's dated rulings and delegated resolutions.
- DR §A L17-25: "Two documents remain live alongside this one … Everything else is superseded." This is stale: the governance doctrine and the remediation workplan bind.
- DR §8 L563-578: "A fresh session reads exactly four", two of them marked SPENT/HISTORY in the same list.
- `CLAUDE.md:538` and `.claude/commands/orient.md:25` both say "DR-2026-08-19 … — what to do now". The DR's §3 "next act" (L323-329, OD-A…OD-G of 2026-08-22) is overtaken: OD-B was answered by D-0165 (2026-10-29 third), and the item links OD-A asked about were dropped. The owner's live plan is "this remediation plan" (2026-11-25).

**Proposed reconciliation.**
- (a) CLAUDE.md L21-23: replace "Where it disagrees with `decisions/DR-2026-08-19-research-restart-operative-instrument.md`, that instrument wins and this file is what to correct — **unless a live owner ruling has superseded the instrument itself, per rule 0, in which case the ruling wins over both.**" with "Order of authority: a later owner statement (rule 0); then owner rulings in `references/project-standards.md`, newest first; then delegated resolutions there, within their grant and never against an owner ruling; then ratified decision records (including `decisions/DR-2026-08-19-…`, as the ledger amends it); then `governance/`; then this file, which is what to correct where it disagrees."
- (b) CLAUDE.md L538 row: replace the target with "`/orient` (derives the live state); the active plan is the one the newest ledger entry names".
- (c) `.claude/commands/orient.md:25`: replace item 1 with "the newest entries of `references/project-standards.md`, which name the active plan".
- (d) DR: one dated line at the top: "> **2026-11-26: read §1.4, §6, §7 and §12.0 (as amended) for their rules; §A, §3, §8 and §9 are history — the live plan is the one the newest ledger entry names.**"

Approval: DELEGABLE ((a) does not alter rule 0's text; the owner may prefer to approve it, since the 2026-11-20 third entry keeps rule 0 for the owner). [CONFIDENCE: high]

---

## ADJ2-C5 — Live scope of the rule-10 suspension

**Verdict.** The 2026-11-20 (fourth) owner words, "no, just do a big pull request so i don't have to waste time", suspend rule 10 for one PR only. That is an [ASSUMPTION] in the ledger L8226: "for this one pull request and on contact … the rule stands for every other pull request". The translation and verification work merged on 2026-11-20 (merges `4f12d50` PR #243 and `778e162` PR #244). The suspension is therefore spent. [UNVERIFIED which of the two PRs was "the big pull request"; `git log --merges --since=2026-11-19`.] Rule 10 stands in full; no change.

**A conflict found while checking.** The owner on 2026-11-21: "I think GAP-368 points towards Claude having permission to hand edit as required for specific columns" / "We don't need a tool for many qualitative judgments/corrections because Claude IS a tool. We just need to ensure that you make transparent and record your hand fixes" (L8263-8282). `CLAUDE.md:294` still says "**Do not hand-write SQL against a table the CLI can reach.**" with no exception.

**Proposed reconciliation.** Append to that CLAUDE.md paragraph:

```
Exception (owner, 2026-11-21): a qualitative value or wording cell may be corrected by hand in a data migration, the old value, new value, reason and session recorded in the migration header and the gap's resolution; identifiers, keys, vocabularies, counts and bibliographic fields stay behind their writers.
```

Approval: ALREADY-SETTLED. The column list stays OWNER-ONLY (C8 Q7). [CONFIDENCE: high]

---

## ADJ2-C6 — CLAUDE.md rule 9 and the harness default to subscribe

**Revised: overturned by first-pass ADJ-06, which is confirmed below.** Rule 9 governs, but its enforcement sentence and the settings.json deny names are stale. The original reading follows. **Verdict (original).** No conflict. Rule 9 is the owner's instruction (2026-09-23). The harness gives the user's instructions precedence, and rule 9 already says the default subscription defers to it and requires the unsubscribe step. The 2026-11-15 end-of-batch sweep ("commit, push, and say in the PR") sits inside rule 9's "except a deliberate change". No change. [CONFIDENCE: high]

---

## ADJ2-C7 — The proposed CLAUDE.md rewrite of 2026-11-20 (third)

**Revised: see first-pass ADJ-07, confirmed below.** The remainder is a live, unapproved proposal, and its ACTION ("Do not rewrite `CLAUDE.md` until the owner approves", L8214) binds. The facts below stand. **Verdict (original).** It landed in part. Not live as a whole, and not owed.
- Landed: commit `94dbaed` ("CLAUDE.md opens on the owner's goal; delete the Layer-0 preamble and the stage_label clause", 2026-11-20). CLAUDE.md now has the Goal and the three "never got wrong" items, merged and so approved (2026-11-20 fourth: "merging approves it").
- Not landed: the move of rules 0, 1, 4, 5, 6, 9, 10 and §§3, 7, 8 to a working-rules file; deletion of the "Proof" narratives; and the size test (`[ $(wc -w < CLAUDE.md) -le … / 4 ]`). CLAUDE.md still carries all of them.
- The owner's later "maybe claude.md goal should also state this is a simple project…" (2026-11-25 seventh) landed as `53ada81`.

The remainder is an unadopted proposal. Nothing makes it owed.

Proposed: no change unless the owner re-commissions it (C8 Q10). Approval: OWNER-ONLY. [CONFIDENCE: high]

---

## ADJ2-C8 — Open owner-only questions (verified against the full ledger)

Each is put as a plain question, with options and the cost of each.

1. **GAP-379, second part.** Should ICF `e120` reach LPA, TALL and BAR through A-SIZE's row?
   - (a) Yes, one triple per identity. Cost: three rows for the owner to review.
   - (b) No. Cost: the body-size group keeps no environmental ICF coverage.
   Open per the last line of L8582-8624: "GAP-379's `e120`/A-SIZE question for LPA, TALL and BAR stays open."
2. **The two class-C pairs** (BRAIN with A-NOSPEECH; COM with A-LOWLOAD). OD-85 rejected them under delegation "with no row changing state"; retiring a row is the owner's mechanism (L8592, L8623). Retire them?
   - (a) Retire both. Cost: two reviews.
   - (b) Keep them as proposals. Cost: they stay visible as unwarranted inferences.
3. **OD-67.** Answered 2026-11-19 ("yes, one answer on the full list, VES withheld"). Moot while T-128 is withdrawn (OD-87). Nothing to ask unless T-128 returns.
4. **OD-77.** Resolved under delegation: `identity_icf_map` is read as the mapping you doubted, and session additions are frozen. Is that the mapping you meant by "I don't think the mapping is correct"?
   - (a) Yes. No cost.
   - (b) No, name it. Cost: OD-77 reopens.
   This is owner meaning, which OD-79 reserves; the 2026-11-25 sixth statement delegated it, so this is a confirmation only.
5. **Observation 71.** What does "accessible route" name: a held term, a new term, or neither? And does the alias "accessible route" on TERM-048 stay? Open since 2026-10-29 (fifth): "Observation 71 is adjudicated only on the owner's answer to its prompt."
6. **OR-5b's three edges** (open; `OR-5b STATUS: ANSWERED BY THE OWNER, PARTLY`, L6174):
   - (i) Does "academic rigour re PubMed" mean indexed in PubMed, or meeting the standard of PubMed-indexed work? The first collides with R5.
   - (ii) How is a DPO statement or lived-experience publication shown to be sound?
   - (iii) Is the test for Co-1 only, or for every tier?
   Cost of leaving them: T-4's Co-1 value rule cannot be built. Note also that "PARTLY" is not a value the gate convention defines, so the gate reads it as OPEN and overstates it. Adjudication-3 item 67 recommends splitting it.
7. **Which columns count as "qualitative"** for hand correction (2026-11-21)?
   - (a) The [ASSUMPTION] list (qualitative judgment and wording columns).
   - (b) A named list.
   Cost of (a): drift case by case.
8. **Matrix rows 46 and 47** (EPI with e260; COM with e240), proposed for rejection: accept or reject? (2026-11-21 fifth.) [UNVERIFIED whether OD-85 or OD-86 reached them.]
9. **Does "medical codes" reach the `terms` rows with `domain='medical'`** (search vocabulary, kept for now)?
   - (a) No, keep them.
   - (b) Delete them. Cost: search recall.
   (2026-11-16 correction, [OPEN].)
10. **CLAUDE.md rewrite remainder.** Resume, drop, or leave? (C7.)
11. **Co-2 v T2 divergence rank** (B).
12. **Six marker sub-points** (A).
13. **`evidence_population_match` column names.** Rename to `study_group` / `served_group`? Cost: a rename with a caller sweep. (LED-127; 2026-10-20 [OPEN].)
14. **Branch protection.** The 2026-04-19 rule ("ruleset stays DISABLED during Phase A") presumes a phase the PR workflow (rule 9) has left. Re-enable or keep off? Repository access control is the owner's.
15. **OR-6c consistency.** Unification (c) supersedes OR-4 and OR-6c "as to selection" only. Edits "follow the adjudication through this ledger and a tooling PR" (L7173-7187). Nothing for the owner unless T-059 finds a case.

---

## ADJ2-C9 — Other conflicts and stale statements

| # | Conflict | Evidence | Proposed reconciliation (exact) | Class |
|---|---|---|---|---|
| 1 | CLAUDE.md §3 says both that base is gated "as a stage" and "Convention: `base` is not a stage" | `CLAUDE.md:270` against the owner 2026-08-27: "base is a stage insofar as it supplies the base information…" (L2298-2345) | Replace L270 with: "Convention for counting cross-stage views: a view reading one stage plus `base` is not counted as crossing, because every stage points into `base`." | DELEGABLE |
| 2 | Synthesis floor | `CLAUDE.md:381` "Only Opus-class models write `best_practice_synthesis`" against the owner 2026-07-25 "best_practice_synthesis can be fable as well" (ACTION (3): "Opus-class or above, which includes Fable-class", L609) | See F4 | ALREADY-SETTLED |
| 3 | Stored `not_applicable` | `CLAUDE.md:373` "Cell states: `stated` / `provisional` / `pending` / `not_applicable`"; `mission-and-epistemics.md:118` row; evidence-architecture L26 and L116. Against OR-1 "Do not store table rows for parameters when there is a missing lens…" (2026-10-29; live SUPERSEDES pair in evidence-methodology) and OD-08 (no row for a cell without a figure) | CLAUDE.md L373: "Cell states: read them from the `specifications.state` CHECK (`dbcore.check_values`); no row is stored for a parameter and lens it does not concern (OR-1, 2026-10-29)." In mission L118, append to the meaning cell: "Not stored for a determination since 2026-10-29 (OR-1); a judged triple may still carry it." | ALREADY-SETTLED |
| 4 | "never bare axis codes" names a vocabulary that no longer exists | `CLAUDE.md:378`; migration 109 | Replace "never bare axis codes" with "never bare codes" | DELEGABLE |
| 5 | T1 "occasionally `grey`" | tier-system.md:15 against the owner 2026-11-06: "if government report is academically sound then it can be t3 I think" (ledger open item: "its correction is queued as a doctrine change") | Replace "`clinical`, occasionally `grey` for unpublished primary" with "`clinical`" | OWNER-ONLY (tier definition; the owner's words support it) |
| 6 | Ledger rule (2026-08-22) names a retired authority | L663-694 "`governance/pipeline-map.yaml` for wiring"; the file is at `_archived/governance/pipeline-map.yaml` | No ledger edit. The CLAUDE.md §3 sentence already says it is retired; add nothing | no change |
| 7 | Ledger rule (2026-04-19) names a missing validator | `scripts/validate_bpc.py` absent; `validate_cross_refs.py` present | History; no change | no change |
| 8 | Contract anchors and header | see F1, F2, F4, F5 | — | — |
| 9 | `.claude/commands/orient.md:25` | see C4 (c) | — | DELEGABLE |

---

## ADJ2-D — Cross-slice resolution of [STATUS UNCERTAIN] and [CHECK] tags

Tag counts: `for f in ps-clean/part-*.md; do grep -c 'STATUS UNCERTAIN' $f; grep -c '\[CHECK' $f; done`. The convention and stats lines are not counted below.

**STATUS UNCERTAIN, one by one**

| Tag (extract:line) | Resolved? | How | What remains |
|---|---|---|---|
| p1:95 VIS/DEAF/DBL "AMENDED 2026-11-06" | Yes | p5 2026-11-06 (L4943-4955): the code table is `base_taxonomy_identity` | Codes read BLIND/DEAF/DEAFBLIND (2026-07-24); the distinctness principle stands |
| p1:191 CO-0004 Part Map | Yes (amendment) | Same 2026-11-06 entry | Whether "TRANSITIONAL" ended [UNVERIFIED] |
| p1:449 session start protocol | Yes | 2026-11-06: `/session-open` then `/orient` | none |
| p1:487 connections "[RETIRED — CO-0009]" | Yes | The live `connections` table exists, so the label refers to the markdown files | none |
| p1:493 orchestrator re-read | Yes | Skill deleted (2026-11-06) | none |
| p1:867 citation mining "[SUPERSEDED — CO-0009]" | Yes | The `citation_mining` table is live; the label refers to the markdown register | none |
| p1:1003 adversarial review amended 2026-10-09 | Yes | p4 2026-10-09: one-plan exception; rule otherwise unamended; 2026-11-20 correction files standing findings as gaps; the one-pass rule unchanged | none |
| p2:27, p2:49 MOB / `item_population_links` | Yes | Item layer dropped (2026-09-01); MOB family 2026-11-12 fifth/ninth sets (MOB parent; WHEEL incl. SCI; LLD; WALKAID; AMB not minted) | none |
| p2:175, p2:217, p2:310 (medical half) | Yes | Owner 2026-11-16: "delete medical taxonomy , medical maps and medical codes btw" (L7688) | none |
| p2:299 identity v `base_taxonomy` confirmation | Mostly | 2026-10-20 delegated recording renamed the registry and column | `evidence_population_match` column names (C8 Q13) |
| p2:310 exactly-one v at-least-one | Yes | D-0182 (2026-09-09 ledger); the link table (OD-39, 2026-11-13) | Whether determinations take a link table (OI-55) |
| p3:31 add-term amended 2026-10-09 | Yes | p4 2026-10-09 D3; 2026-11-06 (93 subjects); 2026-11-06 seventh (base grounds itself); OD-71 | none |
| p3:243 "PRESENT BOTH" amended | Yes | OR-10 (2026-10-29 second), OD-22, OD-42 | none |
| p7:435 CLAUDE.md rewrite | Yes | Landed in part (C7) | C8 Q10 |
| p7:449 one big PR | Yes, probably | Merged 2026-11-20 (#243/#244) [UNVERIFIED which] | none; rule 10 stands |
| p7:598 OD-79 scope | Yes | The sixth statement covers only the questions it names; OD-79 holds elsewhere | none |

**[CHECK] tags, grouped**

| Group (extract:lines) | Resolved? | How | What remains |
|---|---|---|---|
| Medical lens: p3:8,68,79,87,98,209,212; p4:357; p5:628,647,715; p6:32,58 | Yes | Deleted 2026-11-16; three lenses; OI-48's "medical lens" clause now reads "keep impairment level in ICF codes" (2026-11-16 correction) | C8 Q9 |
| Item layer / item codes: p1:106,138,155,506; p1:921; p2:205,280 | Yes | Dropped (2026-09-01); `[A-Z]-NN` is prior-version content (CLAUDE.md §7) | none |
| Population codes, IntD, BAR, Category J: p1:27,74,96,98,263,608,902 | Yes | 2026-07-24 scheme; lens columns (2026-08-28); `identity_code` (2026-10-20); identity sets 2026-11-12 | The Category J and THIN-BASE IntD clauses are prior-version content |
| Stage list and pipeline-map: p1:1022,1126; p2:80,90 | Yes | Seven stages (2026-08-27); `pipeline-map.yaml` archived; table→stage is `stage-map.yaml` | none |
| Crossing / applicability: p1:1105; p2:38,47 | Yes | "overrule Aug 24 DR. we go evidence>judgment>synthesis" (2026-08-27); "yes lens in judgment" (2026-11-14) | none |
| Junction shape: p2:37 | Mostly | OD-39 link table for figures | OI-55 for determinations |
| "Whether done", done: p1:1104 (`search_executions` has lens columns); p2:36 (R4 string absent from research-contract.yaml); p2:57 and p3:7 (`specifications` has no `population_code`/`item_code`); p4:172 (`search_executions.updated_by_session` present); p2:277 (DR-2026-08-27 files exist; `ls decisions \| grep -c DR-2026-08-27`); p3:157 (`floor_mean()` exists) | Yes | Live schema and tree | none |
| "Whether done", not done: p2:160 (`evidence_sources.tier` still stored; OD-70 computes it, `adjudication_integrity` holds it) | Partly | OD-70 | The writer-retire move |
| "Whether done", unverified: p2:127, p2:195, p3:40, p3:50, p3:228, p4:25, p4:209, p5:38, p5:537, p1:977 | No | [UNVERIFIED] — not traced in this pass | Re-derive per item |
| Later rule-5 form: p1:1029,1038,1060,1075 | Yes | CLAUDE.md rule 5 (AFTER_DATA ordering) is later | none |
| Recorder principles: p1:974,1066; p3:135 | n/a | Recorder text, not owner words | Read as unratified |
| Search-first v structure-first: p1:994 | Yes | Compatible: grep finds prior work and places to edit; structure decides facts | none |
| Stale state: p1:1133; p3:109; p4:114; p4:321 | Yes | Corpus cleared 2026-09-13; re-derive rather than quote | none |
| Process: p1:733 (Phase A) | No | — | C8 Q14 |
| Process: p1:754 (code co-production) | Yes | Superseded in practice by 2026-11-06 minimise code | none |
| Process: p1:851 (A12) | History | — | none |
| Process: p1:726 (validators) | Stale | `validate_bpc.py` missing | none |
| Process: p1:192 | No | [UNVERIFIED] | — |
| Process: p1:240 | Yes | Superseded (2026-11-15 T-001 record) | none |
| Process: p1:474 | Yes | Rule stands | none |
| Process: p1:531 | History | — | none |
| Process: p1:696 | Yes | connection-scout absorbed into connection-discovery (D-0146) | none |
| Naming: p2:12,22,163 | Yes | MOB is the parent identity; underscore and `base_` | none |
| Naming: p2:110 (attribution) | No | [UNVERIFIED] | — |
| Nomenclature audits: p2:118,137,139 | Partly | — | `evidence_population_match` still has `source_ref` beside `ref_id` (live) — the rule-5 dual home is open |
| Medical/ICD and AX-: p3:78,189 | Moot | Medical deleted; axes dropped | WHO payloads still serve the ICF glossary |
| Leads: p3:231 | Lead only | — | Confirm against full text |
| Retire in place, freeze: p3:167,170 | Yes | Retire-in-place 2026-09-16; DR §2.5(c) spent | none |
| Jurisdiction floors: p4:199,200,520; p5:26,388,390 | Yes | OD-04 (P1+P2+P3 replaces buckets 1-2); OR-8; OD-34 "Instruments only" | How OD-05's "exhaustion" reads after OD-04 — the reading: P1+P2+P3, for codes and standards |
| D-labels: p4:241 | Partly | OR-8, -14, -15, -16, -17 answer D4, D6, D13, D10/D11, D5; D7 → OD-69 | D9 (Release 0), D12 [UNVERIFIED] |
| Owner later answered: p4:336 (net-negative → 2026-11-06); p4:367 (OR-1c → 2026-11-06); p5:18,670 (ALL → OD-31; LMB → UPL); p5:110 (licences → OD-15, then the 2026-11-19 licensing default); p5:441 (OD-10); p5:567 (OD-32); p6:24 (OR-6c → Unification (c)); p6:29 (OD-52 answered 2026-11-19); p6:166,319 (roots shown as a count); p6:621,888 (OD-64); p6:664 (moot under ⚠); p6:701 (OD-59); p7:602 (OD-87) | Yes | Ledger lines as cited | none |
| Delegated, settled: p5:207,234,235,248,260,330,379,708,728 | Yes | OD-03, -01, -02, -24, -25, -30, -38/-72, -75, OI-50 | none |
| Marks owed: p4:370 | No | mission L118 still lists `not_applicable` | C9 #3 |
| Pending work: p6:800 | Owed | T-059 | none |
| Pending work: p7:97 | Yes | `identity_need_icf` (T-145) is the identity–need link | none |
| Pending work: p7:212,254 | No | — | Domains; OD-69 "list … not fixed" |
| Pending work: p7:243 | No | — | Owner question: CSA/ISO exactly, or standards bodies generally |
| Pending work: p7:270 | Verified | T-120 and T-117 not landed (A) | none |
| Pending work: p2:269 | Rule 7a | — | Quote the command, never the figure |

---

## ADJ2-E — Delegation audit

These are the cases I can prove.

1. **OD-43 (delegated, 2026-11-13)** limited `convergent` to Tier 1–3 and Co-1. The owner overturned it on 2026-11-14: "you can still converge across tiers like a tier 1 and a tier 6 proposing same value" (L6639-6698). The ledger already records OD-43 as ANSWERED BY THE OWNER and the delegated limit as overtaken. Nothing owed.
2. **OD-05 (delegated, 2026-11-12)** said that out-of-scope evidence is "never admitted before exhaustion". The owner narrowed it with OD-34: "Instruments only: a T1–T3 study is admitted on its merits" (L5971-6012). It is recorded. Nothing owed.
3. **OD-14 (delegated, 2026-11-12)** concluded that an owner rule no longer bound because a later ruling had removed its basis. That is condition (e) overreach. It was withdrawn the same day (L5747-5760) and answered by the owner (third, fifth, eighth and ninth sets). Nothing owed.

**Reserved matters inside an express grant (not overreach):**
- OD-02 (page language; audience). The owner named OD-02 in "I guess opus can do it".
- OD-83 (SCI into WHEEL; population taxonomy). It rests on the owner's "SCI is the same as WHEELCHAIR basically", and OD-82 was named in the 2026-11-25 sixth statement.
- OD-85 (the 29 pairs; "a group has a need"). Named in the sixth statement, with "no row changing state".
- Migration 109 / R35 (axis layer retired, after the 2026-09-13 entry had called its survival "owner-gated"). Made under the owner's later 2026-10-14 delegation of §4. Rule 0 favours the later grant.

**Risks, unproven:**
- **OD-12 / OD-33.** These put the render table outside `data/guidebook.db`, generated at build. The owner wrote "I expect the render table to be one where the specification table rows have been converted into complete prose…" (OW-1) and "i want it to be coming from database directly in ideal world" (2026-10-30). "Generated from the database at each build" may meet both. Not proven; the owner may reverse OD-33 at any time.
- **2026-11-19 "Ratify all".** This turned nine reserved items (OD-17, -46, -47, -48, -51, -52 …) into ANSWERED BY THE OWNER on a reading the ledger itself marks: "[ASSUMPTION: 'all' includes OD-17 … the owner has not been shown the contract diff in this session]" (L7983). These are owner words, so not a delegation defect. But OD-17's own condition ("once I have read the corrected contract", L6067) is recorded as unmet. See F1.

---

## ADJ2-F1 — Contract `ratified: false` against OD-17

**Verdict.** `governance/pipeline-contract.yaml:3` reads `ratified: false`, and L7 says "Ratifying the corrected contract is owner decision OD-17". The ledger:
- `OD-17 STATUS: DEFERRED BY THE OWNER` (L6068), on "Ratify after T-022 merges, once I have read the corrected contract".
- Then `OD-17: the corrected contract is ratified (the owner's act; its condition, T-022 merged, is met)` / `OD-17 STATUS: ANSWERED BY THE OWNER` (L7986-7987), on "Sure, append. Ratify all."

So the header is stale. The trailing note (L395-396), "OD-17 ratified the contract before it was made", is also true: the item-68 note was appended on 2026-11-19, after the ratification, so that later change is not covered by it. `scripts/audit/pipeline_contract_audit.py:167` prints the field, and nothing gates on it.

**Proposed reconciliation.** Replace L3-7 with:

```yaml
ratified: true
# Ratified by the owner 2026-11-19 (ledger: "Owner ratification 2026-11-19", OD-17: "Sure, append. Ratify all.").
# The owner had asked to read the corrected contract first (OD-17, 2026-11-12); the ledger records that the
# diff was not shown. Text added to this file after 2026-11-19 is not covered by that ratification.
```

Approval: ALREADY-SETTLED (the header follows the status line). The owner may want to confirm, given the unmet read: OWNER-ONLY to confirm. [CONFIDENCE: high]

---

## ADJ2-F2 — Stage anchors against the 2026-08-27 spine

**Verdict.** The owner's words (2026-08-27): "you research slugs, evidence research, judge evidence, synthesize judgments, specify syntheses, and render specifications." The contract is out of line with them:
- `judgment` anchor (L185): "the 4-state determination machine + convergence + directness (evidence-architecture.md §5)".
- `synthesis` anchor (L275): "… Opus-only (rule #2)".
- `specification` anchor (L286): carries the determination but not the state machine.

The contract's own 2026-11-19 note says the edit "has NO task … The rule change itself is an OPEN POINT". It is not open as a rule: the note itself says "What now governs … is the owner's spine … directness belongs to `judgment`, convergence to `synthesis`, and the determination machine to `specification`" (L387-389, ratified with adjudication item 68 by "Ratify all"). Only the text edit is missing.

The judgment item is also ruled. Owner 2026-08-27: "delivers a verdict on an evidence item for what tier of evidence hierarchy it belongs to (1, 2…6)" · "determines category of judgment item, derives value/process/figure/goal for it".

**Proposed exact anchors:**
- `judgment`: `'the judgment item: each extracted, tiered and categorised value of an evidence item (source_value_extractions), its tier computed from evidence type and scope (OD-70), its directness, and its lens tags (owner 2026-08-27: "judge evidence"; "yes lens in judgment", 2026-11-14)'`
- `synthesis`: `'what the judgments say together: convergence (computed in the engine, OD-07), judged relations (OD-25), conflicts and judged discussion; best_practice_synthesis authored at the Opus-class-or-above floor (DR-2026-06-10; owner 2026-07-25) (owner 2026-08-27: "synthesize judgments")'`
- `specification`: `'the determination and its state machine: the ideal for a cell and its context, graded for evidence — "therefore 1200 mm, marked ●" (owner 2026-08-27: "specify syntheses"; 2026-11-14: "determination means to determine the ideal within the context of all evidence factors…")'`

Then delete the two trailing comment notes (L383-396). They are superseded by the edit, and "hand-written atoms cite the lines above by number", so re-check those atoms (rule 4).

Approval: DELEGABLE (it applies owner words; the text was ratified by OD-17's "Ratify all" only as far as the note goes). [CONFIDENCE: medium-high]

---

## ADJ2-F3 — Translation default stage

**Verdict.** Carried out.
- `pipeline-contract.yaml:380-381`: `translation: default_stage: judgment`, with the owner's "yes, translation runs before judgment" cited at L378.
- Callers read the contract, not a literal: `scripts/db.py:14640`, `scripts/tests/test_translations.py:121`, `scripts/tests/test_db_amend_writers.py:4556`.
- `git grep -n -i -E 'translat[a-z]* (runs|happens|at) synthesis|synthesis (stage )?translates|translation.{0,40}synthesis' -- governance skills scripts architecture .claude CLAUDE.md` finds nothing outside the contract's own history comment.

No change. [CONFIDENCE: high]

---

## ADJ2-F4 — Synthesis model floor

**Verdict.** The rule is "Opus-class or above", which includes Fable-class:
- DR-2026-06-10 decision 1: "Rule #2 is a capability floor, expressed as 'Opus-class or above.'"
- Owner 2026-07-25: "best_practice_synthesis can be fable as well. opus 5 is clearly opus class…". ACTION (3): "Opus-class or above, which includes Fable-class" (L609).

Right: `decision-protocol.md:149-150` ("`fable` is a synthesis-capable tier alongside `opus`").

Wrong:
- `CLAUDE.md:381` "Only Opus-class models write `best_practice_synthesis`", which reads as excluding Fable.
- `pipeline-contract.yaml:275` "Opus-only (rule #2)".
- Incomplete: `pipeline-contract.yaml:281` "(Opus-class)" and `governance/pipeline-operations.md:57` "gated to Opus-class authorship".

**Proposed:**
- CLAUDE.md L381: replace "Only Opus-class models write `best_practice_synthesis`." with "Only Opus-class or Fable-class models (the Opus-class-or-above floor, DR-2026-06-10; owner 2026-07-25) write `best_practice_synthesis`."
- Contract L275: covered by F2.
- Contract L281: replace "(Opus-class)" with "(Opus-class or above, which includes Fable-class)".
- pipeline-operations.md L57: replace "Opus-class authorship" with "Opus-class-or-above authorship".

Approval: ALREADY-SETTLED. [CONFIDENCE: high]

---

## ADJ2-F5 — The `doctrine-recheck` cross-stage criterion

**Verdict.** `pipeline-contract.yaml:360-364`: "A doctrine recheck fires at every stage transition and every 25 sessions." This conflicts on two counts:
- `governance/doctrine-recheck.md` §1.2 defines STAGE_TRANSITION as project stages "A→B, B→C", not pipeline stages.
- The periodic cadence has had no counter since DR-2026-08-19 §10 item 4 removed "the frozen recheck counter `data/doctrine_recheck/working_session_counter.yaml`". The DR's own diagnosis: "A standing obligation with a dead odometer: it can never fire, and can always be cited as owed."

`scripts/doctrine_recheck.py` contains no PERIODIC, STAGE_TRANSITION or counter logic (`grep -n -E 'PERIODIC|STAGE_TRANSITION|counter' scripts/doctrine_recheck.py` prints nothing). It validates records and doctrinal cross-references, which the DR retained ("The `doctrine_recheck --cross-ref` CHECK is deliberately **retained**").

**Proposed criterion text:**

```
A doctrine recheck runs at a project stage transition (A→B, B→C; governance/doctrine-recheck.md §1.2) and its record's doctrinal cross-references validate. The 25-session periodic cadence has had no counter since 2026-08-19 (DR-2026-08-19 §10 item 4) and is not enforced.
```

Deleting §1.1 of doctrine-recheck.md would remove an obligation that cannot fire (CLAUDE.md §8). That is offered, not proposed as a default.

Approval: DELEGABLE (process, not doctrine). [CONFIDENCE: high]

---

## ADJ2-F6 — Do the 2026-11-14 rulings change a cell's state or only its marker?

**Verdict.** Only the marker, and which value is shown as best. The ledger does not speak to state.
- OD-57's question is about the marker: "apply the circle table now".
- U6: "if the only values are from code then code determines the ideal/best", which is about which value.
- 2026-10-30 (second): "The best-practice statements decide which value is named, not the band or flag."

No 2026-11-14 entry mentions `stated`/`provisional`. The OD-57 registration's own reason runs the other way: it relies on "`governance/evidence-methodology.md` §2.2 already holds T3 clinical at `provisional`".

So `no-regulatory-stratum-stated` (L299-305) and `tier3-alone-threshold` (L306-310) stand, and are consistent: a T4–T6-only or T3-alone cell stays `provisional`. OD-10 ("'provisional' = thin evidence") agrees. With ⚠ for T3 grey, a T3-grey-alone cell is `pending` (tier-system §8: "T3-grey alone is weak band and `pending`"). The marker changes; the state does not.

No change. The owner may ask whether a code-only best should ever be `stated`. [CONFIDENCE: medium-high]

---

## ADJ2-F7 — The triangle's causes, by stage

**Verdict.** The causes are derived across stages. `stage-map.yaml`: `evidence_sources` evidence; `source_value_extractions`, `evidence_population_match`, `extraction_lens_links` judgment; `convergence_assessment` synthesis; `specifications` specification; `translations` and `gaps` cross-stage.

| Cause | Field read | Its table's stage |
|---|---|---|
| Grey | `evidence_sources.evidence_type` | evidence. The type is judged (OD-70), and the 2026-08-27 ruling calls the tier verdict a judgment output written into an evidence row (move queued) |
| Unverified | `evidence_sources.verification_status` | evidence |
| Thin (proxy) | `evidence_population_match` grades | judgment |
| Thin (vetted judgment or derivation) | not yet recorded (A, open point 3) | — |
| Thin (project inference / mixed value) | `specifications.rests_on_proxy_inference`, `derivation_paths`; synthesis relation rows | specification / synthesis |

The marker is computed once, at specification, into `specifications.marker`: a cross-stage read by pointer, which CLAUDE.md §3 allows. Render must read `specifications.marker` and recompute nothing. A recomputed marker on a render row would be the second home rule 5 forbids.

The contract's `register-invariants` stays UNENFORCED until a render surface keyed on `parameter_id` × lens exists (T-037). No check is added now (§8: no render surface reaches the guidebook yet).

**Proposed.** Append one clause to `register-invariants`' criterion: "the marker shown is `specifications.marker`, never recomputed at render".

Approval: DELEGABLE. [CONFIDENCE: medium]

---

## ADJ2-F8 — `research-tooling-separation` and the one-PR suspension

**Verdict.** The suspension is recorded only in the ledger (2026-11-20 fourth, as an [ASSUMPTION]). `research_tooling_separation` is advisory (CLAUDE.md rule 10: "PARTLY ENFORCED … (advisory)") and reads changesets, not the ledger. It could have reported the big PR and blocked nothing. The suspension is spent (C5). No change; adding a reader for a spent exception would be apparatus with no subject. [CONFIDENCE: high]

---

## ADJ2-F9 — Stage lists, stage by stage

**Verdict.**
- CLAUDE.md §3 SPINE (L245): `base -> research -> evidence -> judgment -> synthesis -> specification -> render`.
- Contract `spine:` and `stages:` ids: the same seven, in the same order.
- `stage-map.yaml` `tables:` values: the seven stage ids, plus `infrastructure` and `cross-stage`. Both are declared in its header as "not a stage".

They agree. The one internal conflict is CLAUDE.md L270 ("`base` is not a stage"); see C9 #1. `stage-map.yaml` carries no `views:` key, although the owner's OW-1 answer ("Yes, map views to a stage") ordered one. That is owed work in T-005/OW-2, not a disagreement.

Approval: DELEGABLE (C9 #1). [CONFIDENCE: high]

---

## Things the extractors may have dropped (spot-checks against the source)

Checked entries: L17, L26, L609, the circle entries L6904-7000, OD-57 registration L7261-7300, the fourteenth set L7297-7345, OD-63/66 L7367-7435, 2026-11-16 L7688-7711, 2026-11-19 L7967-7988, 2026-11-20 fourth L8217-8236, 2026-11-25 grant L8471-8497. Most are faithful. Differences:

1. **OD-57 registration — dropped.** Source L7263: "None is resolved under delegation: Q1 and Q3 set how an evidence tier is marked … which reach the evidence-tier definitions on the decision protocol's always-DG-NON list". Part-6 keeps "Not to be resolved under delegation" only for OD-62. This bears on the approval class of every marker rule (A).
2. **OD-64 — overturned in part-6.** Part-6 lists "[OPEN] OD-64: T3 grey ◐ vs ⚠" in several places. Source L7425: "OD-64 STATUS: ANSWERED BY THE OWNER", "OD-64: triangle for every grey basis". This lies outside part-6's slice; part-7 has it right.
3. **2026-11-25 grant — softened.** Part-7: "The tooling PR … the owner reads it before it merges. [unratified reading]". Source ACTION (1): "The tooling pull request of OD-74 and OD-75 is asked for; the owner reads it before it merges, as the entry of 2026-11-23 says." That is an ACTION, not only a reading.
4. **2026-11-16 — operative fact dropped.** Source: "the rule version of the determination engine moved to `pilot-7` because the derivation hash had a slot for the fourth lens (`test_db_integrity` K01 keeps `pilot-6` on the four-slot form)". Part-7 omits the rule-version change.
5. **2026-11-19 — wording kept, consequence not drawn.** Part-7: "OD-17: the corrected contract is ratified … [unratified reading: the owner was not shown the contract diff]". Source L7983 is the same in substance. Faithful, but no extractor connects it to `ratified: false` in the contract (F1).
6. **OD-61 — stale only.** Part-6: "T-121 is open". The ledger said so; T-121 landed on 2026-11-15 (`7681114`), and CLAUDE.md §7 lists `references/bpc/`. Not a distortion.
7. **L17, L26, L609, 2026-11-20 fourth, the circle entries** — faithful.

---

## First-pass items: confirmed or overturned

Each first-pass item is checked against this pass's own verification. "Confirmed" means the evidence was re-checked and holds.

| First-pass item | Verdict | Notes |
|---|---|---|
| ADJ-01 (axis layer; functional-taxonomy part by part) | **Confirmed.** It supersedes ADJ2-C1's shorter note | Its part-by-part table is finer than C1, so use its annotation text. Class: both passes say the owner merges it (migration 109: "stay an owner merge"). Its CLAUDE.md §9 L542 row change is also confirmed |
| ADJ-02 (conceptual-model item layer) | **Confirmed.** Use its annotation in place of C2's | Migration 107 header and owner reason verified as quoted. Class: ALREADY-SETTLED and DELEGABLE are compatible |
| ADJ-03 (a) "population" in mission: no conflict | **Confirmed.** It overturns this pass's original C3 | The owner still says "populations still get coded" (2026-11-14) and "disability identities/populations" (2026-11-22). The 2026-08-28 ruling names tables, columns and codes. C3's wording change is optional only |
| ADJ-03 (b) "median as default" question | **Confirmed** | Add it to C8 as Q16 (OWNER-ONLY) |
| ADJ-04 (authority order) | **Confirmed.** Equivalent to C4 | Use its fuller DR note, which includes the OD-numbering collision (DR OD-10/OD-11 against register OD-10/OD-11). C4 (c) adds `/orient` L25, which the first pass did not have |
| ADJ-05 (rule-10 suspension expired; PR 243) | **Confirmed.** Replaces C5's [UNVERIFIED] PR number | C5's separate finding (2026-11-21 hand-correction exception missing from CLAUDE.md §4) is not in the first pass and stands |
| ADJ-06 (rule 9 enforcement sentence stale; deny names) | **Confirmed.** It overturns this pass's original C6 ("no change") | Verified: `.claude/settings.json:43-46` denies `mcp__Claude_Code_Remote__…` and `mcp__github__…`; this session exposes `mcp__claude-code-remote__…`. Whether matching normalises names stays [UNVERIFIED] |
| ADJ-07 (rewrite proposal live but unapproved) | **Confirmed.** It overturns C7's "not live" | Ledger L8214: "ACTION: (1) Do not rewrite `CLAUDE.md` until the owner approves the content above". The remainder is a live, unapproved proposal |
| ADJ-08a–e (open owner questions) | **Confirmed** | ADJ-08a's finding that the GAP-379 gap text and OD-85 disagree is not in C8; the ledger, being later, governs. ADJ-08e (SCI, satisfied by merge of T-102) is consistent with E |
| ADJ-09a (circle table not applied) | **Confirmed.** A gives the full §5 text | The interim one-line note is a fallback if T-120 waits. The first pass adds `evidence-architecture.md:82` and tier-system `:98`, `:113` to A's list |
| ADJ-09b (synthesis floor) | **Confirmed in substance, overturned in its proposed text** | Its replacement, "Only a synthesis-capable class … writes a determination (`specifications`)", conflicts with the owner's 2026-09-09: "you have to compute it". A determination is computed by the engine, not written by a model. The Opus-or-above floor binds judged synthesis text (OD-12: "Discussion needing judgment … is a synthesis-stage row written at the Opus floor"). Use: "Only Opus-class or Fable-class models (the Opus-class-or-above floor, DR-2026-06-10; owner 2026-07-25) author judged synthesis text; a determination is computed, not written (owner, 2026-09-09)." |
| ADJ-09c (mission commitment 2, test 3; evidence-architecture :121; commitment 5 against OD-48) | **Confirmed.** Medium confidence, as the first pass says | Commitment 5's question is OWNER-ONLY; add it to C8 as Q17 |
| ADJ-09d (version pins in decision-protocol) | **Confirmed** | `decision-protocol.md:5` reads "(Sonnet 4.6 conversational; Opus 4.6 best-practice synthesis)" |
| ADJ-09e (broken workplan-co0007 pointers) | **Confirmed** | `workplan/workplan-co0007-v3*.md` are absent at top level; `git ls-files workplan/_superseded \| grep -c co0007` is non-zero. Add `tier-system.md` §5–§7 → missing `skills/guidebook-auditor_SKILL.md` (A) |
| ADJ-09f (hand-typed figures) | **Confirmed** (not re-checked line by line) | Rule 7a applies as stated |
| ADJ-09g (DR OD-number collision) | **Confirmed** | — |
| ADJ-09h (mission evidence-type list) | **Confirmed** | `schemas/enums.py` uses `standard_eb` and so on, while the mission list uses longer names |
| ADJ-09i (CLAUDE.md §8 sign-off list narrower than decision-protocol §2.4) | **Confirmed** | `CLAUDE.md:501-502`. The pointer is the rule-5 fix. With B, §2.4 item 3 also gains Co-2 |
| ADJ-09j (CLAUDE.md T3 gloss "grey primary") | **Confirmed** | — |
| ADJ-09k (highest-numbered PI file) | **Confirmed** | `ls … \| tail -1` prints `v10_9`; `sort -V` prints `v10_14` |
| ADJ-09l (`decisions` table frozen second home) | **Confirmed**, medium | Agrees with ADJ2-D (OQ-5 open) |
| ADJ-10 (facts with more than one home) | **Confirmed** | Merged into ORGANISATION (1) below |

**What this pass adds that the first pass lacks:**
- The exact tier-system §5 text (A).
- Co-2 (B).
- CLAUDE.md L270 "base is not a stage" (C9 #1).
- Stored `not_applicable` (C9 #3).
- The CLAUDE.md §4 qualitative exception (C5).
- "never bare axis codes" (C9 #4).
- T1 "occasionally grey" (C9 #5).
- `/orient` L25 (C4).
- F1–F9.
- The tag resolution table (D).
- The delegation audit (E).
- The extractor spot-checks.

**C8 additions:**
- Q16: "Population Mode's table says 'median as default'. Since 2026-11-14 you have said the guidebook shows four figures and showcases the most accommodating value. Is the median still the default shown for Population Mode?" (First pass ADJ-03 (b). No: one note in mission and evidence-architecture. Yes: T-059 needs a rule for when the median is shown over the best.)
- Q17: "Does 'Universal design is co-extensive with code compliance' still hold now that 'universal' means whom a value is for (OD-48)?" (First pass ADJ-09c.)

**Approval-list additions** (insert by size):
- CLAUDE.md L467 `sort -V` (ADJ-09k).
- decision-protocol L5 version pins (ADJ-09d).
- CLAUDE.md §8 sign-off pointer (ADJ-09i).
- CLAUDE.md §6 T3 gloss (ADJ-09j).
- mission L99 type list pointer (ADJ-09h).
- workplan-co0007 pointer fixes (ADJ-09e).
- Rule 9 enforcement sentence (ADJ-06).
- Owner: settings.json deny names (ADJ-06).
- evidence-architecture hand-typed counts (ADJ-09f).
- decision-protocol §0 note on the frozen `decisions` table (ADJ-09l).

---

## ORGANISATION — structural consequences of the resolutions above

Each line names the conflict that requires it. Nothing here goes beyond those conflicts.

**(1) One home per kind of fact**

| Fact | One home | Others point instead | From |
|---|---|---|---|
| Owner rulings and their status | `references/project-standards.md` (status lines and the gate convention) | CLAUDE.md, the DR and `/orient` say "newest ledger entries", not a file name for the plan | C4 |
| Marker table and tier definitions | `governance/tier-system.md` §5 / §1; code: `band()` | CLAUDE.md §6, mission L136, evidence-architecture L187, evidence-auditor skill, owner-browser.yaml: pointer sentences | A, B |
| Synthesis model floor | DR-2026-06-10 with the ledger's 2026-07-25; restated once in decision-protocol §4.2 | CLAUDE.md §6 and the contract name the floor and point there | F4 |
| Stage list | contract `stages:` (CLAUDE.md SPINE is its checked rendering) | Table→stage: `stage-map.yaml`. CLAUDE.md L270 states no stage claim | F9, C9 #1 |
| Cell states | the `specifications.state` CHECK | CLAUDE.md §6 and mission point | C9 #3 |
| Order of authority | one sentence in CLAUDE.md | DR §A and §8 carry the history line | C4 |
| What to do now | derived (`/orient`, the newest ledger entry) | CLAUDE.md §9 row and DR §3 point | C4 |

**(2) Read order for a fresh session**
1. CLAUDE.md.
2. `/orient` (live state).
3. The newest entries of `references/project-standards.md` (they name the active plan; read OD states by the gate).
4. The doctrine file the task touches (tier-system, mission, evidence-architecture, evidence-methodology).
5. The active plan.
6. DR-2026-08-19 only for §1.4, §6, §7 and §12.0 as amended.

Statements in the wrong file for that order:
- CLAUDE.md §6's marker copy (doctrine).
- CLAUDE.md §9 "What to do now" and `/orient` item 1 (volatile, and wrong).
- DR §8's "four documents" (history).

**(3) Broken or stale pointers (verified)**
- `CLAUDE.md:538` and `.claude/commands/orient.md:25`: DR as "what to do now".
- DR §8 L568-576: two spent workplans.
- `governance/tier-system.md` §5, §6, §7: `skills/guidebook-auditor_SKILL.md` (missing).
- Ledger 2026-08-22: `governance/pipeline-map.yaml` (now `_archived/`; history, no edit).
- Ledger 2026-04-19: `scripts/validate_bpc.py` (missing; history).
- `pipeline-contract.yaml` L3-7: OD-17 pending (answered).
- Contract L395: "has NO task" (resolved by F2 if approved).

**(4) History-only documents, one dated line each (annotation, not rewrite)**
- `governance/functional-taxonomy.md`: as to Layer 1 (C1).
- `governance/conceptual-model.md`: as to ENT-08 (C2).
- DR-2026-08-19: §A, §3, §8, §9 (C4 (d)).

**Approval list, smallest change first** (each is one edit, apply nothing until approved):
1. CLAUDE.md L378 "bare axis codes" (C9 #4).
2. CLAUDE.md L381 synthesis floor (F4).
3. CLAUDE.md L270 base convention (C9 #1).
4. CLAUDE.md L372 marker pointer (A).
5. CLAUDE.md L373 cell states (C9 #3).
6. CLAUDE.md L294 qualitative exception (C5).
7. CLAUDE.md L538 and orient.md L25 (C4 (b), (c)).
8. CLAUDE.md L21-23 order of authority (C4 (a)).
9. Contract header (F1).
10. Contract L281 and pipeline-operations L57 (F4).
11. Contract doctrine-recheck criterion (F5).
12. Contract register-invariants clause (F7).
13. Contract three anchors and notes deleted (F2).
14. mission L93 and tier-system L18 Co-2; decision-protocol L77 (B).
15. Ledger entry for Co-2 (B).
16. mission L136 and L118 (A, C9 #3).
17. tier-system §5 and §8 (A).
18. evidence-architecture, owner-browser and evidence-auditor pointers (A).
19. conceptual-model line (C2).
20. DR history line (C4 (d)).
21. functional-taxonomy line (C1, owner merge).
22. mission L40 (C3).
23. tier-system L15 grey at T1 (C9 #5).
