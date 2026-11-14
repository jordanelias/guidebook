# Independent review of the second delegated pass, OD-40 to OD-55 (condition (d))

_Written 2026-11-13 (UTC) by a second, independent Opus-class instance, under condition (d) of the owner's delegation of 2026-11-12 (`grep -n -F "I guess opus can do it" references/project-standards.md`). This is a review, not a resolution, and not the owner's words. It attacks and does not repair: nothing in the ledger, `DELEGATED-RESOLUTIONS-2.md`, `OWNER-SHEET-PLAIN.md`, the plan, the task files, `DECISION-CLOSURE.md`, the scripts or the canonical database was changed. I did not read the resolving instance's scratch files. Every database probe ran on a scratch copy (`cp data/guidebook.db <scratch>/g.db`, opened `mode=ro`), deleted afterwards. "PS:n" is a line of `references/project-standards.md`; re-find each by its quoted phrase. Every count is a command and what it printed._

`sha256sum data/guidebook.db` during this review: `3c575c89c1a6af4b9d2192e9eb43ed78bfeb366d7b31fe5fe41715c731634cdb` (equal to the value the resolver records). HEAD moved from the resolver's `8b4c4e8b` to `0c24d61e` ("Merge pull request #231"); the database did not move.

## Verdict

The pass is sound in its method and mostly in its substance. Each of the resolved decisions survives the attack on its category; none overrides a standing owner ruling; none is reversed here. Every one needs at least one correction, because of one defect common to them all (C0, below), and five need substantive corrections. Each referral is right. Three of the plain-language questions are unfair to an option or misstate a fact, and must be corrected before the owner sees them.

**C0, a defect common to every resolution: the authority sentence.** Each ledger entry says it is made "under the owner's delegation of 2026-11-12 ("I guess opus can do it")". That delegation named twenty decisions by number (PS:5390, "The set, by the register's own numbering: OD-01, …, OD-30"). None of OD-40 to OD-55 is in it. The grant that does reach them is the owner's twelfth instruction of 2026-11-12, "You have permission to use Opus for judgment if appropriate here" (PS:5866), under its own unratified [ASSUMPTION] of what "appropriate" means (PS:5870), as OD-33 was resolved (PS:5877). The owner's question of 2026-11-13 asks for that to be applied. I verified it in the preserved transcript: a user message at `2026-11-13T23:17:22Z` reads "merge 231 into main.\n\nare you sure you can't resolve these owner decisions using Opus based upon prior rulings, mission/doctrine and project goal?" and a queued message at `2026-11-13T23:17:39Z` reads "I don't know the machinery or code" (`transcripts/harness_5dbc61f3/main.jsonl`). The resolver quotes both correctly. Corrected wording for every entry's first sentence, and for the preamble entry's [ASSUMPTION]: "A resolution by an Opus-class model under the owner's twelfth instruction of 2026-11-12 ("You have permission to use Opus for judgment if appropriate here") and the line its [ASSUMPTION] draws, applied at the owner's question of 2026-11-13, with the conditions (a) to (e) of the delegation of 2026-11-12 applied to it; judged against the owner's three criteria in the order ratified by OI-14." Nothing else changes: the twelfth instruction's line (not the owner's act or words, not licensing, not trajectory or control, not the weighing of groups' harms) and §2.4 of `governance/decision-protocol.md` both admit every resolution confirmed below.

**What the owner must see** (in order of weight):
1. OD-43: the owner's own answers OR-6 and OR-6c (PS:4634, PS:6176) already call a disagreement between any two tiers `divergent`, which the ratified definition does not. The resolution keeps `convergent` to the definition's words (clinical and Co-1), so a cell where two clinical sources agree, or a clinical and a Co-2 source, can never be called convergent, while the same cell in disagreement is called divergent. That asymmetry is the owner's to remove, if they want to; the resolution does not create it.
2. OD-44: the option the owner selected for OR-15 carried the effect "D-5 as written" (`grep -n 'id: OR-15' -A16 governance/owner-browser.yaml`), and D-5 as written picks the second source by a corpus-wide query for the T1 or T2 source with the most findings (`scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md`, D-5 "Material"). That is option A on the plain sheet. The sheet does not say so.
3. OD-49: under the owner's OR-2 ("Branches, and an empty headline when all are conditioned"), typing "new buildings" and "existing buildings" as circumstances may empty the headline of many code-derived cells, because codes condition most of their figures that way. T-091's design must measure it first.
4. OD-53 and the coverage of Deaf and blind people: declining elements and provisions as parameters (a hearing loop is the plain sheet's own example) is consistent with the owner's rulings, but it leaves a provision of presence, which no quantity kind holds (OD-24), with no determination at all. That is a coverage question about OD-24, not about OD-53, and the owner has not been shown it.

## Table

| Decision | Resolver's outcome | My verdict | One-line reason |
|---|---|---|---|
| OD-40 | resolved (a) | confirmed with corrections applied | (a) is right on criterion 1; but a derived row may not carry a source's quote (that row is a claim), and the 2026-09-13 ruling does not make (c) unavailable |
| OD-41 | resolved (a) reformat | confirmed with corrections applied (C0 only) | the owner was shown this exact case in OR-3 and answered "Yes, reformat in place" |
| OD-42 | resolved (b) exact | confirmed with corrections applied | sound; one stated fact is wrong (a foot figure is held, as a condition) |
| OD-43 | resolved, (b) tightened to clinical and Co-1 | confirmed with corrections applied | applies the ratified definition, the least new option; but "same bound" narrows "value or range", "governing" drops T3-clinical, and a cell that cannot converge must not be labelled "queued" |
| OD-44 | referred | referral upheld; sheet corrected | turns on what the owner's own answer covered (the reserved kind of OD-04, OD-28) |
| OD-45 | resolved (c) deferred | confirmed with corrections applied | follows R14 and the operative instrument; the "deferred is okay" quote is about citation mining, and a deferred row still stores `results_found = 0` |
| OD-46 | referred | referral upheld; its reason corrected | §2.4 item 4 says "always"; but the "scope decision" words it cites are the recorder's, not the owner's |
| OD-47 | referred | referral upheld; sheet corrected | decides whom every unnamed code figure is for; the sheet omits that the owner's OD-31 answer already says "only its ICF and access-need lenses" |
| OD-48 | referred | referral upheld | two owner records conflict (G1(a) ratified 2026-07-13; OD-31 of 2026-11-12) and the Design Modes rule itself carries both readings |
| OD-49 | resolved (a1); (b2) | confirmed with corrections applied | survives the DG-NON attack; but the vocabulary must come from instruments' phrases, not from the owner's English examples, and "parent within the level" is unruled |
| OD-50 | resolved (a) any source | confirmed with corrections applied | survives; the 2026-10-09 words are intent, not a ruling, and promotion is irreversible except by retirement |
| OD-51 | referred | referral upheld; sheet corrected | tier definition and Co-1 corpus; the sheet omits that the Co-1 row names "CRPD Art. 4.3 consultation outputs" |
| OD-52 | referred | referral upheld | the definition's "through a building" is the owner's own ruling (OT-2 context) |
| OD-53 | resolved (a), bounded | confirmed with corrections applied | survives; E12 covers axis and method terms only, elements rest on the 2026-08-27 levels and OD-24 (delegated) |
| OD-54 | referred | referral upheld | only the owner can set aside rules 3 and 10; nothing waits on it |
| OD-55 | resolved, conditional on OD-41 | confirmed with corrections applied (C0 only) | not reached while OD-41 stands |

Plain-language questions: OD-44 **corrected** (omits the selected option's effect; the study's date is misdescribed); OD-46 **fair**; OD-47 **corrected** (misdates "at least one", omits OD-31's own words, omits option A's coverage risk); OD-48 **fair** (one addition suggested); OD-51 **corrected** (omits the Co-1 row's "consultation outputs" and the open OR-5b edge); OD-52 **fair**; OD-54 **fair**. All are free of code and of project jargon, except the plain sheet's footer, which is fine for its purpose.

---

## 1. The thirteen facts of the resolver's section 4

| # | Claim | Finding | Evidence |
|---|---|---|---|
| 1 | OD-41 not open on the record | **Confirmed** | `grep -n 'id: OR-3$' -A14 governance/owner-browser.yaml` printed, at line 219, "a unit written 'ratio' where it is 'rise:run ratio'"; `grep -n -F 'OR-3: "Yes, reformat in place"' references/project-standards.md` printed `4618:` |
| 2 | "A conversion from inches is inexact" is false | **Confirmed**, with a correction to the resolver's sub-claim | `grep -n 'id: OR-10' -A12 governance/owner-browser.yaml` printed "Inches and feet convert to millimetres and metres exactly". The sub-claim "No inch or foot figure is held today" is true only of `claim` and `derived` rows: `select extraction_id, ref_id, figure_role, claimed_value, claimed_unit from source_value_extractions where claimed_unit in ('ft','cm')` printed `(44, 'REF-01002', 'condition', '20', 'ft', …)`, and the `cm` finding 220 (REF-00468) quotes "100 cm (39 in.)" |
| 3 | OD-40's "No ruling settles it" leaves out a bearing ruling | **Partly confirmed** | The 2026-09-13 ruling (`grep -n -F 'Derived figures are a weighted average' references/project-standards.md` printed `3180:`) bears, but it rules how a derived figure is *graded*, not that it must be a stored row; see OD-40 |
| 4 | OD-43's options (a) and (b) are looser than the definition | **Confirmed** | `grep -n -F "status 'convergent' requires" scripts/validate_evidence_state.py` printed `371:` (`≥2 evidence axes`); `assess_cell.py` counts `n_axes` over clinical, co1 and co2 (`grep -n -E 'axes_clinical|axes_co1|axes_co2|n_axes =' scripts/assess/assess_cell.py`); the definition at `governance/evidence-methodology.md:245` names clinical and Co-1 |
| 5 | OD-48 omits the owner-ratified G1 | **Confirmed** | `decisions/DR-2026-07-12-evidence-architecture-unification.md` line 3: "ACCEPTED — ratified by owner directive 2026-07-13"; line 24 "T4–6-only determinations are Universal-Mode regulatory determinations"; `grep -n 'design_scale = SCALE_UNIVERSAL' scripts/assess/assess_cell.py` printed `1405:`. The OD-31 prompt (an `AskUserQuestion` in `transcripts/harness_4a95df3b/main.jsonl`, 2026-11-12T20:03Z) reads "And ALL only repeats what design_scale = 'universal' already says" |
| 6 | OD-50's entry reads OR-13 as a restriction | **Partly confirmed** | The register's own wording ("seeded 'From the codes held'") is accurate; the restrictive reading is the adjudication's: `scratchpad/session_2026-11-13-edmonton-checklist-pass/ADJUDICATION.md:43` "The proposal to widen T-072 to every source pulls against OR-13", while the same line says "Whether a non-code source may promote a parameter is not ruled" |
| 7 | OR-14 concerns element pages; "5 is three" rules the tables; `room_items` is gone | **Confirmed** | `grep -n -F '"5 is three."' references/project-standards.md` printed `2419:`; `select name, type from sqlite_master where name like '%room%' or name like '%building%' or name like '%element%'` printed `[('rooms', 'table'), ('sqlite_autoindex_rooms_1', 'index')]` |
| 8 | "A code converges trivially" is the report's reasoning | **Confirmed** | `resolution-report-2026-10-22.md:1007`; `git grep -n -F 'converges trivially' references/project-standards.md` printed nothing |
| 9 | T-087's red-with-waiver route works against R16's design | **Confirmed** | `scripts/audit/research_batch_dod.py` lines 988 to 1013: "neither refuses for want of anything this batch must first do, so the rule does not hold red a batch that did its judging"; "A disposition is per term and corpus-wide, so that costs one call per term once, not one per batch". It is the gate author's design, not an owner ruling |
| 10 | The column comment and the instrument differ | **Confirmed** | the `search_executions` DDL printed `deferred_reason TEXT, -- non-NULL => deliberate no-search for this cell`; `grep -n -F 'is for searches *not run*' decisions/DR-2026-08-19-research-restart-operative-instrument.md` printed `1039:` |
| 11 | The cited Ontario page widens "through a building" | **Confirmed** | the saved page `retrieval-log/session_2026-09-28-research-batch-22-selection/40becb4f9c8fbb81.html`, tags stripped, contains "(3) floor s or walks in a barrier-free path of travel having a slope steeper than 1 in 20 shall be design ed as ramps" once, beside two other uses of the phrase for ramps. Whether "walks" are outdoor is a reading, which the sheet properly calls a suggestion |
| 12 | The generator is not read-only | **Confirmed** | `build_batches.py` line 31 `OUT = W / "REMEDIATION-PLAN.md"`, line 333 `OUT.write_text(...)`, while its docstring says "Reads only; writes REMEDIATION-PLAN.md". I ran it only as a copy whose `OUT` points into my scratch; `git status --short workplan/` afterwards showed only the resolver's two untracked files |
| 13 | OD-48's example is not on `main` | **Confirmed** | `select count(*), sum(retired_at is null) from specifications` printed `(8, 0)` |

The generator copy printed: `decisions 54 blocking ['OD-40', 'OD-41', 'OD-42', 'OD-43', 'OD-44', 'OD-45', 'OD-46', 'OD-48', 'OD-49'] standing ['OD-17', 'OD-47', 'OD-50', 'OD-51', 'OD-52', 'OD-53', 'OD-54', 'OD-55']`, which is the resolver's line.

---

## 2. Per decision

### OD-40 — what a derived figure carries as its quote and locator

**(1) Category.** D-SCHEMA with a D-METH flow-through; not a §2.4 type. Strongest DG-NON case: the verbatim floor is the project's defence against fabricated citations (`CLAUDE.md` §5 (c)), which makes any exemption from it a methodology decision. It fails, because (a) exempts nothing: it stores no text that a check would have to pass. **Survives.**

**(2) Rulings.** The 2026-08-24 rule-5 ruling ("It is better to have a table cell point to another table cell than to rewrite", PS:876, `CLAUDE.md` rule 5) supports (a). **Over-read:** the 2026-09-13 ruling ("Derived figures are a weighted average of their figures", PS:3180) says how a derived figure's band is set. Under (c) a computed figure in a determination's note is still a derived figure and can still be weighted that way, so (c) is disfavoured, not forbidden; condition (e) does not remove it. (c) is rejected on criterion 1 instead: a figure that lives only in prose escapes the arithmetic check (`_refuse_derived_mismatch`) and the edges that carry its inputs' quotes. **Over-read:** "OR-17 (PS:4713) forbids presenting a model's wording as a source's": OR-17 forbids model-generated "phrases/names/aliases" (vocabulary). Applying it to `claim_text` is an analogy, sound in spirit, to be cited as one.

**(3) Facts.** `select count(*) from source_value_extractions where figure_role='derived'` printed `(0,)`. `grep -n -F 'KNOWN DEFECT, recorded by T' scripts/db.py` printed `10511:`; its three blockers are as stated. `PRAGMA table_info(source_value_extractions)` shows `claim_text` and `source_section` nullable and `ref_id` NOT NULL. `grep -n -F 'never read off the source' scripts/migrations/075_extraction_relations.sql` printed `66:--   derived    -- computed from other rows this project holds, never read off the source`.

**A defect in the resolution text.** "A derived row that a source does state in words may carry that quote, checked like any other" contradicts migration 075's definition: a figure a source states is read off the source, so it is a `claim` row (which may carry a relation to the inputs it agrees with), never a `derived` one. Keeping the clause would let one figure be both, which is the dual home rule 5 forbids.

**(4) Criteria.** (a) is best on criterion 1 (no unverified text stored), criterion 2 (a reader sees the sources' own sentences) and is neutral on 3. (b) puts an analyst's sentence in the column that means "the source's words". For the book: under (a) a derived clear width shows the two sentences it was computed from, so a disabled reader can check both.

**(5) Reversal and irreversibility.** Reversal condition right. Nothing irreversible: no schema change; derived rows written later retire in place. **For T-063's design, not the resolution:** the derived row's own `ref_id` is NOT NULL, so a figure derived from two sources names one of them; T-063 must say that this `ref_id` is a pointer to the base input (as `root_ref_id` already is) and not an attribution of the derived figure to that source, or refuse inputs from two sources until it does.

**(6) Opens.** T-063 (generator: `OD-40 | CLOSED (no status line) | T-063`). Task-file edits in §4.

**Verdict: confirmed with corrections applied.** Ledger-ready text, replacing the resolver's OD-40 entry:

```
OD-40: a derived figure has no quote or locator of its own; both are its inputs'

**The resolution.** A derived row stores no quote and no locator; its words and its place are its two inputs', reached through its two `derived_from` edges, each carrying its input's verified quote. The writer refuses a derived row whose inputs lack a quote or a locator, and still checks the arithmetic. A figure that a source states in words is a claim row, never a derived one.

**What decided it.** Criterion 1: every stored quote stays a source's own bytes, so no row is exempt from the verbatim check; an analyst's sentence in the column that means "the source's words" is the shape of the fabricated-citation failure (`CLAUDE.md` §5 (c)). The owner's 2026-08-24 ruling ("It is better to have a table cell point to another table cell than to rewrite") favours the pointer. Deleting the verb (option (c)) was rejected on criterion 1, not as overriding a ruling: a computed figure kept only in prose escapes the arithmetic check and its inputs' quotes; the owner's 2026-09-13 ruling ("Derived figures are a weighted average of their figures") says how such a figure is graded wherever it lives.

**Reversal condition.** A derived figure must be shown with a sentence of its own that no input supplies, or the owner wants computed figures kept only in prose.
```

### OD-41 — `ratio` to `rise:run ratio`

**(1) Category.** Application of OR-3; not §2.4. Strongest DG-NON case: under the 2026-11-12 delegation, "what the owner's own earlier answer covered" is reserved (OD-04, OD-28). It fails here because no reading is needed: the OR-3 prompt's context names this exact case (fact 1). **Survives.**

**(2) Rulings.** Followed exactly. D-0168 is narrowed by OR-3 for reformatting (PS:4632).

**(3) Facts.** `select group_concat(extraction_id) from source_value_extractions where claimed_unit='ratio'` printed `('52,53,54,57,58,60,61,62,64,65,66',)`. Their quotes write the figure `1:n` (e.g. 58: "Ramp with gradient of or less than 1:12"). The per-row condition "and the stored figure reads under it" (the T-061 branch) keeps the reversal case reachable: a source that defines its ratio over sloped length is refused and becomes a new reading.

**(4) Criteria.** (a) best on 1 (one statement, one row; old unit kept in notes) and 2; 3 neutral. (b) would create a second live row the engine must not double-count.

**(5)** Reversal right; an amendment is an UPDATE in a data migration, reversible by a compensating amendment. **(6)** Opens T-093 then T-086.

**Verdict: confirmed with corrections applied (C0 only).** The resolver's entry text stands with C0's authority sentence.

### OD-42 — a figure moved between metric units

**(1) Category.** D-PRES with a D-METH effect; not §2.4. Strongest DG-NON case: it changes published values. It fails: exact display publishes the source's own digits; the rounding it declines would publish digits no source stated. **Survives.**

**(2) Rulings.** OR-10's prompt is about "exact length units (inches and feet to millimetres and metres)", and the owner's answer, "Round to nearest 1/4" or 5mm" (PS:4667), answers that question. OD-22 (delegated, check not required) is refined, not overridden. The register's premise that the inch conversion is inexact is false (fact 2), so the real line is a change of system against a change of prefix, as the resolver says.

**(3) Facts.** `select claimed_unit, count(*) from source_value_extractions where figure_role in ('claim','derived') and claimed_unit in ('cm','m','mm','in','ft','inches','feet') group by 1` printed `[('cm', 3), ('m', 33), ('mm', 32)]`. Without the role filter a `ft` row appears (fact 2).

**(4) Criteria.** (b) best on 1; 2 unaffected (1222 mm is legible); 3 safe (exact is never below the source's minimum).

**(5)** Reversal right; nothing irreversible (a display rule in the converter). **(6)** Opens T-030, and through it T-033 and T-110.

**Verdict: confirmed with corrections applied.** C0, and in `DELEGATED-RESOLUTIONS-2.md` §1 OD-42 the sentence "No inch or foot figure is held today" reads: "No inch or foot figure is held as a claim or derived row today; one condition row is stated in feet (extraction 44, REF-01002), and one centimetre finding quotes inches beside it (extraction 220)." The ledger text stands.

### OD-43 — when the engine may call a cell `convergent`

**(1) Category.** D-METH; "convergence assessment rules" is §1.1's own example, and new methodology is DG-NON by default (§2.2), though not in §2.4's always list. Strongest DG-NON case: (i) it sets when the book tells a reader the evidence agrees, and `convergent` "carries higher confidence than either dimension alone" (`evidence-methodology.md:245`), so it moves how strongly the book speaks; (ii) the owner's own OR-6 and OR-6c have already moved the divergence half of the same methodology beyond the written definition (a T1 against a T2 source is `divergent`, PS:4634; "Any different tiers", PS:6176). **It survives, narrowly:** of the options, only the resolution adds no new rule. It brings the engine to the ratified definition's words; options (a) and (b) as registered would extend `convergent` to clinical-and-Co-2 cells, which would be the new methodology. The OR-6 asymmetry predates it and is put to the owner (Verdict, item 1), not decided here.

**(2) Rulings.** Definition (`evidence-methodology.md:245`), rendered sentence Co-1-C (line 284), H1, OR-6b (PS:4661, PS:4690) are quoted accurately. **Narrowed:** the definition says the axes "agree on the parameter value or range"; the resolution says they "state the same bound". Two sources stating the same range (900 to 1000) agree on a range without a single bound; the resolution's words would exclude that case for no reason in the definition. **Over-tightened:** "the governing figures include its clinical axis" drops T3-clinical evidence, which the definition counts ("Tier 1–3 clinical") and the engine counts on the clinical axis (`axes_clinical = … anchors + t3c`, `assess_cell.py` near line 1296) while listing it as supporting, not governing. The engine's prior "(c) would partly undo the computed ruling" is weaker than stated: OD-07 (delegated) is the record that keeps convergence computed by the engine (PS:5492, ACTION (3)).

**A defect the resolution leaves.** Under it a two-axis cell with no Co-1 evidence (clinical and Co-2) is `pending_assessment` permanently. G8 renders that status with the disclosure that value-level convergence "is queued, never assumed" (`evidence-methodology.md` §3.4). For such a cell that is false: the assessment has been made and the definition cannot be met. The engine's rationale, and the disclosure render reads, must state the actual reason.

**(3) Facts.** `grep -n -F 'exists for grading agreement between extracted values' scripts/assess/assess_cell.py` printed `1337:`. Fact 4 above.

**(4) Criteria.** On 1, the resolution is best: the book never prints "Tier 1 OT evidence … and Co-1 sources … converge" over a cell with no Co-1 source. On 3 it keeps Co-1 as a named half of convergence (co-primary, CRPD Art 4.3). On 2 it costs something: a reader of a clinical-and-Co-2 cell is told nothing about whether its sources agree. The value note's spread (OR-6b) partly answers that.

**(5)** Reversal right. An engine `RULE_VERSION` change; determinations re-derive; nothing irreversible. **(6)** Opens T-068.

**Verdict: confirmed with corrections applied.** Ledger-ready text, replacing the resolver's OD-43 entry body:

```
OD-43: convergent only when Tier 1 to 3 clinical evidence and Co-1 evidence agree on the parameter's value or range, their anchoring claims can all hold, and the governing figures rest on two or more independent roots

**The resolution.** The engine writes `convergent` only when the cell has evidence on its clinical axis (Tier 1 to 3 clinical, as the engine counts it) and on its Co-1 axis, the two state the same value or the same range on the parameter's scale, the anchoring claims can all hold, and the governing figures rest on two or more independent roots. Otherwise the cell is `pending_assessment` (two or more axes) or `single_axis` (one), and its rationale states why in words that are true of it: no Co-1 evidence, or floors that differ but can all be met (the spread in the value note), or values not yet compared; never "queued" for a cell whose evidence cannot meet the definition. A clinical and Co-2 cell is never `convergent`. The validator checks the same conditions.

**What decided it.** It applies the ratified definition ("Tier 1–3 clinical evidence and Co-1 evidence agree on the parameter value or range", `governance/evidence-methodology.md`) and its rendered sentence, which names Co-1 sources; H1 (roots, not documents); OR-6b (differing floors that can all be met are not divergent, which is not agreement). Criterion 1: the book says the evidence agrees only when it does. The looser options would extend the definition, which is new methodology and the owner's.

**Reversal condition.** The owner extends `convergent` to agreement between any two tiers (as OR-6 and OR-6c extended `divergent`), or to agreement within a stated tolerance.
```

### OD-44 — the second source for the blind double extraction (referred)

**Referral upheld.** It turns on what the owner's own earlier answer covered, the kind the 2026-11-12 delegation reserved (OD-04, OD-28, PS:5392), and T-070 needs the owner to launch the raters anyway, so the referral costs no time.

**But the referral's reason omits a fact that favours option A.** The selected option's effect was "D-5 as written" (`grep -n 'id: OR-15' -A16 governance/owner-browser.yaml`, line 620), and D-5 as written chooses its material "by query, not by hand", including "(b) The T1 or T2 source with the most `finding` rows", corpus-wide (`resolution-report-2026-10-22.md` lines 1003 to 1007). So of the three things the owner was shown (the label "batch 23's material", the description "one T1 paper with findings", the effect "D-5 as written"), two point to A and only the label, resting on the false premise, points away. The resolver's statement "Option (a) keeps the T1 test and departs from the owner's 'batch 23's material'" is true but incomplete.

**Facts.** `select tier, evidence_type, count(*) from evidence_sources where created_by_session='session_2026-10-01-research-batch-23' group by 1,2` printed `[(3, 'grey', 3), (5, 'national_fw', 3), (6, 'code', 8)]`. The corpus-wide T1/T2 query printed `('REF-01033', 1, 'clinical', 'session_2026-10-30-ramp-spec-pages-rebuild', 3)` tied with `('REF-01034', …, 3)`; `select ref_id, pub_title, pub_year from evidence_sources where ref_id='REF-01033'` printed "Biomechanics and Physiology for Propelling Wheelchair Uphill Slope", 2015.

**Plain-language question: corrected.** (i) Add to "The situation": "The option you chose also said to run the test 'as written' in the plan, and the plan picks the research study by a search of the whole collection, not of batch 23. So option A is what that part of your answer already says." (ii) Option A: "a ramp study from late October" misdescribes it: the study is from 2015 and was added to the collection in late October; and it is tied with another ramp study on findings, so say "one of the two research studies with the most findings (a 2015 wheelchair ramp study; the tie is broken by the project's own order)". The recommendation is then supported.

### OD-45 — a logged search whose request never returned results

**(1) Category.** Application of R14 and the operative instrument; not §2.4. Strongest DG-NON case: it decides what the book may say about absence of evidence. It fails because (c) applies the owner's rules rather than changing them; (b) would be the change (a fourth cause in a findings channel). **Survives.**

**(2) Rulings.** R14 (`governance/research-contract.yaml` line 280) and the instrument (DR line 1039) quoted correctly. **Over-read:** "deferred is okay so long as it runs eventually" (PS:3737) was said of citation mining's deferral (`citation_mining_status`), not of searches; cite it as the same principle by analogy.

**(3) Facts.** T-080's query printed `(13, 0, 1, 12)`; rows 87, 133, 138 and 191 describe requests that returned no list. Row 81 calls itself "an R14 query-shape failure of a kind R14 does not name"; T-081 must judge it on its own words. **A point the resolution leaves out:** `results_found` is NOT NULL (`PRAGMA table_info(search_executions)` printed `('results_found', 'INTEGER', 1)`), so a deferred row still stores `0`, as the one existing deferral does. Every reader that counts zero-yield searches must exclude `deferred_reason IS NOT NULL` first, or a search not run reads as a null result; T-080 names those readers.

**(4) Criteria.** (c) best on all three; for coverage, blocks fall on non-English national sources, which stay owed. **(5)** Reversal right; T-081's re-classification is UPDATEs, reversible by compensation. **(6)** Opens T-080; T-081 also waits on OI-55 (1).

**Verdict: confirmed with corrections applied.** C0; in "What decided it" replace "the owner's 'deferred is okay so long as it runs eventually' (2026-09-18)" with "the principle of the owner's 2026-09-18 ruling on deferred citation mining ('deferred is okay so long as it runs eventually'), applied by analogy"; and add to the ACTION: "(4) Read a zero-result search as a finding only where `deferred_reason` is NULL."

### OD-46 — `lang_jur_map` codes outside the registry (referred)

**Referral upheld.** §2.4 item 4 says "always"; §2.3's downgrade for a decision that "merely operationalises a prior decision" does not lift an always-DG-NON type. Option A would also write registry rows that cannot be dropped. The owner's cost is one line.

**But its reason misattributes.** "The owner ruling of 2026-09-18 says of these very codes that 'admitting a code silently converts a candidate jurisdiction into a declared one, and that is a scope decision'" (PS:3714): the owner's words in that entry are only "UK is canonical, add BE HR INT ES IT to the enum" (PS:3687); the sentence quoted, and ACTION (3), are the recording session's. Corrected referral reason: "Inclusion or exclusion of jurisdictions is always DG-NON (§2.4 item 4); the recorder of the owner's 2026-09-18 enum ruling also noted that admitting a map-only code is a scope decision." The resolver's recommendation (A) is well supported: the registry already holds countries outside the OD-04 set (`select group_concat(jurisdiction_code) from base_jurisdictions` printed a list including BD, BR, EG, IN, KE, NG, UG, ZA), so membership is not coverage.

**Facts.** `select count(distinct l.jurisdiction), count(*) from lang_jur_map l left join base_jurisdictions b on b.jurisdiction_code=l.jurisdiction where b.jurisdiction_code is null` printed `(17, 19)`; the codes and languages match the resolver's list; `select scope_status, count(*) from lang_jur_map group by 1` printed `[(None, 70)]`. The registry has no scope column (`PRAGMA table_info(base_jurisdictions)`: `jurisdiction_code, kind, parent_code, admission_ref, created_at, created_by_session`), so "scoped out" is marked on the pairs.

**Plain-language question: fair.** Accurate, neutral, one line to answer.

### OD-47 — the lens of a figure whose clause names no one (referred)

**Referral upheld.** It decides, for most code figures at once, which people a figure is said to serve; the population taxonomy is the owner's (§2.4 item 2; the fourteenth statement, PS:5935, "The population taxonomy remains the owner's"). Option A also puts a property on the parameter that holds for every figure, a schema choice that would be hard to reverse.

**What the referral and the sheet omit.** The owner's OD-31 answer (PS:6044) already says that a provision under a general disability heading carries "no identity, only its ICF and access-need lenses". Where a clause names no function, those lenses can only come from what the measurement is for, so A is the natural reading of the owner's own words for that case. The block today is the lens writer's warrant rule (`grep -n 'def _require_lens_warrant' -A30 scripts/db.py`), which is code, not an owner ruling.

**Facts.** `select basis, count(*) from v_live_lens_links where identity_code='ALL' group by 1` printed `[('carried', 34)]`; `select (icf_code is not null),(needs_code is not null),(identity_code is not null),count(*) from v_live_lens_links group by 1,2,3` printed `[(0, 0, 1, 212), (0, 1, 0, 3), (1, 0, 0, 1)]`.

**Plain-language question: corrected.** (i) "You ruled on 12 November that such a provision is not to be filed as 'for everyone', and every figure has to be tied to at least one group, activity or need": the second half is the ruling of 1 September (D-0182). (ii) Add: "Your 12 November answer also said that a provision under a general disability heading carries only activity and need links. Option A is how those links would be found when the sentence names no activity." (iii) Option A's "What it means" must state its risk: "The project decides, once per measurement, every activity it serves. If it lists too few, a group whose need the measurement also serves (a corridor width also serves people who are blind and use a cane or a guide dog, and people who need to rest) is left out of every code figure for it." The recommendation is then supported.

### OD-48 — what `design_scale = 'universal'` states (referred)

**Referral upheld.** Two owner records conflict (fact 5), and the ledger's first Design Modes rule itself carries both readings: "Universal Mode = Universal Design / Code Compliance (population-agnostic, fixed values)" (PS:14). Rule 0 would let the later statement win on contact, but OD-31 does not name G1, and its premise was false; treating G1 as superseded by implication is the act the OD-14 correction reserved (PS:5751). The resolver's recommendation (A) is supported by `governance/mission-and-epistemics.md` line 103 ("Neither axis determines the other") and line 107.

**Plain-language question: fair.** One addition I would make for fairness to B: "The July rule's purpose was to stop a value resting only on codes from ever being shown as best practice. Under A that protection is kept by the separate codes-only mark, which already exists." Without it the reader cannot see why B was ever chosen.

### OD-49 — building type, circumstances, and elements

**(1) Category.** The strongest DG-NON case: the register calls it "jurisdiction and scope vocabulary", and `CLAUDE.md` §8 reserves "jurisdiction"; building types decide which buildings the book speaks about. It fails: no option includes or excludes a building type from the book, and building use is a circumstance of a figure, not a jurisdiction. The determination key, the one doctrinal thing at stake, is left as ruled. Vocabulary approval in bulk with the owner reading the pull request is the owner's own OR-17. **Survives.**

**(2) Rulings.** The three-level ruling (PS:2053: "Building types (eg residential, commercial), room types (eg kitchen, entry, bathroom), construction elements (eg door, door handle, window, floor) are what I wanted for that table"), "5 is three" (PS:2419), the key (2026-08-26, 2026-08-28), one value per cell (`CLAUDE.md` §4, owner 2026-11-06), OR-2 (PS:4616): read correctly; (a2), (a3) and (b1) are correctly found unavailable. **Two over-reaches.** (i) "seeded from the owner's two examples": the owner's words are examples ("eg"), and OR-17 ("Ensure that these phrases/names/aliases are all present in their prescribed jurisdiction/language. It is not acceptable for the model to generate its own phrases/names/aliases", PS:4713) and E1 (a concept first met outside English is named by the instrument's own phrase) require each building type to be minted from an instrument's own scope phrase, in its language. Seeding English labels from the owner's examples would mint names no instrument used, the English bias the 2026-11-06 rulings forbid. (ii) (b2)'s "and its parent within the level" is unruled: the recorded analysis of "5 is three" says the levels do not nest and cross-level edges are junctions (PS:2436 onwards); a parent inside the element level is a new design for T-060 to justify, not part of this resolution. The appeal to OD-01 as a pattern is to a delegated resolution, not an owner ruling; it is consistency, not authority.

**(3) Facts.** `select count(*), count(distinct setting), sum(setting is not null) from source_value_extractions` printed `(214, 76, 125)`; parameter 9's `setting` values join building age, approach and route width (`'new buildings; right angles to an access route at least 1500 mm wide'`); `grep -n 'setting' scripts/assess/assess_cell.py` finds no reader. Fact 7.

**(4) Criteria.** (a1) is best on 1 (figures for dwellings and public buildings no longer compose into one headline) and on 2 (a designer reads the branch for their building). **Its legibility risk:** under OR-2 a cell whose every figure is conditioned has an empty headline, and codes condition most figures on new or existing work; typing that circumstance may empty many headlines. T-091 must measure, on a scratch copy, how many cells' headlines empty under (a1) before T-092 re-tags, and whether a circumstance carried alike by every figure of a cell makes a branch at all.

**(5) Irreversibility, not stated by the resolver.** T-091 adds typed columns and a building-type table, and T-092 writes their values in data migrations; "A column a committed data migration INSERTs can never be dropped" (`CLAUDE.md` rule 5), and vocabulary rows only retire. This is the least reversible of the resolutions, so the reversal condition should say that reversal means retiring rows and NULLing forward.

**(6)** Opens T-091 (its design file still owed) and T-092.

**Verdict: confirmed with corrections applied.** Ledger-ready text, replacing the resolver's OD-49 entry body:

```
OD-49: (a1); (b2)

**The resolution.** (a1) Building type (use), new or existing work, and interior or exterior are each a typed circumstance on the figure, one value per cell, shown as branches within one determination per parameter and lens set. Building type points at the first of the owner's three building levels (2026-08-27). Each building type is minted from an instrument's own scope phrase, in its jurisdiction and language, in a data pull request the owner reads (OR-17, E1); the owner's examples ("eg residential, commercial") show what the level holds, and are not minted as names. "Public" is adjudicated per instrument. Before stored figures are re-tagged, the design measures how many cells' headlines OR-2 would empty and says how a circumstance shared by every figure of a cell is shown. (b2) The owner's 2026-08-27 "three tables" ruling stands; an element row, when a reader needs it, points at its term and holds no name of its own; any relation between elements is decided in that design, not here.

**What decided it.** The other options override standing owner rulings: (a2) the determination key (2026-08-26, 2026-08-28); (a3) one value per cell (2026-11-06) and the building levels (2026-08-27); (b1) "5 is three" (2026-08-27), which OR-14 on element pages does not name. Criterion 1: figures for different building uses no longer compose into one headline; the key is unchanged.

**Reversal condition.** The owner wants building type in the key, or elements as terms only; or the measured headlines show that branching hides a group's difference. Reversal retires the vocabulary rows and NULLs the typed cells forward; nothing written can be dropped.
```

### OD-50 — may a non-code source add a parameter

**(1) Category.** Strongest DG-NON case: what the book's pages ask about, and on whose word, is content, which `CLAUDE.md` §8 reserves. It fails: a parameter is a question, not a finding, and no option includes or excludes a Volume or Part; the owner delegated bulk vocabulary approval with the pull request as the approval (OR-17). And the criteria point the other way strongly: under (b) a disabled people's organisation's document could never add a question the book asks, only a code could, which sits badly with CRPD Art 4.3 and Co-1's co-primary standing. **Survives.**

**(2) Rulings.** OR-13 answered a seeding route (`grep -n 'id: OR-13' -A18 governance/owner-browser.yaml`). **Over-read:** "the owner's own words on the parameter list are 'pull from the major codes, literature and advocacy from major countries'": the ledger records that message as queued before the options arrived, "so that choice was never answered" (PS:4395). It is the owner's stated intent about where the list comes from, not a ruling, and should be cited so. The 2026-10-09 guard for prepopulation ("Screen, then you approve") is replaced for D-8 by OR-17's bulk approval (PS:4713), so the resolution's "the owner reads the pull request" is the standing approval.

**(3) Facts.** `select ref_id from evidence_sources where ref_id='REF-01037'` printed `[]`. `python3 scripts/db.py add-parameter --help` and `decline-parameter --help` take no approval flag; `skills/run-pipeline_SKILL.md` lines 69 to 74 as quoted.

**(4) Criteria.** (a) best on 3 by a wide margin (sensory, cognitive, rest and seating quantities); neutral on 1, since every figure keeps its own tier and marker; on 2, more parameters mean more pages. **(5) Irreversibility, not stated:** a parameter row is written by a data migration and can only be merged or retired; each one makes every held source owe a reading (`v_scan_ledger`). **(6)** No gate; T-087 and T-072 edits in §4.

**Verdict: confirmed with corrections applied.** C0, and in "What decided it" replace "The owner's words of 2026-10-09: 'pull from the major codes, literature and advocacy from major countries'" with "The owner's stated intent of 2026-10-09, never put as a choice: 'pull from the major codes, literature and advocacy from major countries'. Criterion 3 also: under the other options a disabled people's organisation's document could never add a question the book asks." Add to the reversal condition: "Reversal retires the parameters added under it; none is deleted."

### OD-51 — Co-1 standing for a municipal committee (referred)

**Referral upheld** (§2.4 items 3 and 6). **Plain-language question: corrected.** The Co-1 row (`grep -n -F '| **Co-1** |' governance/tier-system.md`, line 16) lists "DPOs, named-org … outputs; CRPD Art. 4.3 consultation outputs". A city's accessibility advisory committee may be such a consultation, so option A's "A committee appointed by a city is not an organisation of disabled people" argues against only half of the row. Add to "The situation": "The book's definition of lived-experience evidence includes both organisations of disabled people and the outputs of the consultations governments must hold with them under the UN Convention. A city advisory committee may be the second kind." And to option B: "Its soundness would still be tested as you ruled for lived-experience evidence; how that test applies to a document that is not a study is one of your open questions (OR-5b)." The recommendation (B) remains supported.

### OD-52 — "barrier-free path of travel" (referred)

**Referral upheld.** "Through a building" is the owner's own words (OT-2 context: "You ruled earlier that it is the entire route through a building", line 1016), approved on 2026-11-13 (PS:6195). Fact 11 confirmed. **Plain-language question: fair.**

### OD-53 — declining held terms in a single-source batch

**(1) Category.** Not §2.4; who records a declination the verb already provides. Strongest DG-NON case: declining an element as a parameter decides that the book will not determine a value for it, which shapes coverage. It fails as a category matter, because declinations are revocable rows reviewed by the owner in the pull request and again by T-072 item 6; but its coverage consequence belongs on the owner's list (Verdict, item 4).

**(2) Rulings.** **Over-read:** E12 (PS:5060) declines "the functional-axis terms and the method terms"; it does not name elements, as the register says. The bound to elements rests instead on the owner's three-level ruling, which places elements in their own level and not among quantities (PS:2053), and on OD-24 (delegated: "A parameter need not belong to an element"). The R16 design comment is the gate author's, not the owner's; it is good evidence of intent, not authority.

**(3) Facts.** `select count(*), sum(<neither parameter nor live declination>) from terms` printed `(94, 83)`; `revoke-declination` exists (`python3 scripts/db.py revoke-declination --help`) and takes `--decision-ref`.

**(4) Criteria.** (a), bounded, best on 1 (reasoned, attributed, revocable acts instead of a gate red by construction) and 2. **On 3:** declining a provision of presence (a hearing loop, a tactile indicator) as "not a quantity" is consistent with OD-24's quantity kinds, and it means no determination will ever be written for it. The resolution is right to bound declination; the gap it exposes is OD-24's.

**(5)** Reversible (revocation). **(6)** No gate; T-087's item 6 must exclude quantities from what it declines (as written it declines "each term the R16 query prints").

**Verdict: confirmed with corrections applied.** C0, and in "What decided it" add after "E12": "(which names functional-axis and method terms); elements are declined because the owner's 2026-08-27 ruling places them in their own building level, not among quantities, and a parameter need not belong to an element (OD-24, delegated)". Add to the ACTION: "(4) Never decline a quantity term; promote it (OD-50) or leave it for T-072."

### OD-54 — writing a canonical row by hand (referred)

**Referral upheld.** Option B sets aside `CLAUDE.md` rules 3 and 10. The eleventh set's [ASSUMPTION] already reads "by hand" as A and acts on nothing else (PS:6270), and no task waits on it, so this question can be asked last. **Plain-language question: fair.**

### OD-55 — conditional on OD-41

**Verdict: confirmed with corrections applied (C0 only).** It follows the owner's "retire in place then" (PS:3540) and is not reached while OD-41 stands.

---

## 3. The status and check lines to append, once the corrections are applied

Under the convention (PS:5724 onwards), the session that records the resolutions appends, after each corrected entry and after the resolver's `CHECK: pending` lines:

```
OD-40 CHECK: confirmed with corrections applied
OD-41 CHECK: confirmed with corrections applied
OD-42 CHECK: confirmed with corrections applied
OD-43 CHECK: confirmed with corrections applied
OD-45 CHECK: confirmed with corrections applied
OD-49 CHECK: confirmed with corrections applied
OD-50 CHECK: confirmed with corrections applied
OD-53 CHECK: confirmed with corrections applied
OD-55 CHECK: confirmed with corrections applied
```

The seven referrals keep `REFERRED BACK TO THE OWNER` and take no check line. The preamble entry's [ASSUMPTION] takes C0's wording. Verify with the convention's `gate` function, once appended: each resolved id should print `OPEN (delegated; confirmed with corrections applied)`.

## 4. Task-file edits the confirmed resolutions need

**How the generator reads them** (`scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`, `bullet()`, the task loop, `closed()`): every `OD-\d+` anywhere in the "Owner decisions" bullet is treated as needing the owner's words, unless the bullet's text starts with "none"; a delegated decision is read only from the "Delegated resolutions" bullet's `for n in …;` loop, and an id in both is read as the owner's (`dels - ods`). So each edit must **remove the id from the "Owner decisions" bullet entirely** (or start that bullet with "none"), not merely annotate it, and **add it to the loop**. No task opens until the ledger lines of §3 exist. Run the generator only as a copy whose `OUT` points outside the tree.

- **T-063.** §2 "Owner decisions": "none". New "Delegated resolutions this task rests on" bullet: OD-40 as corrected, with the convention's `gate` and `for n in OD-40; do gate $n; done`. The banner at line 3 ("HELD on an owner question"): remove. §4 item 3: build the (a) branch only; delete the (b) sub-bullet and the (c) paragraph; settle the derived row's `ref_id` (OD-40 §5 above).
- **T-093.** §2 "Owner decisions": "none"; delegated bullet with `for n in OD-41;`. The "Only under answer (a)" text: built.
- **T-086.** §2 "Owner decisions": "none"; delegated bullet with `for n in OD-41;`. §4 item 2 (second rows): delete. The OQ-T086/OD-55 bullet: "not reached under OD-41 as resolved".
- **T-061.** §4 "Not built here": point at T-093.
- **T-030.** §2 line 23 "Owner decisions": "none"; line 27 loop: `for n in OD-22 OD-24 OD-42; do gate $n; done`, and line 24 names OD-42. §4 item 1: a metric prefix change is shown exactly; a change of measurement system is rounded to the safe side.
- **T-068.** §2 "Owner decisions": "none"; delegated bullet with `for n in OD-43;`; delete "until a ledger line in the owner's words answers it, do not start" and line 153 ("Do not start while Q-T068 has no answer in the owner's words"). §4 item 3: the four conditions of OD-43 as corrected (clinical axis as the engine counts it, Co-1 axis, same value or range, satisfiable, two or more roots) and the truthful rationale; item 2 (validator): the same.
- **T-080.** §2 "Owner decisions": "none"; delegated bullet with `for n in OD-45;`; remove the line-3 banner and line 129 ("in the owner's words"). §4: the refusal is option (c)'s; name the readers of zero-yield searches that must exclude `deferred_reason IS NOT NULL`; align the column comment's "deliberate".
- **T-081.** §2 "Owner decisions": start with "none in the register"; keep OI-55 (1) as prose with no OD id; delegated bullet with `for n in OD-45;`; line 110: "the delegated resolution is confirmed" in place of "the owner's answer is in the ledger". §4: the rows that returned no result list are deferrals owed a re-run; row 81 judged on its words.
- **T-091.** §2 "Owner decisions": "none"; delegated bullet with `for n in OD-49;`. The design file (still owed) states OD-49 as corrected, including the headline measurement and minting building types from instruments' phrases.
- **T-092.** §2 "Owner decisions": "none"; delegated bullet with `for n in OD-49;`; delete the "(a3) declined" sentence.
- **T-060** (design only): elements as in (b2), without an unruled within-level parent.
- **T-087** (no gate): §2 "Owner decisions" and the next bullet: OD-50 and OD-53 resolved under delegation, read through the gate. §4 item 3 (ii): a quantity concept the checklist states may be minted and promoted in the batch. §4 item 6: decline only the R16 terms that are elements, lens terms or methods, one reason each; promote or leave the quantities. Line 141 and the stop list: drop "Do not mint, promote or … decline" for those cases. §6 "Expected after" and §11's waiver: the waiver covers only terms left undisposed. OD-47, OD-51 and OD-52 parts stay as they are.
- **T-072.** Line 24: name OD-50 and OD-53; item 6 reviews batch declinations.
- **Plan and register.** `REMEDIATION-WORKPLAN.md` §5 rows and §8 status lines for each resolved id ("RESOLVED UNDER DELEGATION 2026-11-13, check confirmed with corrections applied"); the batch-1 line ("T-093 … built only under its answer (a)"); `DECISION-CLOSURE.md` §4 prompts 2, 3, 4, 5, 7, 11, 12, 15 and 17 marked resolved under delegation with the ledger pointer. `DECISION-CLOSURE.md` §4 and `REMEDIATION-WORKPLAN.md` §8 should stop telling a reader to run the generator in the tree (fact 12).
- **The plain sheet** (`OWNER-SHEET-PLAIN.md`): the corrections to questions 1, 3 and 5 above, and the OD-48 addition, before the owner sees it.
