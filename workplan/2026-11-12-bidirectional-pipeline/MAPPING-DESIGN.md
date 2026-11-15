# The lens of a code value: the recording session judges and writes it; the maps only propose (revised design)

**Status.** Written 2026-11-15 by an Opus-class designer on the owner's instruction ("have Opus design mapping for codes and identities etc then fold into remediation plan and finalize it"), then revised after an independent critic's attack (findings: `scratchpad/session_2026-11-13-edmonton-checklist-pass/sweep/adj/CRITIC-MAPPING.md`). The first version (a read-time crossing view and an engine edit) was withdrawn. Not read by the owner. The ledger outranks this document (CLAUDE.md rule 0); the term-resolution plan outranks the remediation plan where they conflict. Counts come from commands given beside them: re-run, do not trust. The designer edited no repository file; the end-to-end run used scratch copies of the database, and the repository database's sha256 (`3c575c89…`) was unchanged.

**What changed from the first version.** The read-time crossing (`v_figure_identity`, an edit to `_lens_clause`) and the claim that OR-1 is superseded are dropped. The recording session judges a code value's lens and writes it, identity included. The maps become the writer's source of proposals. Two of the three proposed tasks dissolve; two of the three owner questions are withdrawn.

## 1. The crossing

**What each map holds (re-verified):**
- `identity_icf_map`: identity → ICF, many-to-many, 61 rows, each with mechanism, `mapping_confidence` and provenance.
- `access_need_icf`: need → ICF, 43 rows, no provenance column and no `db.py` writer; 38 rows are e-codes; five are b/d codes: A-PRECISION b765, A-TIME b164, A-SELFCARE d510/d540/d550 (`select need_code, icf_code from access_need_icf where icf_type<>'e'`).
- The medical maps hold 0 rows.
- No live table maps needs to identities. Migration 109 dropped the earlier route: `population_axis_map` (53 rows) and `access_need_axis_map` (21 rows) (`scripts/migrations/109_drop_axes.sql:6-12,44-45`).

**Where the crossing happens: at recording, by judgment.** The owner's words: "all code values will have a lens even if it's not explicitly stated. use contextual judgment"; "at the moment of recording the row is when you will have best idea of context"; "typically anything to do concerning mounting height will concern wheelchair users"; "yes lens in judgment"; "ICF and access needs are supposed to be mapped to populations too so populations still get coded as a result". Rule 8: the script asks for a judgment and records it with its warrant. In the call that records a code value, the session writes: the ICF link, the access-need link, and an **identity link for each group it judges the value serves**; each link with `basis` `context`, `basis_text` (the source's words) and `basis_reason` (the judgment): T-126's two cells.

**The writer is legal today.** `extraction_lens_links` allows one lens per row and several rows per figure. Extractions 33 (`A-EFFORT, MOB`) and 165 (`A-EFFORT, MS`) already carry an identity row beside a need row. (The first version's claim that writing the identity would break the CHECK was false.)

**Rule 5 is not breached.** A map row says a group typically has a limitation in an activity. A link says this clause serves that group, on its own warrant. They are different facts. D-0182 answered the 2026-08-28 "copy of the map" argument by ruling multiplicity acceptable (ledger line 2572).

**The engine does not change.** `_lens_clause` stays as D-0184 and OR-1 ruled: a figure reaches a cell only through the links written on it (`scripts/assess/assess_cell.py:242-257`). OR-1 is not superseded; there is no view.

**Two ledger corrections must be appended on contact (rule 0), in the plan-fold commit** (a ledger entry needs no attestation):
- (i) The sixteenth-set entry's ACTION "reach the populations through the mapping; do not store the derived identity beside them" was the recorder's reading under an [ASSUMPTION], not the owner's words. Replace it: populations are coded "as a result" of the ICF and need links because the maps propose and the session confirms and writes them.
- (ii) OD-31's option text, "under a general disability heading, no identity, only its ICF and access-need lenses", is superseded for code values whose context the session judges; it still holds for the `heading` basis. Prose supersession only (the ledger cannot carry a marker beside its own earlier text).

## 2. The proposals and the missing rows

**(a) Need → identity proposals: read nothing new.**

| Option | Verdict | Why |
|---|---|---|
| Rebuild the dropped axis maps | Rejected | "Axes" is retired vocabulary the owner told us not to relitigate; WRK-181 asks for population ↔ ICF pairs, which is `identity_icf_map`'s job, not a need route |
| Add need → b/d rows to `access_need_icf` | Rejected for now | Needs a provenance column and a new writer; the proposals they would add are reachable more directly from the figure's own ICF link |
| New `identity_need_map` | Rejected | A second home beside `access_needs.absorbs`, and code that adds no proposal a judging session needs |
| Propose from what exists | **Chosen** | No new table, column or verb |

How it works: the writer proposes identities from `identity_icf_map` for the ICF codes the session is about to write, plus `access_need_icf`'s existing b/d rows for its needs. Each proposal shows its `mapping_confidence`, mechanism and provenance. It also shows the need's own registry text (`design_obligation`, `absorbs`) as reading for the judge, never parsed. OR-1 requires every relevant model on a figure, so a code value carries an ICF code and the ICF side always yields proposals. Proposals are aids, not a whitelist: the session may write any live identity, with its warrant. `access_needs.absorbs` stays (`joined_cells_census.py` flags it, 16 of 17 rows delimited); with no need → identity table beside it there is no second home; splitting it is a schema-shape gap to be filed, not part of this design.

**(b) The ICF code for reach.** ICF nests d4452 *Reaching* under d445 *Hand and arm use* (siblings: pulling, pushing, turning, throwing, catching); d4153 *Maintaining a sitting position* and d4154 *Maintaining a standing position* nest under d415. These titles are from the designer's knowledge and unverified: the research task fetches the WHO payload. The d-chapter records activity limitations: wheelchair users are limited in reaching, from a seated reach range, but not in hand and arm use as a whole, so the child is the true claim and the parent over-claims. `base_icf` has no hierarchy and `_lens_clause` matches codes exactly, so a d4452 figure does not reach a d445 cell. **Writer rule:** propose the most specific code the clause supports, and show the parent beside it. **Codes to mint** (`db.py add-icf-code --title-payload <WHO payload>`): d4452, d4153, d4154; title d415. Then map WHEEL → d4452 and WHEEL → d4154 or d4153 (the batch judges which), with mechanism and provenance. **Five identities with no ICF row** (ADHD, DEAFBLIND, EPI, MS, VES) get proposed rows re-derived from `population_axis_map` and each axis's ICF anchors (`governance/functional-taxonomy.md:150-154`): WRK-181's direction, which migration 109 calls "an owner item". **BAR, LPA, TALL get no anchor** (the 2026-09-11 ruling cited in migration 109): judged directly, never proposed.

**Who judges.** The batch session judges each row. The owner confirms the full list in one answer (OD-67) before the data pull request merges, because these rows decide which people a value serves: population taxonomy.

**(c) The marker.** The ledger's ACTION on thin: "derive thin from the population match and the proxy-inference record; do not count roots to decide it; do not store it beside them" (ledger 7089-7096). A `context` link is neither of those records, and `context` is refused below tier 4 (T-126). So: a code value carries its regulatory stratum's marker, which `specifications`' CHECK forces to ○ when `regulatory_stratum_only`; a context link adds no ⚠. A research figure's identity comes only from its own words or its study's participants, so thin stays derived from PROXY grades, as ruled. The mounting-height default shows its marker plus the visible label "assigned: mounting height; typically concerns wheelchair users" (basis `context`): the owner's rule of thumb, recorded with its warrant, not the project's conjecture about evidence. The earlier OD-69 (research figures naming no group) is withdrawn: the `context` basis cannot reach research figures.

**(d) End to end on a scratch copy.** T-102's WHEEL simulated as a child of MOB; d4452 minted with WHEEL → d4452; a scratch parameter "control mounting height"; a T6 code row "Controls shall be mounted at a height of not more than 1200 mm" recorded with three links: d4452, A-REACH and WHEEL (`basis='heading'` stood in for `context`, which today's CHECK does not admit). `determine` gave: WHEEL; WHEEL+d4452; WHEEL+A-REACH; d4452; A-REACH: in lens, `n_sources` 1, state `pending`, `regulatory_stratum_only` 1, `gap_needed` True; MOB: refused (no figure; T-055's parent gather is not built); BLIND: refused, correctly. So the owner's default reaches the WHEEL cell with no engine change; it reads `pending` because one T6 source fails the §2.3 richness rule, the expected state for a code-only cell. MOB is reached once T-055 lands.

## 3. The engine

No change, and no supersession of D-0184 or OR-1. The scratch run reaches the WHEEL cell through the written link; per-figure `EXISTS` (251-253) and `SELECT DISTINCT e.ref_id` (274) already stop a figure with links in two lens columns being counted twice; `link_payload`, `RULE_VERSION`, K01 and the six `_lens_clause` callers are untouched; the skill prose at `skills/run-pipeline_SKILL.md:261` ("only through the live lens links written on it") stays true.

## 4. Coverage and guards

- **Writer (T-126):** `add-extraction` and `add-lens-link` print the proposals before writing and return `identities_proposed` and `identities_written`. A tier-4-or-above row written with ICF or need links but no identity link, while the maps propose one, prints `WARNING: maps propose <codes> (confidence, provenance); no identity written`. It flags rather than refuses.
- **Audit:** one audit, registered **advisory** in `governance/check-registry.yaml`, printing `EXAMINED: n`; it lists by id every live figure with ICF or need links and no identity link, and every identity the maps never propose. The contract gains one judgment-stage criterion pointing at it (precedent `base-medical-lens-offered-not-adopted`, `governance/pipeline-contract.yaml:35-45`). There are 145 live tier-4-or-above links today (derive by command); all 216 links are `carried`.
- **Flip to blocking: T-059's tooling pull request**, after T-127 and T-128. T-059's selection depends on every code value carrying a lens, and rule 10 bars the research batches from editing the registry.
- **Reader minimum:** every link renders with its basis, so a context-assigned group shows as assigned. Figures the audit lists render under "no group judged yet". Nothing is dropped.

## 5. Tasks

- **T-126 (tooling, wave 1)** carries: the `context` basis and `basis_reason` column (unchanged); **reversed:** §4 item 4 now writes the judged identity link, which "No identity link is written" forbade; the proposal display and warning; the advisory audit and criterion; the ICF registry command extended to `'%reaching%'` so it prints d4452 once minted (as written, its `'%hand and arm%'` prints d445); the skill paragraph (the defaults, proposals as aids, writing the identity). §8's "do not add map rows" stays, pointing at T-128. Still no engine change.
- **T-127 (research)** carries the judged ICF, need and identity links for stored code rows, chosen from the proposals; it runs **after T-102 and T-128**, so rows are tagged WHEEL and d4452 once, not MOB and d445 and then swept again [ASSUMPTION: T-102 step 4 already carries MOB rows by judgment; the ledger warns against sweeping the same rows twice].
- **The new-table task and the engine task dissolve.** The map-filling batch survives as **T-128 (RESEARCH)** (next free number: `ls tasks | grep -oE '^T-[0-9]+' | sort -u | tail -3` prints T-127): mints d4452, d4153, d4154 and titles d415 from WHO payloads, writes WHEEL → reach and seated rows, writes the five WRK-181 rows; every row through `add-icf-code` and `add-population-icf-link` with mechanism, confidence and provenance, after OD-67's confirmation; depends on T-102 (WHEEL minted, SCI retired, which needs T-054 and T-055); needs no new tooling.
- **T-059:** adds T-128 as a precondition and flips the audit to blocking. **T-110:** adds T-128. **T-115:** unchanged (under OD-31 its `ALL` retags get ICF and need links plus judged identities through T-126's writer). **T-018, T-019, T-055, T-091, T-102:** unchanged.
- **Pull request order:** T-126 → (T-054, T-055, T-102 as already planned) → T-128 → T-127 → T-115 → T-059 → T-110.
- **Open items:** OI-73 is resolved by T-126's proposals plus T-128; OI-74 closes with no traversal: the identity is written.

**Tests:**

| Test | Defect it catches | Red before T-126? |
|---|---|---|
| T126-01 (revised) | Mounting-height row: links d4452, A-REACH, WHEEL by `context`; the WHEEL cell gathers it; the result lists the WHEEL proposal from the map with its confidence and provenance. Catches a writer that hides proposals or refuses the identity | Yes |
| T126-11 | ICF-only code row whose map proposes an identity: the warning prints and the audit lists the row. Catches a silent omission | Yes |
| T126-12 | The audit omits a figure that has an identity link and reports `EXAMINED > 0`. Catches a vacuous audit | Yes (no audit exists) |
| T128-A (live after-test) | A WHEEL → d4452 row exists and the scratch run returns WHEEL in lens. Catches a map gap | Red until T-128 |

Dropped as unable to go red: the first version's X-04, X-05, X-07 and the parity check.

## 6. Owner question

- **OD-67. May the batch's full list of new population-to-ICF rows be confirmed in one answer?** The list: wheelchair users → reaching and seated or standing posture, and the five groups with no row (ADHD, DeafBlind, epilepsy, MS, vestibular) re-derived from the retired axis map. Recommended: **yes, in one answer, as for the mobility crossings (OI-03)**: these rows decide which groups are proposed for every code value, which is population taxonomy and the owner's.

## 7. Risks and what the designer could not check

**Risks.** A proposal anchors judgment: a recorder may accept whatever the map proposes (figure 166, one d450 link, would propose BRAIN, COM, MOB, PAIN and SCI); the guard is the visible mechanism and confidence plus the warrant the session must state. Until T-102, the default writes MOB, not WHEEL. A d4452 cell and a d445 cell never meet, because there is no ICF hierarchy.

**Not checked.** The WHO titles; which SCI rows T-102 carries; the 2026-09-11 "no anchor" ruling text; rulings in `sessions/`.

## Disposition of the critic's points

| # | Point | Disposition |
|---|---|---|
| 1 | Intersection hides groups | Fixed: no read-time rule; proposals are not a whitelist (ten identities have no map row, verified) |
| 2 | The first OD-67's benefit false | Accepted; withdrawn; the number reused for the map-row confirmation |
| 3 | Inflation in the adopted direction | Accepted (figure 166 verified); fixed: the map only proposes |
| 4 | Read time was the designer's reading; the CHECK claim false | Accepted (extractions 33 and 165 verified) |
| 5 | Prior homes omitted | Accepted; weighed in 2(a); D-0169 says `access_need_icf` "maps needs to ICF e-codes", so e was the design, not a ban |
| 6 | `link_payload` and `RULE_VERSION` | Moot: no engine change |
| 7 | Unlisted readers | Moot for the engine; the prose stays true |
| 8 | Tests that cannot go red | Accepted; dropped |
| 9 | Blocking unassigned, PR order, deferred supersession, T-126 command | Fixed: T-059 flips the audit; the order lists T-054, T-055, T-102 (T-019 is merged); the ledger corrections go in on contact; T-126's command is extended |
| 10 | d4452 is a child of d445 | Answered in 2(b) |
| 11 | Thin marker inconsistent | Fixed in 2(c) |
