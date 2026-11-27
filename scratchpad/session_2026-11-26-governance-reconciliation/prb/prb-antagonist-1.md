# PR B part 1 — antagonist pass (blind-then-compare)

Repository HEAD at time of reading: ee815a82. Canonical DB sha256 3d419efb94b7d5c8a1297ba9552bdee64228007e38da95af612e5406bb68edb9 (unchanged; all probes ran on a scratch copy `scratchpad/ant1/g.db`). Schema user_version 167.

## PHASE 1: my independent specification

Written before opening `prb-design-1.md`.

### (a) The ruled marker rule

Ledger lines are `references/project-standards.md` at HEAD.

| Basis of the showcased value | Glyph | Owner's words (line) |
|---|---|---|
| T1, T2 | ● | "full for tier 1/2?" (proposal, 6944); applied by "od57 yes" (7315, gate 7327-7328) |
| Co-1, Co-2 | ● | "Co-1 stays full, Co-2 full too" (6989; quoted in U7, 7876) |
| T3 clinical | ◐ | "half for tier 3/4" (6944); OD-57 registration names "lowering T3 clinical from ● to ◐" (7265), answered yes (7327) |
| T3 grey | ⚠ (never ◐) | "2 triangle for all" (7401), gate "OD-64: triangle for every grey basis" (7424-7425), ACTION (3) 7434 |
| T4 | ◐ | "T4 only half circle" (7195); "half for tier 3/4 as 4 is above jurisdiction code" (6944) |
| T5, T6 | ○ | "empty for 5/6" (6973; U7 7876) |
| any tier, source grey | ⚠ in place of the circle | "no, triangle instead if the value is coming from grey or unverified" (7053) |
| any tier, source unverified | ⚠ in place of the circle | same (7053); glyph U+26A0 without U+FE0F: "except use the Unicode one" (7039-7044) |
| any tier, basis thin | ⚠ in place of the circle | "thin too" (7071); thin = "the evidence doesn't directly concern someone but is conjecture" (7087) |
| project inference, or a value mixing a finding with a project inference | ⚠ | 7120-7128 ("we aren't clinicians so it is flagged as thin"); 7159 ("if it mixes then it's a new value proposed ... conjecture") |
| clinician's vetted judgment; derivation by a clinician or academic | not thin (circle of its tier) | 7101-7108; 7141 |
| floor claim confirmed by absence by a verified, retrieved study | the study's band | OR-22b (6183-6184) |
| unretrievable source | anchors only with a valid academic route (OR-23, 4725 and 4758) or, for T4-T6, a registry citation by jurisdiction, standard number and clause (OR-23b, 6186-6187); with a route, its value takes ⚠ (7053); without one it anchors nothing | |

**Explicitly unruled** (tier-system.md §5 "Not yet ruled (owner)", and the ledger's own "does not decide" lines): whether every PROXY population-match grade makes a value thin (7092); how ⚠ enters a derived figure; how vetting and an author's standing are recorded; a single clinician's unvetted opinion; whether a `provisional` cell is thin in the ⚠ sense; what becomes of unretrievable sources already held that have no route (OR-23 reading, 4758: "the ruling does not say what becomes of those already held").

**OD-59 on a several-source cell.** "od59 yes" (7333) answers the registered question (7273): the showcased value carries the grade of *its own source*, not the floor of the mean of all governing sources; ⚠ only where that value's own basis is grey, unverified or thin (reading at 7319). So the cell marker is a function of the **headline value's source(s)**, not of the governing set. The ledger does not say what happens when **several sources state the same headline value** (common: three codes each state 1:20). My reading, flagged [ASSUMPTION]: the value "comes from" each source that states it, so it carries the best circle among the verified, non-grey sources that state it, and ⚠ only when every source stating it is grey or unverified, or the value is thin. The floor-of-the-mean reading is withdrawn for cells by OD-59 (the registration names it as the alternative rejected). `floor_mean` survives only for a derived figure's inputs (owner 2026-09-13; tier-system §5 bullet). This multi-source edge is a genuine gap: it is either delegable as the obvious reading of "its own source" or an owner question; I would put it to the owner as one line and build the reading meanwhile, reversible.

### (b) What the engine does today, and the wrong outputs

Code read: `schemas/tier_derivation.py` `band()`, `floor_mean()`; `schemas/enums.py` `EvidenceMarker` (three members; `ordinal = len(EvidenceMarker) - index`); `scripts/assess/assess_cell.py` `classify`, `determine`, `_confirmed_bands`, `compose_value`; the `specifications` CHECK in `sqlite_master`.

- `band()`: T1, T2, T3-clinical → ●; T4, T5 → ◐; T3-grey, T6 → ○. Wrong against the ruled table on T3 clinical (should be ◐), T3 grey (should be ⚠), T5 (should be ○).
- Marker block of `determine`: `regulatory_stratum_only` → `source_bands = []` → ○ for every T4-T6-only cell (so a T4-only cell is ○; owner: ◐). Proxy branch: each verified governing source takes `_confirmed_bands` (an unconfirmed row is ○ regardless of tier). Otherwise floor of the mean over **verified governing** sources. Unverified sources are left out of the marker (`_verified`), so a value read off an unverified source can carry a circle (owner: ⚠). There is no ⚠ path at all, and the column CHECK refuses ⚠: `marker IN ('●','◐','○') AND (regulatory_stratum_only = 0 OR marker = '○')`.
- The marker is the floor-mean over the governing set, not the headline value's own source: contradicts OD-59.
- **Eligibility by tier.** `determine`'s branches choose the governing set by stratum: if any T1/Co-1(verified)/T2/Co-2 anchor exists, only anchors govern and T3/T4-T6 values cannot be the headline however accommodating; T3 clinical governs only when no anchor exists; **T3 grey alone → `pending` with a gap** (no value shown at all); unverified Co-1 is bucketed out. This is "tier decides eligibility", contrary to U1 ("a source's tier sets the marker and the weight, not whether its value may be the best", 7870) and the harm test (7177-7187).
- **design_scale.** The G1 branch writes `design_scale = 'universal'` whenever the basis is T4-T6 only, and the proxy branch inherits it, even for an identity-keyed cell. Contrary to OD-48 (a) "whom it is for" (7995-7996; adjudication 3 item 4).

Probe on scratch copy, `determine(conn, pid, {identity_code: 'MOB'})`:

| | param 3 × MOB | param 12 × MOB |
|---|---|---|
| state | provisional | provisional |
| design_scale | **universal** (wrong under OD-48 (a): the cell names MOB) | **universal** (same) |
| marker | ○ | ○ |
| tier_basis | T4-6-only-threshold+CO1+T2-direction(proxy_inference) | T4-6-only(regulatory_stratum_only) |
| headline | ≤ 5 % | ≤ 6000 mm |
| has_unverified_sources | 1 | 1 |

Under the ruled table, the 3×MOB headline (5 % = 1:20) is stated by verified T6 codes (REF-00992 1:20, REF-00995 5 %, REF-01018 1:20, REF-01015 1:20, REF-01017 "viisi prosenttia") and verified T5 (REF-01024 1:20, REF-01030 5 % recommended, REF-01021 1:20 under a condition), and by two UNVERIFIED T4 (REF-00994, REF-01014). Its verified sources are T5/T6 → ○. So ○ is what the ruled table gives on my multi-source reading; ⚠ would need either "every stating source unverified" (false) or thin (needs the unruled PROXY question). The 12×MOB headline 6000 mm is REF-00139 (T6, verified) and REF-00988 600 cm (T5, verified) → ○. **The circle is right on both probe cells; design_scale is wrong on both.**

Wrong outputs that would reach the guidebook today on other cells: a T4-only value printed ○ (should be ◐); a T5 value printed ◐ (should be ○); T3 clinical ● (should be ◐); a grey value either suppressed (grey-only cell pending) or, where it governs, ○ (should be ⚠); a value whose own source is unverified printed with the circle of the verified others (should be ⚠); a more accommodating code value hidden behind a research value (tier gating); every T4-T6-based identity cell labelled `universal`.

### (c) C10

Today (`scripts/tests/test_db_integrity.py`, C10): fails if any live `stated`/`provisional` specification has a `governing` row in `specification_source_links` whose source is not `VERIFIED`. Subject: live published cells (today 0: all 8 `specifications` rows are retired, so C10 examines nothing on main).

What the owner's rule implies: unverified sources are **kept** (7005, "let's return to keeping them but they get a triangle warning"), and an unretrievable source **anchors only** with a route (OR-23 "This applies only when the source is properly cited in an academic context, i.e. there is a valid academic route to the source"; OR-23b "Yes, for T4 to T6" registry citation by jurisdiction, standard number and clause). So C10 should be **route-gated**: a published cell may rest on a non-VERIFIED governing source only if (i) T1-T3/Co: a valid academic route is recorded (reading at 4758: a resolving DOI or index record, or a citing bibliography, i.e. `verification_method IN ('corroborated-not-retrieved','citing-bibliography')` or a DOI/PMID; [ASSUMPTION], the reading is the recorder's), or (ii) T4-T6: jurisdiction, standard number and a clause locator are recorded. The ⚠ is the *marker* consequence and belongs to the value; it is **not** the permission. "C10 passes when the marker is ⚠" is unsupported: under OD-59 a cell may correctly carry a circle while an unverified source sits in its governing set (the headline comes from a verified source), so a test "circle fails" would be wrong, and "⚠ passes" would admit a routeless source the owner said anchors nothing.

Data fact for the route test: every UNVERIFIED source has `standard_number IS NULL`, but four T4-T6 ones carry the number in `pub_title` (REF-01013 "O. Reg. 163/24, s.3.8.3.4", REF-01014 "ISO/CD 21542", REF-01016 "NZS 4121:2001", REF-01026 "Decreto-Lei n.º 163/2006") and their extraction rows carry the clause (`source_section`, `loc_*`). A route test reading only `standard_number` would drop sources whose registry citation exists in the record in another column: a data-entry gap, not a missing route.

### (d) Smallest change, and migration constraints

1. `band()`: the ruled table, plus a separate `warn` predicate: `⚠` for grey, unverified, or a thin flag the engine already holds (project inference only: `rests_on_proxy_inference` is NOT automatically thin; see "riskiest"). Keep `EvidenceMarker` ordinals for the three circles; add ⚠ as a value that has **no ordinal** (`floor_mean` must refuse it rather than silently renumber: adding a fourth enum member changes `len(EvidenceMarker)` and therefore every ordinal, so FULL becomes 4 and the owner's 2026-09-13 "● 3, ◐ 2, ○ 1" ruling breaks).
2. Marker = own source(s) of the headline (OD-59), replacing the governing-set floor-mean and the `regulatory_stratum_only` override. `_confirmed_bands` may still **raise** a code row to its confirming study's band (OR-22b) but an unconfirmed row takes `band(tier)`, not ○.
3. Selection: every identified value in the lens is a candidate; most accommodating in the recorded direction; tier never filters (grey and T3 included). The harm-test record is the only replacement trigger, and it does not exist (`harm_finding` = 0 on all 214 rows; no relation means "worse at"). The shape is delegated to the task (fourteenth set, 7325: "for the task to design").
4. `design_scale = 'universal'` iff `identity_code IS NULL`; else `population`. Engine only; **no CHECK** (rows 2-8 of `specifications`, retired, are `universal` with `MOB`; a CHECK would refuse them on the rebuild's copy unless it exempts retired rows).
5. Schema: one migration rebuilding `specifications` for the marker CHECK (SQLite cannot alter a column CHECK). Constraints: the rebuild must (i) recreate `idx_spec_row_identity`, `idx_spec_retired`, trigger `trg_spec_retire_needs_reason`, and the seven views naming `specifications` (`v_divergence`, `v_pending`, `v_item_provenance`, `v_source_reach_all`, `v_best_practice`, `v_gap_subject`, `v_determination_provenance`), because RENAME reparses the schema (migration 076 dropped and recreated its views for this reason); (ii) carry `sqlite_sequence` forward by SELECT from the old row, not a literal (076 hard-coded `seq = 2`); (iii) keep the two FK children (`specification_source_links`, `specification_extraction_links`) pointing at the final name (create-new, copy, drop-old, rename-new; never rename-old); (iv) replay order: the last `AFTER_DATA` cutoff is 20261106053823 and every data migration that INSERTs/UPDATEs `specifications` is dated 2026-09, so they replay before the new schema step; the 8 retired rows are copied by the rebuild and must satisfy the new CHECK (their marker is NULL, retired: they do). No AFTER_DATA marker is needed for the marker CHECK alone. Rule 3: migration only; rule 5: no second marker column; reproducibility gate compares counts only, so also run `--deep`.
6. C10 route-gated as in (c).

### (e) Red tests first

- band table: T3 clinical ◐; T3 grey ⚠ (U+26A0 alone, assert no U+FE0F); T4 ◐; T5 ○; T6 ○; Co-1/Co-2 ●.
- `floor_mean` over the three circles reproduces the owner's five rows unchanged after ⚠ exists (guards the ordinal shift).
- Marker of a headline stated by a verified T6 and an unverified T4: ○; stated only by an unverified T4: ⚠; a T4-only cell: ◐ (red: ○, and CHECK refuses ◐ with rso=1).
- CHECK on scratch: ⚠ accepted; ◐ with rso=1 accepted; ⚠ with U+FE0F refused.
- Selection: T6 more accommodating than T1, no record → T6 value stated; grey-only cell → stated/provisional with ⚠ (red: pending).
- design_scale: 3×MOB → `population` (red: `universal`); an ICF-only cell → `universal`.
- C10: a seeded live cell resting on an unverified T6 with jurisdiction, standard number and clause passes; the same with no standard number fails; an unverified T1 with neither DOI nor citing-bibliography fails.

### (f) Riskiest decision

Whether a proxy determination (`rests_on_proxy_inference = 1`) is "thin" and so ⚠. The owner made the project's own inference thin (7120-7128) and a mixed value ⚠ (7159); the engine's proxy branch says "no source states it" in its own rationale, yet the headline it selects is a value codes state. If the proxy branch is read as a project inference, 3×MOB is ⚠; if as a code value selected by U1's most-accommodating rule, ○. Under U1 the most accommodating identified value is the best without any inference, so the "direction" findings no longer select anything; the proxy label is residue of the pre-U1 engine. Deciding ⚠ here, or deciding PROXY population grades → thin, would decide an unruled question. The second riskiest: dropping held unverified sources from the governing set on a missing `standard_number`, which changes what the page prints as governing and touches the held-sources question OR-23 left open.

---

## PHASE 2: comparison with `prb-design-1.md`

Probes for this phase: `scratchpad/ant1/stating.py` (the unconditioned headline rows of a cell and which of them state the selected bound), `scratchpad/ant1/union.py` (every lens cell of every parameter, today's headline against the headline with the rows the union would add), and direct read-only queries. All on the scratch copy or `mode=ro`.

### Where the two specifications agree

The circle table and its line numbers; ⚠ as U+26A0 without U+FE0F; ⚠ kept out of the ordinal so `floor_mean` keeps ● 3, ◐ 2, ○ 1; OD-59 read as the headline value's own source(s), not the governing set; the regulatory-only override deleted; `_confirmed_bands` giving an unconfirmed row its own band instead of ○; C10 route-gated, not "⚠ passes"; T-117 item 4a / T117-07 wrong under OD-59; `design_scale` from the key; no CHECK on `design_scale`; PROXY-as-thin left to the owner; `rests_on_proxy_inference` not treated as thin; no AFTER_DATA marker for the `specifications` rebuild; the 12×MOB glyph ○.

### Where the design adds to my Phase 1 (and is right)

- `stating_refs` returned by `_compose_headline` (the rows whose bound equals the selected bound): the exact mechanism OD-59 needs; I had the rule but not the hook.
- Refusing the cell when several stating sources carry different markers (Q-B2), rather than choosing. That is the conservative choice. But see defect D2: it fires on the target cell.
- The `test_scan_contract.py:1019` 5-tuple caller.
- The T117-02 defect in the task file (a T5-only cell is masked by the override, not red at engine level).

### Comparison table

| # | Claim | Agonist | Antagonist | Verdict | Evidence |
|---|---|---|---|---|---|
| 1a | 12×MOB: ○ is the ruled glyph; ⚠ not derivable | ○ (high) | ○ | **SURVIVES** | `stating.py … 12` prints `STATING (today): [(116, 'REF-00988', 5, 'national_fw', 'VERIFIED', '600', 'cm')]`; 17 of 20 governing rows are conditioned branches, so REF-00139's 6000 mm (row 135) is not a headline row. REF-00988 has no `evidence_population_match` row, so it cannot become thin even if Q3 is answered yes. |
| 1b | 3×MOB: ○ once the route gate drops route-less unverified sources | ○ (medium) | Q-B2 fires; neither ○ nor ⚠ can be derived from ruled text | **WOUNDED** | `stating.py … 3` prints stating rows 25 (REF-00992, T6, VERIFIED), **28 (REF-00994, T4, UNVERIFIED)**, 30 (REF-00995, T6, VERIFIED). The design only gets ○ by dropping REF-00994 through a route gate that does not apply to it (defect D1: the source was retrieved). Correctly scoped, the stating marks are {○, ⚠, ○} and the design's own `set(marks) != {circles[0]}` refuses. Once GAP-371 is resolved and REF-00994 is VERIFIED, the marks become {○, ◐, ○} and it refuses again (Q-B2(b)). The path-finder's "should be ⚠" is also not derivable: the ledger lists this combination as undecided (7059: "How a cell resting on a grey or unverified source together with others is marked"). |
| 1c | "PROXY grades exist on REF-00994 and REF-00995 only" | evidence line | 32 PROXY rows, all target `MOB` | **FALSE as written** (true only within the 3×MOB stating set) | `select match_grade,count(*) from evidence_population_match group by 1` → `PROXY 32`, among them REF-00139, REF-01013, REF-01014, REF-01015, REF-01016, REF-01018, REF-01024, REF-01025, REF-01026, REF-01030 … So Q3 reaches nearly every MOB code value, not two. |
| 2 | T-117's `rso = 0 OR marker <> '●'` contradicts OR-22b | contradicts (high) | contradicts only under the design's own rso rule | **WOUNDED** | OR-22b (6183) says "migration 116's regulation-only rule (○) does not apply to it". That holds if the clause is dropped, **or** if `regulatory_stratum_only` is 0 on a cell whose code row a study confirms. The engine's existing proxy branch already sets rso = 0 when the basis "is no longer TRUE[ly]" regulatory only. Design §2.3 item 2 defines rso from the governing refs alone, and confirmers are never governing, so a confirmed code cell gets rso = 1 and ●, and also carries the code-derived flag beside a full circle. Live reach today is nil: all three `confirms` edges have label referents (`(48,None,1),(49,None,1),(54,None,1)`). |
| 3 | C10 route-gated, not "⚠ passes" | route-gated (medium) | route-gated, **for unretrievable sources only** | **WOUNDED** | The owner's words support a route gate: OR-23 at 4725, "This applies only when the source is properly cited in an academic context". They do not support "⚠ passes". But OR-23 and `tier-system.md:77` say "An unretrievable source". The design (line 123) paraphrases this as "an unverified source anchors only with a route", and §1.3 item 7 gates on `verification_status <> 'VERIFIED'`. Five of the six it drops were retrieved (defect D1). |
| 4a | No live headline on params 3 or 12 moves under the union | holds (high) | holds on every parameter | **SURVIVES** (but see LOW note) | `union.py` over all 20 lens cells of parameters 3, 4, 5, 6, 8, 9, 11 and 12: 3×MOB stays 5 %, 12×MOB stays 6000 mm, and every other cell is `pending` before and after. Note: `specifications` holds 8 rows, all retired (`select count(*), sum(retired_at is null)` → `(8, 0)`). "Live" means engine-computed; nothing is published, so the claim protects no printed page yet. |
| 4b | An OD-58 statement fits no existing record; `worse_at` is the smallest home | yes (medium) | fits no existing record: agreed; smallest home for **this** PR: no | **WOUNDED** | `harm_finding` = 0 on all 214 rows, and its CHECK ties it to `finding` and an `insufficient` edge (db.py:12259). `insufficient` means "not enough" and `exceeds` "more than needed": neither is "struggle more". The design's §2.6 itself finds no harm statement waiting in parameter 3, and parameter 12 has one finding (167, REF-01033) that is not one. The first capture path is T-125. So the rebuild of `extraction_relations` (63 rows, view `v_derived_figure_check`, two indexes), the writer refusals, the reader and the Q-B3 refusal list are all machinery over zero rows in a PR whose goal is a first determination (CLAUDE.md §8, "Nothing is added without naming what reads it": the reader reads nothing). |
| 5 | design_scale is one line, and no reader takes `universal` as "rests on codes" | high | one line: yes. No reader: false | **WOUNDED** | Its own falsifier: `governance/evidence-methodology.md:144` ("a T4–6-only determination is a *Universal-Mode regulatory determination* — `design_scale='universal'`"); state-graph atom `workplan/pipeline-state-graph/ATOMS.tsv:1208` EVI-331, ACTIVE MUST RATIFIED_DOC, "A T4-6-only determination has design_scale='universal'"; `governance/evidence-architecture.md:121`. No code reader (the `git grep` the design ran is clean for scripts/schemas). |
| 6 | 168 needs no new AFTER_DATA marker | correct | correct | **SURVIVES** | The last marker is `-- AFTER_DATA: 20261106053823` (118, 125, 130, 131, 146). Every data migration writing `specifications` is dated 2026-09. The last writing `extraction_relations` is `20261106045634`, before the cutoff. No data migration after the cutoff writes either table (loop over `data_*.sql`, `ts > 20261106053823`, grep INSERT/UPDATE/DELETE: no hit). `build_plan()` places 168 after the last segment. The 8 retired rows have marker NULL, so they pass the widened CHECK on the rebuild's copy. |
| 7 | The six unverified 3×MOB governing sources have no standard number, so they drop out of the governing set | drop (reasoned, [UNVERIFIED]) | the column is NULL; dropping them is wrong for five | **FALSE** for REF-00994, REF-01013, REF-01014, REF-01016, REF-01026; **SURVIVES** for REF-00997 | `retrieval_log.manifest_lines_for(ref, url, doi)` gives usable logged retrievals of 3, 1, 2, 2, 2 for those five and **0** for REF-00997. The manifests show HTTP 200 with sha256, e.g. `nzs.4121.2001.html` 267142 bytes `35a2ddc1…` and `decretolei_163_2006…pdf` 650754 bytes `5744dca7…`. REF-00994's UNVERIFIED standing comes from a title it could not verify (GAP-371: "the logged payload's cover reads 'Accessibility Guide, October 2020'"), not from failing to retrieve it. The owner says such sources are kept with ⚠ (7005), and D-0157 (`assess_cell._is_disqualified` docstring) says "a plain UNVERIFIED source is NOT disqualified". Is dropping them a reserved decision? For REF-00997 (403, Wayback reset) it is not: OR-23/OR-23b decide it, and applying them is delegable. For the five it is not a decision at all: no ruling permits it, and doing it changes the OD-63 render's surveyed code bodies (NZ, Ontario, Portugal, ISO, IPC disappear from the min/mode/median/max colour code). |
| 8 | Size about +350/−90, plus 400–500 migration lines | reasoned | plausible; about 35 % of it serves zero rows | **[UNVERIFIED]** | Design §7: the harm reader (+35), db.py refusals (+15), `route_shown` (+20, mis-scoped), the Q-B2/Q-B3 refusals and one of the two rebuilds go if 4b and D1 are corrected. |
| 9 | Callers swept | listed | incomplete | **WOUNDED** | See "Omissions" O1–O6. |

### Defects in the design, with corrections as exact text

**D1 (CRITICAL): the route gate is applied to unverified sources, but the rule is for unretrievable ones.** Design line 123 reads "OR-23 and OR-23b, as reconciled in `tier-system.md:77`: an unverified source anchors only with a route." `tier-system.md:77` reads "An unretrievable source anchors only …". §1.3 item 7, §4 and line 498 (which calls REF-01016 "an unretrievable source") all follow that misreading.
Correction, §1.2 bullet 3: "OR-23 and OR-23b, as reconciled in `tier-system.md:77`: an **unretrievable** source (no usable retrieval logged: `retrieval_log.manifest_lines_for(ref_id, url, doi)` is empty, the predicate `db.py` already uses for VERIFIED) anchors only with a route. A retrieved source that is not yet VERIFIED is kept and its value carries ⚠ (7005, 7053; D-0157)."
Correction, §1.3 item 7, first sentence: "The engine drops a source that is non-VERIFIED **and has no usable logged retrieval** and has no shown route, before `classify`."
Correction, §4: "3×MOB. Governing: the 27 refs, plus the four T3 grey, minus REF-00997 (no logged retrieval, no route) = 30. The stating rows are 25, 28 and 30: marks {○, ⚠, ○}. Q-B2 fires, so the cell is refused until the owner answers Q-B2. 12×MOB: governing 10, REF-01016 kept (retrieved; row 140, 9000 mm, is a headline row but not a stating row); the value stays 6000 mm, stated by row 116 alone; marker ○; `population`. C10 passes."

**D2 (HIGH): Q-B2 is on the critical path for 3×MOB, and the design says the opposite.** Design line 320 reads "It does not fire on 3×MOB or 12×MOB after the route gate (§3). It would fire on 3 if REF-00994 gained a route." Correction: "It fires on 3×MOB today (REF-00994 is retrieved, so the route gate does not apply to it; marks {○, ⚠, ○}), and again after REF-00994 is verified (marks {○, ◐, ○}). It does not fire on 12×MOB. Q-B2 must be put to the owner before 3×MOB can be published; 12×MOB is publishable without it."

**D3 (HIGH): unverified Co-1 is left out of the eligibility union.** Design §2.3 item 1 reads `eligible = anchoring(b["t1"]+b["co1"]+b["t2"]+b["co2"]+b["t3c"]+b["t3g"]) + b["t45"] + b["t6"]`. `classify` sends an unverified Co-1 to `b["co1_unverified"]`, but an unverified T1 stays in `b["t1"]`. So a co-produced source subject to the same route and ⚠ rules as a T1 can never govern, against OR-6c ("Co-1 and T1 are same value") and CLAUDE.md §6. Correction: `eligible = anchoring(b["t1"]+b["co1"]+b.get("co1_unverified", [])+b["t2"]+b["co2"]+b["t3c"]+b["t3g"]) + b["t45"] + b["t6"]`, with a red test: an unverified Co-1 with a logged retrieval, stating the most accommodating value alone, governs and is marked ⚠ (red: excluded). No live reach today: none of the 8 UNVERIFIED sources is Co-1.

**D4 (MEDIUM): with the `●` clause dropped, rso ignores confirmation.** Correction to §2.3 item 2: "rso = 1 iff every governing ref is in `b["t45"] + b["t6"]`, the cell is not proxy, **and no governing row takes a confirming study's band in `_confirmed_bands`**." Keep T-117's `(regulatory_stratum_only = 0 OR marker <> '●')` as a guard. That satisfies OR-22b and still refuses a code-only ●, which no ruling allows.

**D5 (MEDIUM): the stating set rests on unit-string parsing.** Rows 76 (REF-01014, T4, 1:20), 78 (REF-01015, T6), 81 (REF-01018, T6), 94 (REF-01025, T3 grey, 1:20) and 113 (REF-01024, T5) state 1:20 but carry annotated `claimed_unit` strings ("rise:run ratio (preferred maximum; …)"), so `bound_on_scale` returns None and they are not stating rows. Normalising those units (a data fix) adds REF-01025 (⚠) and REF-01014 (⚠) to the 3×MOB stating set, and the marker or the refusal changes with nothing going red. Add to §6 stop conditions: "the live-data comparison lists, per cell, the stating rows and the governing rows that state the selected bound in prose but do not parse; a non-empty second list is reported to the coordinator."

**D6 (LOW): `determination_gates` is named as an inbound foreign key.** Design §1.5 item 6 copies this from the T-117 file. `PRAGMA foreign_key_list(determination_gates)` lists evidence_sources, access_needs, base_icf, base_taxonomy_identity and base_parameters, not specifications. Correction: "the inbound keys are `specification_source_links`, `specification_extraction_links` and the self-reference."

**D7 (LOW): "PROXY grades exist on REF-00994 and REF-00995 only"** (line 568). Correction: "Of the three 3×MOB stating sources, REF-00994 and REF-00995 are graded PROXY and REF-00992 has no population-match row. Corpus-wide, 32 rows are PROXY, all for MOB (`select match_grade, count(*) from evidence_population_match group by 1`), so Q3 reaches almost every MOB code value."

### What the design omits

- **O1.** Prose and atom callers of `design_scale = 'universal'` as the code-only basis: `governance/evidence-methodology.md:144`, `governance/evidence-architecture.md:121`, and atoms EVI-331 (`workplan/pipeline-state-graph/ATOMS.tsv:1208`). Name them as T-120's, or supersede them in the ledger. Leaving them unnamed lets a ratified-doc MUST atom contradict the engine with nothing red.
- **O2.** The state-graph atoms still stating the old marker rule, ACTIVE MUST: EVI-062 (`ATOMS.tsv:945`, "entire basis is T4-T6 takes the weak band") and EVI-141 (`:1024`, "Any regulatory_stratum_only cell renders at the weak band"), both against "T4 only half circle"; also EVI-055 and CLM-038. T-117 tells the task to run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after; the design never mentions the graph.
- **O3.** Code comments restating the old marker: `scripts/db.py:6807` ("UNVERIFIED and shown ○"), `scripts/research/retrieval_log.py:2326` ("shown ○"), `scripts/audit/research_batch_dod.py:450` ("grey renders ○"). They are prose callers inside `scripts/` and false after merge.
- **O4.** `skills/evidence-auditor_SKILL.md` lines 45, 46 and 53–56 (T3 clinical ●, T5 ◐, an unverified source "should be ○", a T4–T6 basis "should be ○"), not only line 47; `skills/cross-population-conflict-mapper_SKILL.md:166` (a ● ◐ ○ legend with no ⚠).
- **O5.** How "unretrievable" is derived (D1). No typed column holds it, and `verification_method` is unreliable: REF-00997 says `direct-render` with no usable retrieval. `retrieval_log.manifest_lines_for` is the existing single home. But it counts index-record retrievals too (REF-01002 has 8 usable lines, likely its TRID record and other index pages: [UNVERIFIED] which). Those lines are what OR-23's "valid academic route" would cite, so Q-B4 is partly answered by existing records.
- **O6.** 12×MOB is the first cell publishable after part 1 with no owner answer, and 3×MOB is not (D2). The design's summary implies both.

### Open owner questions: owner-only or answerable?

| Q | Design | Antagonist | Blocks part 1? |
|---|---|---|---|
| Q3 (PROXY → thin) | owner | **Owner-only.** `tier-system.md` §5 "Not yet ruled (owner)" and ledger 7092 "Whether any PROXY grade makes a value thin". Reach is 32 rows (D7). | No. Circles stand meanwhile; a later yes flips glyphs reversibly. |
| Q3b (`rests_on_proxy_inference` → thin) | owner | **Answerable from the ledger, delegable at medium confidence.** The thin causes are a project inference and a value that "mixes … then it's a new value proposed" (7159). The 3×MOB headline is a verbatim code value (rows 25, 30), chosen by U1's own rule ("most accommodating", 7870) under a direction recorded with `direction_ref_id`, so no new value is proposed. Record the reading [ASSUMPTION]. | No |
| Q-B2 (several stating sources with different marks) | owner | **Owner-only** (marker semantics: evidence-tier definitions are DG-NON; 7059 lists it as undecided). Give a recommended default: the best circle among verified, non-grey stating sources; ⚠ only when every stating source is grey or unverified. Warrant: the design's own monotonicity argument in §1.8 ("more evidence would then lower the marker"). | **Yes, for 3×MOB.** Not for 12×MOB. |
| Q-B3 (Co-1, T3 grey, T2 standard_eb under OD-58) | owner | **Owner-only in part.** Co-1 is read "yes", flagged, at 7318 and held at 7325 ("Whether Co-1 statements count under OD-58 beyond the reading above"). T3 grey and T2 national are not addressed. | No (zero records) |
| Q-B4 (academic route for unretrievable T1–T3) | owner | **Partly answerable.** The OR-23 reading at 4758 names the route as "a resolving DOI or index record, or a citing bibliography (the `verification_method` values)". The column's own CHECK comment defines `corroborated-not-retrieved` and `citing-bibliography` as existence established without retrieval. The reading is unratified [ASSUMPTION]; build it as such, or ask in one line. | No (REF-01002 is not gathered for 3×MOB or 12×MOB) |
| Q-B5 (grey-only and below-richness code-only cells) | owner | **Code-only half answerable:** U6 at 7875, "if the only values are from code then code determines the ideal/best". Whether §2.3 richness still sets `pending` is a state rule in evidence-methodology (DG-NON). **Grey-only half owner-only.** | No for 3 and 12. Yes for 4, 5, 6, 9, 11 × MOB, which are pending code-only below richness (`union.py`). |

### SPLIT recommendation

**Ready now (PR B part 1, tooling only):**
1. `band()` table; `EvidenceMarker.WARNING` with no ordinal; `floor_mean` over circles only.
2. Rebuild `specifications`: CHECK `marker IS NULL OR (marker IN ('●','◐','○','⚠') AND (regulatory_stratum_only = 0 OR marker <> '●'))`. No AFTER_DATA marker. Views, trigger, indexes and sequence recreated; foreign_key_check after.
3. Delete the rso override. An unconfirmed row takes its own band. rso is 0 when a confirming study's band is used (D4).
4. Marker = the headline's stating sources (OD-59). ⚠ for grey, or for unverified (retrieved or routed). Refuse on mixed marks (Q-B2), naming the question.
5. Eligibility union including unverified Co-1 (D3); rso and cfo from the final set.
6. A route gate for **unretrievable** sources only (D1), reusing `retrieval_log.manifest_lines_for`. C10 fails on: a governing source that is non-VERIFIED with no logged retrieval and no route; or all governing sources non-VERIFIED or grey under a circle.
7. `design_scale` from the key; the prose and atom callers O1 named for T-120 or superseded.
8. Comment and prose callers O3 corrected; O2 and O4 listed.

**Wait for the owner:** Q-B2, before 3×MOB is determined. Q3 does not block. Q-B3 and Q-B5 do not block part 1.

**Move out of part 1 (not dropped):** the `worse_at` relation, the `extraction_relations` rebuild, the `_write_relation_edge` refusals, the displacement reader and the Q-B3 refusal list. Put them in a separate tooling PR (part 2) that lands before or with T-125's capture path. That PR is then read by a writer that is in use and has an EXAMINED subject. If the coordinator keeps them in part 1, put them in a separate migration file (169) so that a failed `extraction_relations` rebuild does not hold back the marker CHECK.

### Approval list (smallest change first)

| # | Change | Class | Confidence | Evidence command |
|---|---|---|---|---|
| 1 | `band()` to the ruled table | DELEGABLE | high | `grep -n -F 'OD-57 STATUS: ANSWERED' references/project-standards.md`; `grep -n -F 'OD-64: triangle for every grey basis' references/project-standards.md` |
| 2 | `EvidenceMarker.WARNING` with no ordinal; `floor_mean` over circles only | DELEGABLE | high | `sed -n 85,99p schemas/enums.py` (ordinal = len − index) |
| 3 | `design_scale` from the key, one line | DELEGABLE | high | `git grep -n -E '^OD-48( STATUS)?:' references/project-standards.md` |
| 4 | Delete the rso override; unconfirmed row takes its own band | DELEGABLE | high | `grep -n -F 'T4 only half circle' references/project-standards.md` |
| 5 | Widen the marker CHECK, keep the ● guard, rso 0 under confirmation | DELEGABLE | medium-high | `python3 -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select sql from sqlite_master where name='specifications'\").fetchone()[0])" \| grep -n marker` |
| 6 | Marker from the stating sources (OD-59), refusal on mixed marks | DELEGABLE (the refusal); the default answer is OWNER-ONLY (Q-B2) | high / — | `python3 scratchpad/ant1/stating.py <copy> 3` |
| 7 | Eligibility union including `co1_unverified` | DELEGABLE | high | `grep -n -A8 'if ty == "co1"' scripts/assess/assess_cell.py` |
| 8 | Route gate scoped to unretrievable sources (no logged retrieval); C10 rewritten to match | DELEGABLE | medium | `python3 -I -c` running `retrieval_log.manifest_lines_for` over the UNVERIFIED sources (3,0,8,1,2,2,2,2 today) |
| 9 | Q3b recorded as not thin [ASSUMPTION] | DELEGABLE | medium | `grep -n -F "because if it mixes then it's a new value" references/project-standards.md` |
| 10 | Q-B2 asked, with the monotone default | OWNER-ONLY | — | `sed -n 7059p references/project-standards.md` |
| 11 | Q3 asked | OWNER-ONLY | — | `grep -n -F 'Whether any PROXY grade makes a value thin' references/project-standards.md` |
| 12 | `worse_at` and the harm reader, as part 2 | DELEGABLE (shape delegated, 7325) | medium | `grep -n -F 'for the task to design' references/project-standards.md` |
| 13 | Record `standard_number` for REF-01013, REF-01014, REF-01016 and REF-01026 from their logged payloads; resolve GAP-371 for REF-00994 | research PR (rule 10), DELEGABLE | high that the payloads exist | the manifest lines quoted in row 7 of the comparison table |

### Summary

The design reads the owner's table, OD-59, OD-48 and the replay order correctly. Its marker mechanism (stating rows) is sound. It has one critical defect. Its route gate applies OR-23/OR-23b, which are rules for **unretrievable** sources, to every **unverified** source. Five of the six sources it drops from 3×MOB were retrieved (HTTP 200, sha256 logged). That is the only reason 3×MOB comes out ○: correctly scoped, the stating marks are {○, ⚠, ○} and the design's own Q-B2 refusal fires. 12×MOB survives every attack (○, `population`) and is the first cell publishable after part 1. Other defects: unverified Co-1 is left out of the union; dropping the ● guard leaves rso blind to confirmation; the stating set depends on unparsable unit strings. Claim 5's "no reader" is false for prose and the state-graph atoms. The `worse_at` rebuild serves zero rows and belongs in a separate PR. Q3b is answerable from the ledger; Q-B2 is owner-only and blocks 3×MOB.

File: /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/prb-antagonist-1.md
