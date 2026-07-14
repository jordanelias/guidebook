# Stage 4.3 — Phase E Synthesis: Execution Plan
**Version 1.0 · 2026-06-10 · PROPOSED — for owner ratification before execution**
Maps to: master workplan §5 4.3 + §9.5 amendment · BPC-rewrite workplan §8 (Phase E) · PI v10.14 standing rules #2, #4, #6–#11.
On ratification, commit to `workplan/phase-e-execution-plan-v1.md` and record the §9 rulings as DRs per architecture `<migration_and_growth>`.

---

> ## ⟢ Version 1.1 · 2026-06-10 — RATIFICATION + G1 CORRECTION
>
> **Decisions ratified** ("proceed with recommendations with care"). **D-4.3-A** and **D-4.3-B** are filed as `decisions/DR-2026-06-10-synthesis-model-floor.md` and `decisions/DR-2026-06-10-e2g-reverification-scope.md` (committed `93c017f`, with rule-#11 attestations; the rule-#2 capability-floor clarification is queued for v10.15 owner-paste). **D-4.3-C…G** are accepted per the recommendations — but **D-4.3-C also needs owner-side action**: GAP-286 records the scholarly connectors returning "No approval received", so they must be approved in claude.ai settings before E.2b/PMP can use them.
>
> **G1 is CORRECTED — do NOT capture the author rows as a migration.** Careful preflight showed the item as originally worded (inherited from master-workplan §5 3.1: "capture the 165 `evidence_source_authors` rows as a migration") is **categorically wrong** per the ratified, governing **DR-2026-05-28 §Decision**. Those 165 rows are genuine PubMed author enrichment written by the scheduled `source-verification` job; the DR documents that a capture-or-`--rebuild`-replace "would silently delete 167 rows of correct author/run data… must not be done." The divergence is bidirectional (≈210 committed-only enriched rows incl. replacements of stub author lists; 45 migration-stub rows) precisely because enrichment overwrote the migration-produced stubs (e.g. rebuild has `van der Ham, I.`; committed has the full author list). DR-2026-05-28's **ledger step (step 2) is already effectively closed** by the Stage-4.2 reconciliation — `migrate_db` reports no pending. What remains is DR-2026-05-28 **step 3**, an owner design choice, now tracked as **D-4.3-H** (§9). Until D-4.3-H is ruled, **G1 does not execute as an entity migration**; the `resolve_dois`/`verify-urls` write-contract sub-item folds into the ruling, and the re-authored reproducibility-invariant script is scoped to the 7 core invariants (which already exclude these job-owned tables).

---

## 1. Verdict and scope

Stage 4.3 is the program's centre of gravity: re-synthesize the 68 retracted BPCs, give the 13 never-synthesized slugs their first synthesis, populate `evidence_cell_state` + `convergence_assessment`, and remediate the synthesis-content gap batch (GAP-265/266/268/269/270/271/274/275/276/277) — all on the ratified hierarchy (D-A, D-D, D-E).

**The gate `[Stage 1–3]` is not yet met, but it is close.** Three findings frame the plan:

1. **Phase B is essentially complete.** 639/640 sources clear rule #6's gate; **67 of 82 ACTIVE slugs are fully eligible** for Phase E today. The blockers are small and named (§3).
2. **The Track-3 pilot already exists and is mid-flight.** `references/bpc-reasoning/room-acoustic-performance.md` is headed `Status: PILOT (Phase E.1 Track 3)`, with the RT60 rule-#9 walk at Pass 1 (steps 1–3 done) and 7 `reasoning_doc_citations` rows written. The right move is to **resume and complete this pilot under inline review** — not to start a new one (the skill itself states the pilot is "not retroactively reconstructable").
3. **Three protocol artifacts have drifted from the ratified rules** and would corrupt synthesis if executed as written (§3 G4). Fixing them is cheap and must precede the first synthesis commit.

This plan defines: gate closure (§3), the per-BPC protocol with exact schema bindings (§4), the pilot resume (§5), wave structure (§6), the verification battery that replaces the deleted CI gates (§7), risks (§8), the decisions only the owner can make (§9), sizing (§10), and exit criteria (§11).

---

## 2. Ground truth (preflight, 2026-06-10, repo @ `95e5466`, DB v24)

`[READ: audits/bpc-rewrite-workplan-2026-05-11.md — §§5–13 + Appendix A in full this session; §§0–4 prior sessions]`
`[READ: skills/adversarial-research_SKILL.md — full, 222 lines]` `[READ: skills/progressive-measurement_SKILL.md — full, 222 lines]`
`[READ: skills/reasoning-doc-citations_SKILL.md — full, 271 lines]` `[READ: skills/multilingual-research_SKILL.md — full, 582 lines]`
`[READ: references/bpc-reasoning/room-acoustic-performance.md — header + pilot scoping]` `[READ: scripts/validate_reasoning.py — status semantics]`

**Eligibility frontier (rule #6 gate, live query):**

| Class | Count | Disposition |
|---|---|---|
| RETRACTED-PRE-REHAB + eligible | **62** | Main re-synthesis cohort — E-ready now |
| RETRACTED-PRE-REHAB + zero-source | 6 | Re-synthesis, research-first (E.2b builds the evidence base) |
| NULL state + eligible | 5 | First synthesis — E-ready now |
| NULL state + zero-source | 8 | First synthesis, research-first |
| METHODOLOGY-AUTHORED + blocked | 1 | `manoeuvring-footprint-…-methodology`: 1 of 8 sources is the DB's only remaining `AUTHOR-TITLE-ONLY` — Phase-B residue, ~15 min |

**Sources:** 311 COMPLETE + 328 COMPLETE-STATUTORY + 1 AUTHOR-TITLE-ONLY; 635 VERIFIED + 5 UNVERIFIED-1. **Substrate:** `reasoning_doc_citations` 7 rows (all pilot); `source_value_extractions` **0** (exists, unpopulated — R10c); `spec_value_probes` 21 rows / 4 items walked (**88 of 92 items have no PMP walk**); `evidence_population_match` 27; `citation_mining` 7/82 slugs; `item_population_links` 361; `lang_jur_map` **0 rows** (table exists, never populated despite 1.4 "executed" — `[GAP: lang_jur_map empty — A.3 linkage owner-pending]`). Rule #7 fields: 21/296 gaps filled. `conflicts`: 0 rows (populated by the arbitration tail, §6 W-last).

**Cell-state machine (2.3, bound):** `evidence_cell_state(cell_id, item_code, population_code, state, design_scale, convergence_id, confidence_dimensions_present/absent, confidence_synthesis_basis, gap_register_id, not_applicable_rationale, has_unverified_sources, all_sources_disqualified, …)` — cells are **item × population (× design scale)**, with the 2.4 validator enforcing pending ⇒ gap-link. `convergence_assessment(convergence_id, status, clinical_sources, co1_sources, co2_sources, down_weighted_sources, discounted_sources, rationale, synthesis_approach, …)` — the convergence-not-evidence doctrine made queryable. Workload bound: 361 item-population links across 92 items; `room-acoustic-performance` alone sources 13 items.

**The 4.3 gaps (live):** GAP-265 (P1, DSDG 2440 mm corridor uncited), GAP-266 (P1, Steinfeld 2006/BS 8300 turn uncited), GAP-268 (P1, DEAF invisible in 5 circulation/wayfinding BPCs), GAP-269 (P1, 1800 mm vs 2440 mm internal contradiction), GAP-270 (P2, 17 code-floor BPCs), GAP-271 (P2, "aligned on best practice" pattern), GAP-274 (P1, 3 STUB BPCs cited in Part 4), GAP-275 (P2, Co-1 0/24 in residential-entry), GAP-276 (P2, kitchen 1500 mm code floor), GAP-277 (P3, IntD existence question). Also bearing: GAP-283 (mining 7/82 — closes incrementally via E.2b Step 4), GAP-286 (connectors "No approval received" — §9 D-C).

**Doctrine SHA for rule #11 tokens:** `373255e`. Attestation infra present (`attestations/*.json`, `schemas/attestation.schema.json`). `[GAP: Stage 1.1 re-attestation list not located in governance/ or decisions/ — 4.1 preflight must find or reconstruct it]` `[GAP: "Multilingual Research Protocol v4" and the 14-language Keyword Compendium not located on disk — multilingual pre-run inputs; locate or declare-and-author before the first E.2b run]`

`[NULL: Stage-2 machinery re-verified this session via rebuild + validators — no defects found; trail in 2.5/4.2 summaries]`

---

## 3. Gate closure — must land before the first synthesis commit

Ordered; G1–G5 are mine to execute on "proceed", G6 is yours.

- **G1 — Stage 3.1 (R3-a).** Capture the 165 `evidence_source_authors` rows as a data migration (diff committed DB vs `--rebuild`; emit INSERTs); fix the `resolve_dois` (and `verify-urls`) write-contract so scheduled jobs stop writing outside the migration framework (per D-B); re-author the GAP-290 reproducibility invariant as a level-2 script now that CI's blocking copy is gone. Acceptance: `--rebuild` yields 1244 authors; invariant script exits 0.
- **G2 — Phase-B residue (1 source).** Upgrade or CLOSE-DELETE the single `AUTHOR-TITLE-ONLY` source blocking the methodology slug. ~15 min.
- **G3 — Stage 4.1.** Locate the Stage 1.1 re-attestation list (`[GAP]` above) and complete the sweep against doctrine `373255e`. For GAP-265/269: these are content claims about specific corridor values — they can only truly close inside the circulation-cluster synthesis (§6 W1). Proposal: 4.1 attests and re-scopes them to W1 deliverables rather than closing them on paper first (**D-4.3-F**, your call).
- **G4 — Protocol-drift fixes (caller-sweep duty, architecture `<migration_and_growth>`).** Three small commits:
  (a) `reasoning-doc-citations` pre-check still requires `metadata_quality='COMPLETE'` only — predates DR-2026-05-18. As written it would wrongly disqualify all 328 statutory sources, i.e. most jurisdiction cells. Fix to `IN ('COMPLETE','COMPLETE-STATUTORY')` (matches PI rule #10 and the already-updated audit script).
  (b) `multilingual-research` completeness thresholds still say "all 24 jurisdictions" / "12 of 24" / "16 of 24" while its own axes declare 46; its embedded tier table predates the Stage 1.1 ratified hierarchy. Re-base thresholds proportionally to 46 (24→46, 12→23, 16→31 unless you prefer different floors) and point the tier table at `schemas/tier_derivation.py` as canonical.
  (c) Stale model pins ("Sonnet 4.6 / Opus 4.6") in skill headers — update per **D-4.3-A**.
  Reconcile all three in `references/skill-registry.md` per architecture.
- **G5 — `lang_jur_map` population.** Mechanical migration from the skill's own language↔jurisdiction text (EN→US/UK/CA/AU/IE/NZ/SG/…, FR→FR/BE/CH, etc.). Flagged to you because the table's emptiness traces to the owner-pending A.3 item.
- **G6 — §9 rulings.** Nothing in §4 onward executes until D-4.3-A and D-4.3-C are ruled; the rest can be ruled at their first point of use.

---

## 4. The per-BPC protocol (the unit of work)

Two passes per slug, mirroring the workplan's E.1→E.2h pipeline and PI rule #2's facts/judgment split, with `validate_reasoning`'s status enum (`DRAFT → OPUS-PENDING → COMPLETE`) as the stage gate. **Write-contract: every DB write ships as a data migration via `emit_data_migration.py` (forward-only), applied in place to the committed DB and committed together with the touched files** — no direct writes, per the reproducibility invariant. Synthesis-bearing commits carry `[DOCTRINE: 373255e]` before the timestamp + an `attestations/<slug>.json` per rule #11. Push is rebase-aware (live scheduled jobs still advance `main`).

**Pass 1 — FACTS (target: doc validates at OPUS-PENDING; steps 1–4 complete):**
1. `research-log-manager CHECK` (rule #4); load the slug's class (§2 matrix) and prior search-log state.
2. **E.2a** — create/extend the reasoning doc from `_template.md` §A (evidence inventory) by joining `source_slug_links` × `evidence_sources` × `search_languages` × `search_coverage`. Mostly mechanical.
3. **E.2b** — multilingual research at 19×46 per the skill, **with the workplan's own mitigation as standing policy**: priority jurisdiction-language cells searched genuinely; the remainder marked `PROVISIONAL-NOT-SEARCHED` rather than blocking (ratify in **D-4.3-G**). AR/HI/ID/SW/BN results flagged `[UNVERIFIED-TERMS]` until A.11 compendiums exist. Step 4 of the skill runs `citation-miner` per confirmed Tier-1/2 source batch (this is what closes GAP-283 incrementally). New sources enter at `UNVERIFIED-1` and are upgraded before they bear weight.
4. **Extraction substrate** — every retrieved jurisdiction/parameter value becomes a `source_value_extractions` row (the 018 substrate, currently empty) with section locator. **Rule: no step-3 table cell without a backing extraction row.** This makes the table mechanically auditable (cells ↔ extractions ↔ citations join).
5. **E.2c** — rule #9 steps 1–4 per qualifying parameter (declaration; per-population worst-case; jurisdiction table derived from extraction rows; lowest-barrier code per population).
6. **Rule #10 sub-rule 2** — a `reasoning_doc_citations` row per jurisdiction cell from a genuine re-read of the cited section (`value_match`), with the skill's PAYWALL paths (downgrade / corroborate / `paywall_purchase_candidate=1`) applied honestly. The detection question ("does the section state this value, or speak to the topic?") is answered per cell.
7. **E.2d** — cross-population conflicts logged per-population, never reconciled inline; queued for the arbitration BPC (step 9 flags).
8. `validate_reasoning` at OPUS-PENDING (steps 1–4 error-level) → **facts commit** (doc + migration + attestation + `[ADHERENCE-LOG]`).

**Pass 2 — JUDGMENT (synthesis-capable model only, per rule #2 / D-4.3-A; target: COMPLETE):**
9. **E.2e** — `adversarial-research` per synthesis claim and per gap the BPC closes: all five outputs (prior, queries, CI+shift, named dissenter, falsification) + `evidence_population_match` grades. Topic-vs-claim question answered in writing per claim.
10. **Rule #8** — PMP walk per numerical specification value the BPC asserts (after adversarial clears the claim): full `spec_value_probes` walk to strict termination or a logged waiver; `items.pmp_*` updated. Multilingual probes only where E.2b surfaced divergent target-language values (skill's fan-out rule).
11. **Steps 5–9** — tiered evidence with T4/T5 excluded at step 5; guidebook chosen value per population; rationale; trade-offs; step-9 conflict flags. **Language rules enforced at write time:** every code-floor citation carries explicit rejection/convergence-not-evidence language (GAP-270); the "aligned on best practice" pattern is banned (GAP-271 — add a grep check to `validate_reasoning` or a small level-2 audit so this is mechanical, per the enforcement spectrum's promotion path).
12. **Rule #10 sub-rule 3** — `reasoning_doc_citations` rows (`claim_match`) for qualitative/definitional claims; `CONTRADICTED` invalidates and forces revision.
13. **E.2g** — BPC file synthesis sections written; `PRE-REHABILITATION` banner overwritten; cross-references doc↔BPC. Prior retracted synthesis handled per **D-4.3-B** (recommended: claim-inventory only, `[SELF-AUTHORED — bias risk]` discipline, no retained prose).
14. **Cell-state writes** — `evidence_cell_state` rows for the slug's sourced items × applicable populations (× design scale): `stated`/`provisional`/`pending` (the ●◐○ map), `pending` rows carrying `gap_register_id` (2.4 enforces), `not_applicable_rationale` where a pairing is genuinely out of scope; one `convergence_assessment` row per evidence cluster recording clinical/Co-1/Co-2 composition, what was down-weighted or discounted, and why — jurisdictional agreement recorded as convergence, never as evidence.
15. `bpc_metadata` → COMPLETE; **E.2h** validators (`validate_reasoning` at COMPLETE, `validate_bpc`, `validate_evidence_state`) → **judgment commit** → spot-check quota (§7).

---

## 5. The pilot — resume `room-acoustic-performance` (Track 3 mandate)

Already designated, mid-flight, and the strongest possible exercise of the machinery (32 eligible sources, 5 parameters — RT60/NC/dB(A)/STI/NRC, 13 sourced items, multi-population including DEAF/NDV/DEM/NEU/OFS). Remaining pilot scope, in order, **with an inline owner-review checkpoint after each numbered block**:

1. Resolve the existing `NOT-FOUND` citation row (audit C1) and finish the RT60 walk: steps 4–9 + sub-rule-3 rows. *(First review: a complete rule-#9 walk.)*
2. First PMP walks — the RT60-bearing items among the 13 (e.g. the ≤0.4 s convergence point the doc names). *(Second review: walk quality, alt-phrasing independence.)*
3. Remaining parameter walks (NC, dB(A), STI, NRC) at calibrated pace.
4. First cell-state + convergence batch for the 13 items. *(Third review: does the cell machine express the doctrine faithfully?)*
5. E.2g banner overwrite + COMPLETE. *(Fourth review: ship/no-ship; extract the calibrated per-step cost model and the reusable doc patterns before scaling.)*

Pilot exit criteria: all §4 steps exercised at least once; all level-2 audits exit 0; the per-slug cost model (§10) re-based on observed effort; review notes folded into the protocol before W1.

---

## 6. Waves (post-pilot)

Ordering per workplan Appendix A (P1-gap slugs first; population-general before feature; cross-population LAST), refined by the live gap content and shared-source clustering (e.g. REF-00050 spans 6 slugs — re-reads amortize within a wave):

- **W1 — Circulation/wayfinding cluster** (`accessible-circulation-geometry`, the mobility population-general slugs, bariatric/turning slugs, `wayfinding-dementia-spatial-design`, the 5 GAP-268 BPCs): carries GAP-265, 266, 268, 269. The 1800-vs-2440 contradiction (269) is resolved as a logged cross-population conflict, not papered over.
- **W2 — GAP-270's 17 code-floor BPCs.** `[GAP: the 17-BPC list lives in bpc-audit-pass0 F-X2 — extract during W1]`. Doctrine-sensitive batch; the rejection-language rule from §4.11 is the deliverable.
- **W3 — Remaining eligible slugs** by Appendix-A tier and shared-source clusters; GAP-275 (residential-entry Co-1) and GAP-276 (kitchen) land in their slugs' runs.
- **W4 — Zero-source 14** (research-first). Note: several (`economics-sources`, `construction-cost-data`, `case-study-…`) may be reference registries rather than synthesis BPCs — classify at wave start and route stubs per Decision 4 (gap-naming docs, no 9-step). GAP-274's 3 STUB BPCs handled here: stub docs authored, Part-4 citations re-pointed. GAP-277 (IntD existence) surfaced to you at this wave.
- **W-last — Cross-population arbitration** (the workplan's G.4, pulled into 4.3's tail because 4.4 needs it): a dedicated judgment session over the accumulated step-9 flags, populating the `conflicts` table — which is what gives the webpage's conflict pages content.

Per wave: regenerate `parts/v10` (stub mode) so progress is visible and reproducible; run the §7 battery; checkpoint handoff.

---

## 7. Verification battery (enforcement with CI deleted)

The blocking gates are gone; this is the level-2 replacement, run as discipline, results logged:
- **Per pass:** `validate_reasoning` (status-appropriate), `validate_bpc`, `validate_evidence_state --states-only`.
- **Per session:** `research_protocol_audit.py`, `pmp_audit.py`, `reasoning_doc_citations_audit.py`, `adherence_log_audit.py`, `audit_evidence_metadata.py` — all must exit 0 before session close; plus the spot-check quotas the skills mandate (1 closed gap traced to primary text; 1 PMP walk step-pass traced; 1 citation re-opened at its section).
- **Per wave:** `migrate_db.py --rebuild` invariant check (now including the 1244-author invariant from G1); `generate_parts.py` regeneration; the GAP-271 language audit.
- **Terminal mechanical proof:** `generate_parts.py --mode full` exits 0 — its gate is exactly 4.3's deliverable (every ACTIVE BPC COMPLETE + cells populated).

---

## 8. Risk register (inherits workplan §12; deltas for this environment)

| Risk | Mitigation |
|---|---|
| **PAYWALL cascade on statutory cells** (most jurisdiction values live in paid standards) | Skill's three paths applied per cell; `paywall_purchase_candidate` aggregated per wave for your purchase decision (**D-4.3-E**); official free summaries/transpositions as corroboration; honest `NOT-FOUND`/downgrade over pretended verification |
| **Verification theater at scale** (rote rdc/PMP rows) | Audits C1–C8 + C3/C4 per session; spot-check quotas; >70 %-EXACT distribution flag; the detection questions answered in writing |
| **Anchor bias from retracted syntheses** | D-4.3-B recommendation: claim-inventory only; `[SELF-AUTHORED — bias risk]` on any consultation of prior text |
| **19×46 fan-out (≈874 cells/slug)** | PROVISIONAL-NOT-SEARCHED policy (workplan's own HIGH/HIGH mitigation), priority set per D-4.3-G; PMP stays EN-default per skill |
| **Scheduled jobs writing the DB mid-wave** (`verify-urls`/`resolve-dois` commit directly to main) | G1 write-contract fix; until then, rebase-aware push + re-capture; option: pause the two schedules during waves (your call) |
| **Missing inputs** (keyword compendium, Protocol v4, re-attestation list) | Named `[GAP]`s with locate-or-author tasks at their first point of use; nothing proceeds on memory in their place |
| **Context budget per session** | One pilot block or 1–3 slugs per session; checkpoint at ~85 %; handoff per `<session_close>`; no mid-walk session ends |
| **Single-reviewer ceiling** | The pilot's inline reviews + the skills' escalating spot-check schedule are the documented partial mitigation — stated, not solved |

---

## 9. Decisions required (owner) — nothing in §4+ executes before A and C

- **D-4.3-A — Model floor for synthesis (rule #2).** Rule #2 and the skill headers say "only Opus". This session runs Fable 5, which sits above Opus. Recommendation: rule #2 is a capability floor, not a brand pin — ratify "Opus-class or above" via a one-line DR + queued PI clarification, and sweep the stale model pins (G4c). Without this ruling I will not write `best_practice_synthesis`.
- **D-4.3-B — E.2g reverification scope** (the deferred decision the master workplan surfaces at 4.3). Recommendation: **full re-synthesis**; prior retracted text may be consulted only as a claim inventory to verify, never retained as prose — under rule #10 the verification machinery is the dominant cost anyway, so salvage saves little and imports anchor bias.
- **D-4.3-C — Scholarly-connector posture** (the preferences carve-out marked `[DECISION REQUIRED]`; GAP-286). Recommendation: option (b) — scholarly connectors (PubMed, Consensus, Scholar Gateway) auto-activate for T0/T1 retrieval during 4.3; they are the fastest path to the peer-reviewed sources PMP's strict termination requires. Note GAP-286 records "No approval received" — the connectors likely also need approval in your claude.ai settings. Option (a), web-only, is workable but slower and weaker on strict-search recall.
- **D-4.3-D — Ratify the resumed pilot** (§5) and its four review checkpoints.
- **D-4.3-E — PAYWALL/purchase posture:** budget for standards purchases (aggregated candidates per wave) vs. accept systematic downgrade-or-corroborate on paid statutory text.
- **D-4.3-F — GAP-265/269 ownership:** close at 4.1 (paper) or re-scope to W1 (substance, recommended).
- **D-4.3-G — Coverage policy:** ratify PROVISIONAL-NOT-SEARCHED + the priority jurisdiction-language set per slug class; ratify the G4b threshold re-basing (23/46 Co-1, 31/46 Tier-5, or your preferred floors).
- **D-4.3-H — `evidence_source_authors`/`pipeline_runs` reproducibility posture (DR-2026-05-28 step 3; surfaced by the G1 correction).** *(3a, recommended)* declare these "job-owned" tables, authoritatively written by the `source-verification` scheduled job, explicitly **exempt** from the migration-reproducibility contract; scope the re-authored reproducibility-invariant script to the 7 core invariants (already excluding these tables — matches the deleted CI's actual scope) and align the architecture `<data_layer_pattern>` wording to say so. *(3b)* have the job emit a snapshot migration each run (full-DB reproducibility; more job-side engineering). This is the real content of Stage 3.1 / G1; the naive "capture as migration" path is ruled out by DR-2026-05-28.

Draft DR stubs for A and B are appended below for one-step ratification.

---

## 10. Sizing and cadence (honest)

The workplan priced Phase E at ~1,170 h for 95 slugs. Re-based on 82 slugs and the live substrate — 67 already eligible, mining and extraction substrates in place but **88/92 items still needing PMP walks** and `source_value_extractions` starting from zero — the equivalent figure is **~950–1,300 h of protocol-grade work**: pilot 2–3 sessions; then roughly 1 high-coverage or 2–3 low/mid slugs per session once templated; W-last arbitration as a dedicated session. This is a multi-month program executed in session-sized increments with per-wave checkpoints. `[CONFIDENCE: medium — high on structure and gates (grounded in full reads + live queries); medium on throughput until the pilot calibrates the per-step cost model. The pilot exists partly to convert this to high.]`

## 11. Exit criteria (4.3 done when all hold)

1. All 82 ACTIVE slugs at `evidence_state` terminal (COMPLETE, or stub-documented per Decision 4), `bpc_complete=1`, banners overwritten; reasoning docs pass `validate_reasoning` at COMPLETE (workplan §13 BPC criteria 1–9).
2. `evidence_cell_state` covers every applicable item×population (361 links) with no orphan `pending` (gap-linked) and `convergence_assessment` populated; `validate_evidence_state` exits 0.
3. Rule #7 fields on every gap closed in 4.3; PMP walk or logged waiver for every numerical-spec item; rdc rows for every jurisdiction cell and load-bearing qualitative/definitional claim; zero unresolved `CONTRADICTED`/`DIFFERENT`.
4. GAP-265/266/268/269/270/271/274/275/276 closed with protocol fields; GAP-277 ruled; GAP-283 at ≥1 mining row per ACTIVE slug; `conflicts` populated by W-last.
5. All §7 audits exit 0; `--rebuild` reproduces the DB including the author invariant; attestations present for every synthesis-bearing commit.
6. **`generate_parts.py --mode full` exits 0.**

---

## Appendix — draft DR stubs

**DR-A (synthesis model floor).** *Per PI rule #2 and skill model-pin headers, `best_practice_synthesis` is restricted to "Opus". Ruling: the restriction is a capability floor — "Opus-class or above" — satisfied by Claude Fable 5 (Mythos-class, above Opus). Facts-pass work remains unrestricted. PI v10.15 queues a one-line clarification to rule #2; skill headers swept (G4c). Rationale: the rule's purpose is judgment quality, not brand identity; pinning to a superseded model name would invert the rule's intent.*

**DR-B (E.2g reverification scope).** *The 68 RETRACTED-PRE-REHAB syntheses are re-synthesized in full. Prior synthesis text is admissible solely as a claim inventory — a checklist of assertions to verify or discard under rules #7/#8/#10 — and is never retained as prose. Consultation of prior text is tagged `[SELF-AUTHORED — bias risk]`. Rationale: under rule #10 the cost of synthesis is verification, not drafting; salvage offers minimal savings against material anchor-bias risk in a single-reviewer methodology.*
