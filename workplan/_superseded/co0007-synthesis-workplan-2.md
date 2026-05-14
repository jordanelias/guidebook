<!-- SUPERSEDED 2026-05-11 -->
> **⚠ SUPERSEDED:** This workplan is replaced by `audits/bpc-rewrite-workplan-2026-05-11.md` (ADOPTED 2026-05-11 in session_2026-05-11h, per PI v10.8 standing rule #6). CO-0007 synthesis (Stage 0.7) is foundation-complete. The synthesis methodology is now governed by PI v10.8 standing rule #9 (9-step rule). Do not use for forward work. Preserved here as historical record. See `audits/bpc-rewrite-workplan-2026-05-11.md` §Appendix E for the full supersession map.

---

# CO-0007 Synthesis: Mission, Throughlines, and Workplan — v2
**Created:** 2026-04-26 03:14 UTC
**Status:** SYNTHESIS DOCUMENT v2 — re-issued per Stage 0.7
**Supersedes:** `workplan/workplan-co0007-synthesis.md` (committed `4ef8cab2b2fb`, 2026-04-25 00:20Z)
**Resolves audit findings:** L-01, L-02 (counts), B-01 (verified figures), N-07 (contamination), and reflects the Stage 0.5 decisions (T-03, T-04, D-03)
**Decisions incorporated:** `governance/pre-stage-a-decisions.md` (committed `619c0bb6`)
**Mission moved out:** `governance/mission-PROVISIONAL.md` (committed `619c0bb6`)
**Workplan reference:** `workplan/workplan-co0007-v3.md` (committed `3385209d`)

---

## What changed from v1

This re-issue corrects v1 in the following respects, all surfaced during Stage 0 verification:

| Change | v1 claim | v2 status | Source |
|---|---|---|---|
| Commit count | "approximately 280 commits" | **2,259 commits** on `main` (rhetorical figure was 8× off; not budget-load-bearing) | 0.2 §M1 |
| BPC files | 78 | **78 topic-slug** (confirmed) + 14 frozen population-level + 1 thermoregulation + 1 index | 0.2 |
| Search-logs | 90 | **76 topic + 14 population** = 90 (confirmed when summed) | 0.2 |
| Part 4 specs | 92 | **92** (confirmed exactly) | 0.2 |
| Spec-DB records | 73 | **73** (confirmed exactly) | 0.2 |
| Appendix A tables | 20 | **20** (confirmed exactly) | 0.2 |
| Jurisdictions | 46 | **49 in standards registry / 24 canonical coverage / 46 prior cite** — three denominators, none labeled (audit L-01/L-02) | 0.2 §M5 |
| Bibliography sources | 557 / 94% verified | **584 / 503 verified (86%)** — library grew, residual tripled to 81 sources | 0.2 §M2 |
| Tier-JSON ↔ bibliography drift | not noted | **33-source drift** between the two stores (live D-02 instance) | 0.2 §M3 |
| Connection register | 189 entries | **`Total connections migrated: 181`; `Next CON-ID: CON-0189`** (next-ID interpretation) | 0.2 |
| Skill files | "approximately 40" | **45 files** (42 active + 3 deprecated subdirectory) | 0.3 |
| Atomic parameters | "60–80 atomic parameters" | **Not a corpus unit** — workplan-side concept for migration unit. Definitional question for A3, not a verifiable count. | 0.2 §M4 |
| BPC contamination | "partly-contaminated synthesis layer" (qualitative) | **0/13 frankly contaminated; 1/13 ambiguous; ~92% doctrinally aligned** | 0.4 |
| Two corpus states surfaced | not noted | **STUB ~7%** (synthesis pending Opus); **MERGED ~7%** (CO-0006 redirect files) | 0.4 §F3 |
| Stage A document count | "Five governance documents" | **Thirteen governance documents** (A1-A13 per workplan v3) | workplan v3 |
| Stage A sessions | 18–28 | **25–37** (workplan v3) | workplan v3 |
| Stage B sessions | 22–34 | **26–40** (B1 multi-form derivation; B4 multi-pilot) | workplan v3 |
| Stage C sessions | 140–200 | **165–245** (C0 added; C2 expanded; C7 includes residual) | workplan v3 |
| Total sessions | 180–262 | **224–334** (corrected arithmetic + new Stage 0) | workplan v3 |
| Real-world estimate | 12–18 months | **15–24 months** (Co-1 cadence + parallelism + project-management overhead are the binding constraints) | workplan v3 |
| Decision points | 12 | **23** (workplan v3) | workplan v3 |
| Mission as artifact | embedded passage | **`governance/mission-PROVISIONAL.md`** committed; A1-A2 canonicalizes | 0.6 |
| Co-1 operational role | implied co-author | **Reviewer with documented Co-author trajectory** (per D-03) | 0.5 |
| Co-1 tier encoding | unspecified | **`tier` + `evidence_type` taxonomy** (per T-03 Option B) | 0.5 |
| Sparse-evidence behavior | unspecified | **State machine: stated / provisional / pending / not_applicable** (per T-04 Hybrid) | 0.5 |
| Audience use-patterns | single-pattern per audience | **Two use-patterns per primary audience** (per audit T-05) | 0.6 |
| Stage 0 verification stage | absent | **Stage 0 added** (8–12 sessions; verification + decision freeze before Stage A) | workplan v3 |

---

## Part I — Multi-Perspective Analysis (corrected)

### Top-down (mission → atoms)

The project exists to **improve accessibility outcomes in the built environment by changing how people who shape those environments think.** Everything else serves this. Five Core Doctrine principles operationalize this purpose (committed in `references/project-standards.md` 2026-04-24 23:38 and 23:46): purpose-of-questions, non-uniformity, three-tier hierarchy, evidence hierarchy with Co-1 co-primary, best-practice-as-most-accommodating-the-evidence-supports.

From those principles, a strategic stance: build a structured knowledge resource supporting multiple navigation modes and embedding questions, variability, co-occurrence, evidence-tier transparency, and tier handoffs at every level.

**v1 said graph-shaped data was "the minimum form."** v2 corrects this: the form follows from B1 (storage form decision), which evaluates ≥3 candidate forms (graph DB, RDF, structured markdown with build pipeline, relational, hybrid) against requirements rather than asserting graph-shaped. Audit v2 §N-05 surfaced this as architectural assertion before derivation.

### Bottom-up (existing artifacts → what they imply) — corrected figures

The project has accumulated **2,259 commits** on `main` between 2026-03-18 and the time of this re-issue. The corpus contains:

- **78 topic-slug BPC files** at `references/bpc/<topic>/<slug>.md`, plus **14 frozen population-level files** at `references/bpc/<POP>.md` (per project-standards rule 2026-03-27)
- **76 topic-slug search-logs + 14 population-level search-logs** = **90 total**
- **92 Part 4 item specifications** at `parts/v10/part04.md` (A:18, B:12, C:6, D:11, E:15, F:8, G:9, H:5, I:4, K:4)
- **73 records in `references/specification-database.json`** (Phase 2A complete; Phase 2B/2C pending)
- **20 Appendix A jurisdiction comparison tables** (A.1–A.20) at `parts/v10/appendix-a-jurisdiction-comparison.md`
- **49 unique jurisdiction codes** in `references/standards-registry.md` (112 jurisdiction-standard pairs); the **24 canonical coverage scope** per project-standards rule is the sampled-research jurisdiction set, distinct from the registered standards
- **CRPD ratification map** (per `references/standards-registry.md`)
- **Bibliography of 584 deduplicated sources / 503 verified (86%)** per `references/bibliography-v11-draft.md` self-meta; **81 [GREY] entries** (citation details unverified). **The bibliography text and the six tier-JSON files (which sum to 551 sources) are out of sync** by 33 sources; reconciliation is C7 work
- **Connection register: 181 migrated entries**; CONSUMED 140, CONSUMED-DEFERRED 42, PENDING 5, plus 3 CONSUMED this session; next CON-ID is **CON-0189**
- **13 doctrinal-divergence parameters** in `references/opus-divergence-synthesis.md` (Ramp Gradient, Threshold Height, Corridor Clear Width, Reach Range, LRV Contrast, Turning Space, Door Opening Force, Anti-Scald Temperature, Grab Bar Height, Slip Resistance, Rest Seating Interval, Classroom RT, Kitchen Worktop Adjustability)
- **45 skill files** (42 active in `skills/` + 3 archived in `skills/deprecated/`)

**What the corpus actually contains:** v1 framed the corpus as "research output with a partly-contaminated synthesis layer." Stage 0.4 contamination sampling (N=15) found **0 of 13 evaluable BPCs frankly contaminated, 1 ambiguous (S10 kitchen, self-flagged PROVISIONAL), 12 doctrinally aligned (4 of those 12 EXEMPLARY)**. The contamination concern that drove the audit is not supported by the sample. Two reasons: (a) most sampled BPCs were Opus-refreshed between 2026-03-28 and 2026-04-09 — the doctrine was being practiced before the rule was committed; (b) the 2026-04-24 23:46 doctrinal rule articulates an existing practice.

**Two corpus states first surfaced quantitatively in 0.4:** STUB (≈7%, BPCs awaiting Opus synthesis — Sonnet correctly defers per protocol) and MERGED (≈7%, CO-0006 redirect files for consolidated topic slugs). Workplan §C3/C7 must accommodate both.

### Lateral (parallel concerns at same level)

Parallel structures with conceptual overlap (largely as v1):
- Part 4 item specs ↔ Parts 6/7 room matrices ↔ Part 5 building-level conflicts (three views)
- Part 4 specs ↔ spec-database (two stores of parameter values — current Phase-2A-complete drift is ~73 records vs 92 specs)
- Part 4 jurisdiction tables ↔ Appendix A tables (two locations of comparison data; drift)
- BPC `best_practice_synthesis` ↔ Part 4 description ↔ Opus divergence synthesis (three locations of synthesis claims)
- **NEW (0.2 finding):** Bibliography text (584 sources) ↔ tier-JSON files (sum: 551 sources) — 33-source drift between two stores of bibliography data

Population-level epistemological inconsistency persists (MOB functional, DEAF cultural-linguistic + functional, PAIN symptomatic, OFS syndromic). Treating as single taxonomy obscures real differences in how evidence applies, how Co-1 should be gathered, how specifications should be framed.

Evidence-tier compression: Tier 1 OT clinical research and Tier 1 anthropometric research have different methods and certainties; Co-1 lived experience as primary evidence and Co-1 as confirmation of clinical findings have different epistemic roles. Stage 0.5 T-03 resolution (`tier` + `evidence_type`) addresses the encoding side; A6 evidence methodology specifies authoring rules per evidence_type.

Jurisdiction definitional inconsistency: 49 registered / 24 canonical coverage / 46 prior synthesis cite — three denominators, none disambiguated. Glossary in A8 jurisdiction philosophy.

### Diagonal (cross-cutting relationships spanning levels)

**Mission ↔ atoms:** "Questions for the designer" connects highest-level mission directly to lowest-level data atom. Audit v2 §T-02 / §D-01 found this throughline is rendering-absent in v1's architecture (item view, population view, conflict-resolution view, respect-visibility view, jurisdiction-comparison view — none questions-led). Workplan v3 §B3 adds **questions-led navigation mode as first-class entry surface**; `questions-renderer` skill (NEW) in C2; question-coverage-validator (NEW) in B2.

**Doctrine ↔ tooling:** Each Core Doctrine rule implies tooling. Workplan v3 §B2 has expanded validator suite to make this concrete: schema-validator, evidence-tier-validator (Co-1-aware per T-03), single-source-validator, cross-reference-resolver, round-trip-rendering-validator, question-coverage-validator (per T-02), variability-coverage-validator (per N-04), design-stage-coverage-validator (per T-06), refresh-staleness-validator (per D-02), Co-1-representation-validator, temporal-coherence-validator, epistemic-defense.

**Evidence tier ↔ skill methodology:** Skill that generates BPC must search Tier 1–3 first, then code data. Audit observation that current sequence places Tier 1 toward end is mitigated by REBUILT BPC-orchestrator, multilingual-research, evidence-auditor in workplan v3 §C2.

**Audience ↔ navigation:** Each prioritized audience implies a navigation mode (per v1). v2 adds use-patterns within audiences (audit T-05): designer at programming AND mid-project; disabled-reader information-finding AND representation-checking; OT clinical-collaboration AND specialist-handoff; policymaker comparison AND rationale.

**Population ↔ Co-1 representation:** Doctrine treats Co-1 as co-primary with Tier 1; corpus is uneven (heavy on autism and physical; light on PTSD, MS, DBL). The structure must make this imbalance visible. workplan v3 §A5 + cross-stage CS5 representation-monitoring address this; gates C4 per population.

**Jurisdiction ↔ disability worldview:** Different jurisdictions encode different theories of disability (ADA rights-based; EU standards-harmonization; Japan barrier-free; India ICF-aligned). Worldview is a first-class data dimension per A8.

---

## Part II — Throughlines (preserved)

Six consistent threads. Wording largely as v1; clarification on T2.

**T1: Specifications serve questions; questions serve people; people are not uniform.** Master throughline. Audit v2 §N-04 added: "people are not uniform" claim is operationalizable — every parameter exposes within-population variability. variability-coverage-validator (NEW) tests this in B2.

**T2: Codes are the floor; evidence is the basis; experience is co-primary.** Seven-tier evidence hierarchy is the spine. v2 clarifies via T-03 resolution: Co-1 is co-primary *parallel* to Tier 1, encoded via `tier` + `evidence_type`, not flattened to "Co-1 IS Tier 1."

**T3: Single sources of truth resolve propagation problems.** Audit v2 §D-02 noted SSoT holds at edit time but not at read time without explicit refresh policy. workplan v3 §B5 adds rendering-refresh-coordinator skill and policy decision (continuous-deploy / periodic-snapshot / versioned-release).

**T4: Three tiers describe the gradient of context-specificity.** Universal Mode (universal), Tier 1 (population), Tier 2 (person). DAR mandatory at all tiers.

**T5: Co-occurrence is the norm.** Default to combinatorial views, not single-population views. Workplan v3 §C6 (conflict migration) addresses combinatorial entries explicitly (estimated 200–400 actual entries from 55 pairs × ~60 parameters).

**T6: The guidebook teaches; it does not prescribe.** Audit v2 §N-08 noted the questions-led pedagogical commitment has thin meta-evidence — the project doesn't engage inquiry-based-learning literature. workplan v3 §A6 adds engagement; §B6 tests with practicing architects; §A1-A2 cites in mission-and-epistemics.

---

## Part III — Meta-Throughlines (preserved with revisions)

**M1: Data shape follows mission shape.** v1 asserted "graph-shaped data with view-layer queries is the minimum form that matches the mission's multi-modality." v2 reframes: the form is selected in B1 from ≥3 candidates against requirements (audit N-05 resolution). Multi-modality is the requirement; graph-shaped is one way to meet it; v1's pre-commitment to graph form is rejected.

**M2: The product is questions; the medium is structured data; the rendering is human language.** Audit v2 §T-02 / §D-01 found "questions" throughline did not traverse to rendering or validation in v1's architecture. v2: questions-led navigation mode + questions-renderer skill + question-coverage-validator complete the throughline.

**M3: Authority and humility coexist through method.** Structured form makes method visible by construction.

**M4: The project is a teaching tool that must be teachable to itself.** Self-applying methodology. C2 cross-cutting requirement: skills must self-apply.

**M5: Co-1 is not an audit step; it is a co-author relationship.** Audit v2 §D-03 (Critical) found doctrine claims this; operations deliver Reviewer. **Stage 0.5 D-03 resolution is operational Reviewer with documented Co-author trajectory** (`governance/pre-stage-a-decisions.md`). The doctrinal claim of "co-primary evidence" applies to Co-1 evidence (the corpus); the operational role of Co-1 collaborators (people) is currently Reviewer. Mission language (`governance/mission-PROVISIONAL.md` §3) declares this. The audit's "ambiguity is unacceptable" finding is resolved by transparent declaration plus trajectory triggers.

**M6: The project's deepest commitment is epistemic.** Audit v2 §D-04 found this is documentation-only, not operationally tested. Workplan v3 §A6 + C2 adds `epistemic-defense` skill (NEW per D-04): periodically tests current claims against simulated external critique (alternative tier orderings, alternative evidence weights, alternative population taxonomies); findings feed A6 revision cycles.

**M7: Time is part of the data.** Audit v2 §D-05 found this is deferred to project end (C11). Workplan v3 §A9 establishes time model as Stage A phase; §C1 builds time-handling into migration tooling from start; supersession-checker skill (NEW) in C2; C11 narrows to documenting practice live throughout Stage C.

---

## Part IV — Mission Statement

Mission was previously embedded in this synthesis as a passage. Audit v2 §T-01 identified that mission "exists only as a passage embedded in a longer document" and the Coda's "sit with the mission" test cannot be operationalized against an informal artifact.

**Mission committed at:** `governance/mission-PROVISIONAL.md` (committed `619c0bb6`, 2026-04-26 02:42 UTC). Adoption test now operates against that file.

**Status:** PROVISIONAL pending A1-A2 canonical version.

**Substantive changes from v1's embedded passage:**
- Audience priority specifies use-patterns (audit T-05): designers at programming AND DD; disabled people information-finding AND representation-checking
- Co-1 operational reality declared explicitly: Reviewer with Co-author trajectory clause
- Sparse-evidence cells declared explicitly: stated / provisional / pending / not_applicable state machine
- Tier encoding declared explicitly: Co-1 co-primary parallel to Tier 1, not flattened
- Methodological boundaries declared (formal new construction; not legal authority; not OT substitute)
- Test-against-which-decisions-evaluated specified as 7-question checklist (added items 5 and 7 cover Co-1 operational respect and clean-data + transparent-methodology)

The mission language is no longer this synthesis's responsibility. This synthesis defers to the governance file and sits *under* it as workplan-supporting material.

---

## Part V — Comprehensive Workplan

Defers to `workplan/workplan-co0007-v3.md` (committed `3385209d`, 2026-04-26 01:53 UTC) which is the complete revised workplan incorporating all audit findings.

Brief structural summary follows; the workplan v3 file is canonical.

### Workplan structure

Four macro-stages now (was three). Each stage gates the next; outputs accumulate.

- **Stage 0: Verification and decision freeze.** 8–12 sessions. Verifies factual base; makes pre-Stage-A doctrinal decisions; establishes provisional mission. **(NEW per workplan v3)**
- **Stage A: Foundations.** 25–37 sessions. Thirteen governance documents binding all subsequent work; Co-1 recruitment thread initiated.
- **Stage B: Architecture and pilot.** 26–40 sessions. Working multi-pilot demonstrating end-to-end the structured form serves the mission.
- **Stage C: Migration and scaling.** 165–245 sessions. Complete project in structured form; audit-as-byproduct; ongoing time-handling.

The 2,259-commit corpus is **input** to Stages B and C. Existing artifacts are not "fixed"; they are migrated through a process that audits them as a byproduct.

### Stage 0 highlights (NEW per workplan v3)

| Phase | Sessions | Resolves | Status (this re-issue) |
|---|---|---|---|
| 0.1 Session protocol grounding | 1 | B-03 | ✓ committed |
| 0.2 Quantitative verification | 1–2 | B-01 | ✓ committed |
| 0.3 Skill inventory | 1 | B-04 | ✓ committed |
| 0.4 Contamination sampling | 1–2 | N-07 | ✓ committed |
| 0.5 Pre-Stage-A doctrinal decisions | 2–3 | T-03, T-04, D-03 | ✓ committed |
| 0.6 Provisional mission commit | 0.5 | T-01 | ✓ committed |
| 0.7 Synthesis + roadmap re-issue | 1 | L-01, L-02 | this file |
| 0.8 Repo strategy | 0.5 | — | ✓ committed (stay in `jordanelias/guidebook` `main`) |
| 0.9 Workplan adoption | 0.5 | — | pending |

### Stage A (corrected)

13 phases (was 8 in v1; A1-A2 merged per audit L-07; A9-A13 added). Output: 13 governance documents.

| Phase | Sessions | Resolves | Output |
|---|---|---|---|
| A1-A2 Audience + mission canonical (merged) | 4–6 | L-07, T-01, T-05, partial N-08 | `governance/audience-priority.md`; `governance/mission-and-epistemics.md` |
| A3 Conceptual model | 5–7 | T-06, T-07, N-03 | `governance/conceptual-model.md` |
| A4 Voice and framing | 2–3 | — | `governance/voice-and-framing.md` |
| A5 Co-1 relationship + recruitment thread | 5–7 + parallel cross-stage thread | D-03, N-06 | `governance/co1-coauthor-relationship.md`; `governance/co1-recruitment-plan.md` |
| A6 Evidence methodology | 3–5 | T-03 final, T-04 final, N-02, N-08, partial D-04 | `governance/evidence-methodology.md` |
| A7 Population taxonomy | 2–3 | — | `governance/population-taxonomy.md` |
| A8 Jurisdiction philosophy | 2–3 | jurisdiction disambiguation | `governance/jurisdiction-philosophy.md` |
| A9 Time model unification | 2–3 | L-04, D-05 | `governance/time-model.md` |
| A10 Adversarial-use review | 1–2 | — | `governance/adversarial-use-framework.md` |
| A11 Legal/regulatory framework | 1–2 + counsel | — | `governance/legal-regulatory.md` |
| A12 Decision proxy and capture | 1 | L-05 | `governance/decision-protocol.md` |
| A13 Doctrine-recheck cadence | 1 | B-06, partial D-04 | `governance/doctrine-recheck-cadence.md` |

### Stage B (corrected)

Multi-pilot construction (per audit N-09). Three pilot tracks span dimensions that matter for architecture validation:
1. Adequate-evidence parameter, adequate-corpus population (turning space + MOB + G-04 Wet Room)
2. Contested parameter, multi-population (lighting illuminance + NDV/AUT + MOB + OFS + B-08)
3. Sparse-evidence parameter, sparse-corpus population (acoustic privacy/RT60 + NDV/MH PTSD + A-13)

All three tracks operate against the same room (Bathroom + Lighting + Acoustics adjacencies) so room-level composition is also exercised.

| Phase | Sessions | Resolves |
|---|---|---|
| B1 Schema design with architectural derivation | 6–9 | N-05, partial L-04, D-05 |
| B2 Tooling design with expanded validator suite | 4–6 | T-02, T-06, N-04, D-02, D-04, D-05, T-03 |
| B3 Navigation mode specification | 3–4 | T-02, T-05, D-01 |
| B4 Multi-pilot construction | 8–12 | N-01, N-09 |
| B5 Pilot rendering with refresh policy | 3–4 | D-02 |
| B6 Pilot validation against mission | 4–5 | N-08 partial |
| B7 Architecture lock | 2 | — |

### Stage C (corrected)

C0 added (skill responsibility matrix). C2 expanded scope. C7 includes 81-source bibliography residual disposition (was 6%, now 14%).

| Phase | Sessions | Notes |
|---|---|---|
| C0 Skill responsibility matrix | 2–3 | NEW per audit L-03 / B-04 |
| C1 Migration tooling build | 4–6 | Time-handling integrated from this point onward |
| C2 Skill set rebuild | 12–16 | Skill-inventory note: per Stage 0.3, ~75 skill-tasks; budget may understate by ~50% — **flagged for 0.9 adoption decision** |
| C3 Migrate parameters | 30–40 | 60–80 atomic parameters (definition in A3) |
| C4 Migrate populations | 18–28 | 11 populations; gated on Co-1 corpus per population per A5 |
| C5 Migrate items and rooms | 30–45 | 92 items + room-set |
| C6 Migrate conflicts | 28–45 | 200–400 actual entries from 55 pairs × ~60 parameters |
| C7 Migrate evidence base | 12–17 | **584 sources / 81 unverified residual** (was 557/33 in v1 framing); per-source disposition per B-05 resolution |
| C8 Migrate jurisdictions | 8–12 | 49 codes / 112 pairs / temporal handling per A9 |
| C9 Cross-cutting prose migration | 20–30 | Parts 1–3, 5, 9, 10–12 in voice from A4 |
| C10 Quality gates and validation | 6–10 | Validators from B2 |
| C11 Maintenance lifecycle | 3–5 | Documents what's been live since C1 |

### Estimated total scope (corrected)

| Stage | Min | Max |
|---|---|---|
| Stage 0 | 8 | 12 |
| Stage A | 25 | 37 |
| Stage B | 26 | 40 |
| Stage C | 165 | 245 |
| **Total** | **224** | **334** |

| Real-world pace | Min | Max |
|---|---|---|
| 2 sessions/day intensive | ~4 months | ~5.5 months |
| 1 session/day sustained | ~7.5 months | ~11 months |
| Real-world (Co-1 cadence + parallelism + project-management overhead) | **15 months** | **24 months** |

The 12–18 month estimate from v1 was built on understated session counts. v2 commits to **15–24 months real-world** as the honest range. Recruitment alone may push the lower bound up — A5 recruitment thread takes weeks-to-months of clock time independent of session count.

---

## What is salvageable from existing work — revised per Stage 0.4

| Status | Items | Adjustment from v1 |
|---|---|---|
| **Fully reusable** | Research data (jurisdictional values, verified evidence sources, multilingual coverage, Co-1 corpus); ≥92% of evaluable BPC `best_practice_synthesis` fields (per 0.4 finding) | v1 said partly-contaminated; v2 says largely doctrinally aligned. **Migration is migration, not rebuild, for most BPS fields.** |
| **Reusable with adjustment** | Skill methodologies (structure intact; output target + synthesis logic change); validators (paradigm intact; code rewrites); voice work (partial; A4 may supersede); bibliography metadata for the 503 verified sources | Same as v1 |
| **Reusable conditionally** | BPC `best_practice_synthesis` fields where contamination sample shows ambiguous (~8% by 0.4 estimate) — flag for evidence backfill | NEW per 0.4 |
| **Pending Opus synthesis** | BPCs in STUB state (~7% by 0.4 estimate) — needs Opus pass per existing protocol | NEW per 0.4 |
| **Redirect / consolidate** | BPCs in MERGED state (~7% by 0.4 estimate) — redirect handling during migration | NEW per 0.4 |
| **Superseded** | A small minority of pre-2026-03-28 non-Opus-refreshed BPCs not in sample; Part 4 specs as currently framed; Appendix A tables as currently framed; prior CO-0007 audit workplan; the audit v1; workplan v2; this synthesis v1 | v1 listed BPC `best_practice_synthesis` here broadly; v2 narrows to "small minority not in sample" |
| **Open question** | `voice-style_SKILL.md` (depends on A4); 81-source unverified bibliography residual (depends on C7 disposition) | Per audit B-05 |

The v1 salvage matrix treated contamination as binary; v2 treats it as continuous (per 0.4) and identifies five disposition categories instead of three. This is the most operationally consequential change in the re-issue.

---

## Decision points the workplan defers to project owner — corrected

23 decision points (was 12 in v1; expanded per audit L-02 + workplan v3 expanded phase set):

| # | Phase | Decision | Status |
|---|---|---|---|
| 1 | precondition | Adopt synthesis (per Coda's mission-test) | **PENDING (this re-issue triggers fresh sit-with)** |
| 2 | 0.4 | Contamination ratio acceptance — does it change scope? | RESOLVED: 0% frankly contaminated; ~92% aligned. C-stage scope reduces. |
| 3 | 0.5 T-03 | Co-1 tier encoding | RESOLVED: Option B (`tier` + `evidence_type`) |
| 4 | 0.5 T-04 | Sparse-evidence behavior | RESOLVED: Hybrid state machine |
| 5 | 0.5 D-03 | Co-1 operational role | RESOLVED: Reviewer with Co-author trajectory |
| 6 | 0.8 | Repo strategy | RESOLVED: stay in `jordanelias/guidebook` `main` |
| 7 | 0.9 | Workplan adoption | **PENDING** |
| 8 | A1-A2 | Audience priority + use patterns | pending |
| 9 | A1-A2 | Mission language + epistemic commitments | pending (PROVISIONAL committed at 0.6) |
| 10 | A3 | Conceptual model + entity inventory + cross-cutting axes | pending |
| 11 | A4 | Voice selection | pending |
| 12 | A5 | Co-1 resourcing; per-phase role assignments; recruitment plan | pending |
| 13 | A6 | Co-1 tier encoding details; sparse-evidence implementation; values-criteria mechanism; pedagogy integration; epistemic defense | pending |
| 14 | A7 | Population taxonomy | pending |
| 15 | A8 | Jurisdiction philosophy + denominator glossary | pending |
| 16 | A9 | Time model selection | pending |
| 17 | A10 | Adversarial-use mitigation tactics | pending |
| 18 | A11 | Disclaimer language; licensing; trajectory positioning | pending |
| 19 | A12 | Decision protocol + standardized model-routing notation | pending |
| 20 | A13 | Doctrine-recheck cadence | pending |
| 21 | B1 | Storage form (12+ year implication) | pending |
| 22 | B2 | Build-vs-buy per tool | pending |
| 23 | B5 | Rendering refresh policy | pending |

Plus ongoing Co-1 collaborator decisions throughout, scoped per A5.

---

## Risks and mitigations — corrected

**Risk: scope optimism.** Mitigation: stage gating; if Stage A overruns budget, Stage B does not start. Stage 0 verification (already done) reduces this risk by replacing estimates with verified figures for Stage 0.1–0.4 inputs.

**Risk: Co-1 collaborator unavailability.** Mitigation: A5 explicitly addresses; trajectory clause (per D-03) decouples doctrine from operational reality; methodological-limit declaration is mission language (per `governance/mission-PROVISIONAL.md` §3).

**Risk: schema lock-in too early.** Mitigation: pilot validation (B6) designed to surface architectural problems before lock; iteration permitted. **B1 multi-form derivation (per N-05) ensures architecture is selected from candidates, not asserted.**

**Risk: existing work feels wasted.** Mitigation: 0.4 finding (~92% doctrinally aligned BPCs) substantially reduces this risk. Most existing work is migration-ready, not rebuild-required.

**Risk: project too large to finish.** Mitigation: each migrated parameter independently usable; value released incrementally.

**Risk: synthesis itself wrong.** Mitigation: Stage A includes audience priority + mission articulation as explicit decision points; this re-issue exists because v1 had verifiable errors. **The cycle works.**

**Risk (NEW): C2 budget understates by ~50%.** Mitigation per 0.3 finding: either revise C2 budget upward (12–16 → ~24 sessions) or defer some NEW skills (e.g., web-renderer, respect-visibility-renderer) to mid-Stage-C; flag for 0.9 adoption decision.

**Risk (NEW): bibliography residual tripled (33 → 81 sources).** Mitigation per 0.2 §M2: C7 budget revision (12–17 → 15–22 sessions) OR tighten disposition criteria (more "deprecate as unverifiable" relative to "re-verify").

---

## Coda

This re-issue exists because Stage 0 verification surfaced quantifiable errors in v1's quantitative claims and qualitative errors in v1's contamination framing. The corrections matter because downstream decisions reference upstream figures.

The substantive findings are: the corpus is healthier than v1 credited (no frank contamination); the bibliography residual is worse than v1 credited (81 sources, not 33); the architectural form was asserted prematurely (now derived in B1); the Co-1 doctrinal claim needed transparency about operational reality (now declared in mission); the time model + epistemic defense + questions-led pedagogy + design-stage axis were all under-operationalized (now phased explicitly).

The workplan adopts at 0.9. The mission has been committed PROVISIONAL at 0.6; the Coda's "sit with mission ≥1 day before adopting" test now operates on `governance/mission-PROVISIONAL.md` specifically. Adoption is the project owner's call.

The 15–24 month real-world horizon is honest. Recruitment cadence (A5), Co-1 review windows, and external counsel/architect input are the binding constraints; session count is not. The project is large because the mission is large and the existing corpus is substantial. Each migrated parameter is independently usable, so value is released incrementally.

The principle the project committed to in resolving 0.5: **clean data, transparent methodology**. v2 makes the data cleaner (verified figures, disambiguated denominators, explicit corpus states) and the methodology more transparent (declared Co-1 role, declared sparse-evidence state machine, declared encoding semantics, declared resource-honest declaration). v1 is superseded.

Roadmap re-issue (`co0007-roadmap-2.md`) is **deferred** to the next session: roadmap-1 was an artifact in earlier conversation state not committed to repo; without that file as the basis to revise from, a roadmap-2 re-issue would essentially restate Part V of this synthesis. The 0.7 phase is satisfied by this synthesis re-issue alone if you accept that disposition; otherwise flag and I'll produce a roadmap document de novo from workplan v3 in next session.
