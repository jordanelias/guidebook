# Workplan: Evidence Base Expansion Programme
**Created:** 2026-04-03
**Basis:** `misc/literature-review-proposal-2026-04-03.md` (commits b5a433e7, 4a79f36c)
**Track:** Independent of v10.5 assembly. Runs in parallel after Phase 0 complete.
**Model assignment:** Sonnet 4.6 (all search, extraction, drafting) · Opus 4.6 (all best_practice_synthesis — manual session)
**Principle:** Phase 0 gates everything. No searches until Phase 0 deliverables are committed.

---

## Programme Summary

| Phase | Label | Slugs / tasks | Sessions est. | Opus required |
|---|---|---|---|---|
| 0 | Prerequisites | 5 deliverables | 1–2 | No |
| 1-A | Thermoregulation | 1 new slug | 4–6 | Yes — after |
| 1-B | Sensory space (Global South) | 1 new slug | 4–6 | Yes — after |
| 1-C | Wayfinding (Global South) | 1 new slug | 4–6 | Yes — after |
| 1-D | Bathroom typology | 1 new slug | 4–6 | Yes — after |
| 1-E | Co-1 housing (Global South) | 1 new slug | 4–6 | Yes — after |
| 2 | CRPD monitoring integration | 1 new slug | 2–3 | Yes — after |
| 3-A | threshold-door-hardware expansion | existing slug | 2–3 | Yes — after |
| 3-B | pain-ofs expansion | existing slug | 2–3 | Yes — after |
| 3-C | acoustics expansion | existing slug | 2–3 | Yes — after |
| 3-D | dementia-residential expansion | existing slug | 2–3 | Yes — after |
| 3-E | intellectual-disability expansion | existing slug | 2–3 | Yes — after |
| 3-F | FDR-OFS-02 layout circuit | existing slug/FDR | 1–2 | No (FDR inline) |
| 4 | POE horizon slug | 1 new slug | 3–5 | Yes — after |
| Opus | Synthesis passes (all phases) | All above | Per phase | Opus 4.6 manual |

**Total session estimate:** 40–60 Sonnet sessions + Opus passes after each phase.
**Do not attempt to compress multiple phases into a single session.**

---

## Phase 0 — Prerequisites
**Gate:** All 5 deliverables must be committed to GitHub before any Phase 1 session starts.
**Estimated sessions:** 1–2
**Skills:** None (direct editing)

### P0-D1 — Change Order
**What:** Formal Change Order documenting jurisdiction register expansion (24 → 46) and language axis expansion (14 → 19).
**File:** `references/change-orders/CO-0005-evidence-expansion.md`
**Contents:** Rationale · Scope (jurisdictions added, languages added, slugs created) · Impact on existing BPC entries (none at P0; additive only) · Approval record
**Dependency:** None — do first.

### P0-D2 — Keyword Compendium update
**What:** Add Part 3 entries for 5 new languages: AR, HI, ID, SW, BN.
**File:** Multilingual keyword reference document (project files — locate via multilingual-research_SKILL.md §Pre-Run step 2)
**Contents per language:** 10 concept groups minimum matching existing language entries. Use proposal §2d terms as starting point — flag all as `[UNVERIFIED — native-speaker review pending]` until confirmed.
**Dependency:** P0-D1 approved.
**Note:** Do not execute any search using these terms until the UNVERIFIED flag is resolved. Flagged terms may be used for initial retrieval but must be marked provisional in the search-log.

### P0-D3 — multilingual-research_SKILL.md update
**What:** Add 22 new jurisdictions to Axis 2 of the skill file.
**File:** `skills/multilingual-research_SKILL.md`
**Contents to add:**
- Tier A jurisdictions (IN, ZA, MX, CL, CR, ID, BD, NG, PH, EG): Co-1 targets, Co-2 OT body, primary statutory standard, primary Tier 5 source — all drawn from proposal §5
- Tier B jurisdictions (KE, TH, CO, AR, PE, GT, EC, UY, MA, GH, TZ, ET): same fields, noting where targets are thin
- THIN/NOT-RUN flags for Caribbean and remaining LAC per proposal §5
**Dependency:** P0-D1 approved.

### P0-D4 — Gap register entries
**What:** Add GAP-LRP-01 through GAP-LRP-12 to `gap_register.md`.
**Format:** Standard gap register row format. Status: OPEN. Priority per proposal §5 table.
**Dependency:** P0-D1, P0-D2, P0-D3 committed.

### P0-D5 — Slug registry and directory stubs
**What:** Create stub entries in `references/slug-registry.md` for 7 new slugs:
1. `thermoregulation-built-environment` → `health-and-symptom-management/`
2. `sensory-space-global-south` → `sensory-environment/`
3. `wayfinding-global-south` → `wayfinding-and-signage/`
4. `bathroom-typology-global-south` → `bathrooms-and-wet-areas/`
5. `co1-housing-research-global-south` → `frameworks-and-methodology/`
6. `crpd-implementation-built-environment` → `frameworks-and-methodology/`
7. `post-occupancy-evaluation-global` → `frameworks-and-methodology/`

Create empty `references/search-log/{topic}/{slug}.md` and `references/bpc/{topic}/{slug}.md` stub files for each.
**Dependency:** P0-D1 through P0-D4 committed.

### P0 completion gate
Before opening any Phase 1 session, confirm:
- [ ] CO-0005 committed
- [ ] Keyword Compendium updated with UNVERIFIED flags
- [ ] multilingual-research_SKILL.md updated with all 22 jurisdictions
- [ ] GAP-LRP-01–12 in gap_register.md, all OPEN
- [ ] All 7 slug stubs committed

---

## Phase 1 — P1 Slugs (New)
**Rule:** One slug per session thread. Do not start Phase 1-B until Phase 1-A search is complete and intermediate checkpoint committed. Opus synthesis for each slug queued after LOG — do not wait for all Phase 1 slugs before queuing.

### Jurisdiction set for all Phase 1 slugs
All 46 jurisdictions (24 existing + 22 new). Existing 24 must be re-searched if the slug is new (no prior coverage). New 22 searched per §2 protocol.

### Language set for all Phase 1 slugs
All 19: SV · NO · DA · FI · FR · DE · ZH · JA · NL · ES · PT · KO · IT · EN + AR · HI · ID · SW · BN (last 5 flagged provisional pending P0-D2 verification)

---

### Phase 1-A — `thermoregulation-built-environment`
**GAP-LRP-01** · P1 · Populations: OFS · MST · TCOA · PAIN
**Rationale:** All current thermoregulation evidence (Uhthoff, Krupp, MCAS, EDS/OFS) is temperate-climate. Tropical/subtropical specifications for cooling, humidity, and passive ventilation are absent. Directly affects F-07 (HVAC/thermal), CON-0101, CON-0107.

**Session structure:**
| Session | Task |
|---|---|
| 1-A-1 | research-log-manager CHECK · Load keyword terms · Batch A (SV/NO/DA/FI) + Batch B (FR/DE/NL) · Checkpoint |
| 1-A-2 | Batch C (ES/PT/IT — priority LAC jurisdictions: MX/CL/CO/AR/PE/CR/EC/UY/GT) + Batch D (ZH/JA/KO) · Checkpoint |
| 1-A-3 | Batch E (EN jurisdictions: US/UK/CA/AU/IE/NZ/SG + ZA/NG/KE/GH/TZ/ET) · Checkpoint |
| 1-A-4 | Batch F (AR/HI/ID/SW/BN — new languages; flag provisional) · Targeted Co-1 pass: CBR networks, WHO Climate & Health, IPCC disability working groups · Checkpoint |
| 1-A-5 | Citation mining (all Tier 1–2 sources) · Synthesis · Pre-LOG completeness check · research-log-manager LOG |
| 1-A-6 (if needed) | Overflow: additional jurisdiction passes where THIN flagged at checkpoint |

**Priority database additions for this slug:** WHO IRIS (climate/disability), WPRIM, EMRO Index Medicus, IndMED

**Opus queue entry after LOG:**
```
SLUG: thermoregulation-built-environment
PRIORITY: P1
SYNTHESIS TASK: Climate-stratified best-practice table (tropical / subtropical / temperate / cold).
Identify where current F-07 and CON-0101/0107 specifications require climate-conditional variants.
```

---

### Phase 1-B — `sensory-space-global-south`
**GAP-LRP-02** · P1 · Populations: NDV · NDV-MH · DEM
**Rationale:** PAS 6463 (UK) dominates existing sensory-relief-space-design BPC. No non-Western evidence. Cultural variation in sensory norms, privacy, communal vs. private space, and low-resource implementation absent.

**Session structure:**
| Session | Task |
|---|---|
| 1-B-1 | CHECK · Keyword load · Batch A + B · Checkpoint |
| 1-B-2 | Batch C (LAC priority) + Batch D · Checkpoint |
| 1-B-3 | Batch E + African jurisdictions (ZA/NG/KE/GH/TZ/ET) · Checkpoint |
| 1-B-4 | Batch F (new languages) · Co-1 pass: DPI Japan, CDPF China, DPO India on sensory environments · ASEAN Disability Forum · Checkpoint |
| 1-B-5 | Citation mining · Synthesis · Pre-LOG check · LOG |

**Relationship to existing BPC:** New slug feeds into `sensory-relief-space-design` as supplementary evidence. Do not overwrite existing BPC entry — cross-reference from new slug.

**Opus queue after LOG:**
```
SLUG: sensory-space-global-south
PRIORITY: P1
SYNTHESIS TASK: Identify where PAS 6463 specifications transfer across climates and cultures,
where they require adaptation, and what genuinely alternative low-resource provision exists.
Flag any cultural consensus/divergence on privacy norms in sensory spaces.
```

---

### Phase 1-C — `wayfinding-global-south`
**GAP-LRP-03** · P1 · Populations: VIS · DEAF · DEM · IntD · DBL
**Rationale:** ISO 21542 is the only international reference in current wayfinding BPC entries. Indian HMIS, South African tactile standards, ASEAN signage guidance, ESCAP Incheon Strategy wayfinding provisions not retrieved.

**Session structure:**
| Session | Task |
|---|---|
| 1-C-1 | CHECK · Keyword load · Batch A + B · Statutory standards pass (Tier 6) for all 22 new jurisdictions — wayfinding/signage chapters · Checkpoint |
| 1-C-2 | Batch C (LAC) + Batch D · Checkpoint |
| 1-C-3 | Batch E + African/Asian new jurisdictions · Targeted Co-1: NAB India, Blind SA, Vision Nigeria, Deaf Philippines, FENASEC Ecuador · Checkpoint |
| 1-C-4 | Batch F · ESCAP Incheon Strategy §9 (wayfinding) direct retrieval · ASEAN Enabling Masterplan wayfinding provisions · Checkpoint |
| 1-C-5 | Citation mining · Synthesis · Pre-LOG check · LOG |

**Opus queue after LOG:**
```
SLUG: wayfinding-global-south
PRIORITY: P1
SYNTHESIS TASK: Identify specification convergence/divergence between ISO 21542,
existing BPC wayfinding entries, and Global South evidence.
Determine whether tactile ground surface indicators, auditory signals, and colour contrast
specifications require climate/substrate/maintenance variants for Global South contexts.
```

---

### Phase 1-D — `bathroom-typology-global-south`
**GAP-LRP-04** · P1 · Populations: MOB · OFS · TCOA · PAIN · NDV
**Rationale:** All bathroom/wet-area specifications assume Northern European enclosed bathroom. Tropical typologies (open-air wet rooms, floor-level drainage, squat fixture prevalence, split toilet/shower rooms) are unaddressed. Direct impact on Part 4 bathroom items.

**Session structure:**
| Session | Task |
|---|---|
| 1-D-1 | CHECK · Keyword load · Batch B (FR/DE/NL — partial relevance for wet-room norms) + Statutory pass for IN/ID/BD/PH/EG/MA bathroom accessibility provisions · Checkpoint |
| 1-D-2 | Batch C (LAC — Mexico/Colombia/Peru/Brazil wet-room typologies) + Batch D (JA/ZH/KO — squat fixture prevalence and accessibility) · Checkpoint |
| 1-D-3 | Batch E + ZA/NG/KE bathroom accessibility · AIOTA / IOTI / OTAP practice guidance retrieval · Checkpoint |
| 1-D-4 | Batch F (HI/AR/ID priority — squat fixture, wet-room terms) · WHO sanitation and disability cross-reference · Checkpoint |
| 1-D-5 | Citation mining · Synthesis · Pre-LOG check · LOG |

**Opus queue after LOG:**
```
SLUG: bathroom-typology-global-south
PRIORITY: P1
SYNTHESIS TASK: Classify bathroom accessibility specifications by typology
(enclosed Northern European / open-plan wet room / split facility / shared facility).
For each typology, determine: what transfers from existing BPC; what requires variant specification;
what has no evidence base (named gap). Climate and maintenance considerations explicit.
```

---

### Phase 1-E — `co1-housing-research-global-south`
**GAP-LRP-05** · P1 · Populations: All
**Rationale:** This is the primary Co-1 gap. CBR and participatory action research on housing barriers from Global South is entirely absent from all existing BPC entries. No lived-experience evidence from Global South disabled people. This slug is a Co-1 evidence bank — it feeds all other slugs, not a standalone design item.

**Session structure:**
| Session | Task |
|---|---|
| 1-E-1 | CHECK · PICO framing: population = disabled people in Global South housing contexts; outcome = functional independence, participation, identified barriers · Co-1 pass ONLY this session: SODIS Peru, ECDD Ethiopia, CCBRT Tanzania, Fundación Saldarriaga Concha, NCPEDP India, APDK Kenya, GFD Ghana · Checkpoint |
| 1-E-2 | CBR network literature: CBR Africa Network, CBR Asia-Pacific, WHO CBR Guidelines (5 components, housing chapter) · LILACS Co-1 retrieval · AJOL disability housing · Checkpoint |
| 1-E-3 | Batch C (ES/PT LAC participatory research) + Batch D (ZH/JA/KO — disability housing lived experience) · CRPD shadow reports from 10 priority new jurisdictions (IN/ZA/ID/PH/NG/CO/CL/MX/KE/EG) — Co-1 content only · Checkpoint |
| 1-E-4 | Batch F (new languages) · UNCRPD Committee Concluding Observations housing extracts (built environment, Article 9, Article 19 — all 22 new jurisdictions) · Checkpoint |
| 1-E-5 | Citation mining · Synthesis · Pre-LOG check · LOG |

**Special rule:** This slug has no Tier 6 (statutory code) dimension. Evidence hierarchy: Co-1 → Tier 2 → Co-2 → Tier 3. Do not anchor on standards. PICO outcome = barrier identification and barrier removal as reported by disabled people.

**Opus queue after LOG:**
```
SLUG: co1-housing-research-global-south
PRIORITY: P1
SYNTHESIS TASK: Identify the top 10 built environment barriers reported by disabled people
in Global South housing contexts. For each barrier: cross-reference to existing BPC slug;
determine whether existing specification addresses it, partially addresses it, or is silent.
Where silent: flag as P1 gap for targeted research. This slug is a gap-identifier, not
a specification source — synthesis output is a prioritised gap list, not a specification table.
```

---

## Phase 2 — CRPD Monitoring Integration
**GAP-LRP-11** · P2 · Slug: `crpd-implementation-built-environment`
**Rationale:** CRPD Article 9 Concluding Observations and shadow reports from all signatory states contain structured DPO evidence on built environment barriers. None integrated into current BPC.

**Session structure:**
| Session | Task |
|---|---|
| 2-1 | CHECK · OHCHR treaty body database: retrieve Article 9 Concluding Observations for all 22 new jurisdictions + existing 24 (where not already retrieved) · Classify: specific built environment finding vs. general accessibility statement · Checkpoint |
| 2-2 | DPO shadow report retrieval: CRPD Coalition reports for IN/ZA/CO/CL/MX/ID/PH + IDA (International Disability Alliance) Global South shadow report synthesis · Checkpoint |
| 2-3 | Synthesis: map each Concluding Observation finding to BPC slug · LOG |

**Output format:** Mapping table `CRPD Article 9 finding | Jurisdiction | Source tier | BPC slug affected | Current BPC status (addresses / partial / silent)`.

**Opus queue after LOG:** None — this is a mapping exercise, not a best-practice synthesis. Findings feed directly into P2 gap flags on existing slugs.

---

## Phase 3 — P2 Slug Expansions (Existing Slugs)

Each session expands an existing slug's jurisdiction coverage to include the 22 new jurisdictions. The existing 24-jurisdiction search-log entry is not re-run — only the new jurisdiction delta is added.

**Protocol per slug:**
1. research-log-manager CHECK — load existing log; identify which of the 22 new jurisdictions are NOT-RUN
2. Run targeted passes for NOT-RUN jurisdictions only
3. Pre-LOG check — existing jurisdiction fields remain; new fields appended
4. LOG with status update (PARTIAL → scope extended; new jurisdictions now SEARCHED or THIN)

| Sub-phase | Slug | GAP | New jurisdiction priority | Sessions |
|---|---|---|---|---|
| 3-A | `threshold-door-hardware` | GAP-LRP-06 | IN · EG · ZA · MA · NG | 2–3 |
| 3-B | `pain-ofs-built-environment-design` | GAP-LRP-07 | IN · ZA · MX · CO · CL · PE | 2–3 |
| 3-C | `acoustics-speech-intelligibility` (and `room-acoustic-performance`) | GAP-LRP-08 | IN · ZA · NG · KE · EG · ID | 2–3 |
| 3-D | `dementia-residential-design` (confirm slug name via registry) | GAP-LRP-09 | IN · ZA · MX · CO · AR · BR (expand) | 2–3 |
| 3-E | `intellectual-disability-design` (confirm slug name) | GAP-LRP-10 | IN · ZA · ID · PH · KE | 2–3 |
| 3-F | FDR-OFS-02 (residential layout circuit) | — | IN · ID · BD · NG · KE · CO · ZA | 1–2 |

**Opus queue after each 3-x LOG:** Add to opus-synthesis-queue.md with flag `EXPANSION — existing synthesis review required. Determine whether new evidence changes existing best_practice_synthesis or is additive only.`

---

## Phase 4 — POE Horizon Slug
**GAP-LRP-12** · P3 · Slug: `post-occupancy-evaluation-global`
**Execute after Phase 3 complete.** Session budget 3–5. Standard multilingual-research protocol. Priority databases: BDTD (Brazil), LILACS, AJOL, SciELO, WPRIM. Priority jurisdictions: IN · ZA · MX · CO · ID.

---

## Opus Synthesis Queue Additions

The following entries must be appended to `workplan/opus-synthesis-queue.md` at Phase 0 completion (not at search completion — register the intent now):

```
| thermoregulation-built-environment | P1 new | Climate-stratified specification table | After Phase 1-A LOG |
| sensory-space-global-south | P1 new | Cross-cultural sensory space transfer analysis | After Phase 1-B LOG |
| wayfinding-global-south | P1 new | ISO 21542 vs. Global South evidence convergence | After Phase 1-C LOG |
| bathroom-typology-global-south | P1 new | Typology-classified bathroom specification variants | After Phase 1-D LOG |
| co1-housing-research-global-south | P1 new | Gap prioritisation from Co-1 evidence | After Phase 1-E LOG |
| crpd-implementation-built-environment | P2 new | Mapping output only — no synthesis required | N/A |
| threshold-door-hardware | P2 expansion | Expansion review — additive or revision? | After Phase 3-A LOG |
| pain-ofs-built-environment-design | P2 expansion | Expansion review | After Phase 3-B LOG |
| acoustics-speech-intelligibility | P2 expansion | Expansion review | After Phase 3-C LOG |
| [dementia slug] | P2 expansion | Expansion review | After Phase 3-D LOG |
| [intellectual disability slug] | P2 expansion | Expansion review | After Phase 3-E LOG |
| post-occupancy-evaluation-global | P3 new | POE synthesis — what performs, what fails, what is unknown | After Phase 4 LOG |
```

---

## Gap Register Entries to Create at P0-D4

```
| GAP-LRP-01 | thermoregulation-built-environment | OFS · MST · TCOA | No tropical/subtropical climate evidence | P1 | OPEN |
| GAP-LRP-02 | sensory-space-global-south | NDV · NDV-MH · DEM | PAS 6463 dominates; no non-Western evidence | P1 | OPEN |
| GAP-LRP-03 | wayfinding-global-south | VIS · DEAF · DEM · IntD · DBL | ISO 21542 only; ASEAN/India/Africa absent | P1 | OPEN |
| GAP-LRP-04 | bathroom-typology-global-south | MOB · OFS · TCOA | Northern European typology only | P1 | OPEN |
| GAP-LRP-05 | co1-housing-research-global-south | All | Zero Global South Co-1 evidence in any BPC entry | P1 | OPEN |
| GAP-LRP-06 | threshold-door-hardware | MOB · VIS | US/UK/DE/AU only; MENA/South Asia/Africa absent | P2 | OPEN |
| GAP-LRP-07 | pain-ofs-built-environment-design | OFS · PAIN | High-income countries only | P2 | OPEN |
| GAP-LRP-08 | acoustics-speech-intelligibility | DEAF · DBL | Hearing loop infrastructure absent in Global South | P2 | OPEN |
| GAP-LRP-09 | [dementia slug] | DEM · TCOA | All evidence from high-income countries | P2 | OPEN |
| GAP-LRP-10 | [intellectual disability slug] | IntD | UK/AU/US only; no Global South evidence | P2 | OPEN |
| GAP-LRP-11 | crpd-implementation-built-environment | All | CRPD Concluding Observations not integrated | P2 | OPEN |
| GAP-LRP-12 | post-occupancy-evaluation-global | All | No POE studies from Global South in any BPC entry | P3 | OPEN |
```

---

## Relationship to v10.5 Workplan

This programme is **independent** of v10.5 Phase 5 (cross-reference-resolver + assembly). Phase 5 can proceed without waiting for this programme. However:

- New BPC entries from this programme will require a subsequent cross-reference pass before they can inform item specifications
- Any new best-practice synthesis findings that contradict existing item specifications in Parts 1–12 must be routed through the amendment process (CO required)
- FDR-OFS-02 (Phase 3-F) feeds Part 6 residential layout — if Phase 5 assembly completes before Phase 3-F, FDR-OFS-02 deferred findings must be incorporated via targeted amendment, not inline edit

---

## Session Protocol for Each Phase 1–4 Session

Every session:
1. State phase and session number (e.g., Phase 1-A, Session 2)
2. Load multilingual-research_SKILL.md (do not rely on memory)
3. research-log-manager CHECK before any search
4. Execute the session's assigned batches only — do not overrun into next session's batches
5. Commit checkpoint to GitHub at end of session
6. State: languages complete (N/19), jurisdictions complete (N/46), sources found (N)
7. Do not proceed to LOG until all 19 languages and all 46 jurisdictions have a recorded status

---

## Standing Rules (inherited from PI, restated for clarity)

- Sonnet never writes best_practice_synthesis. All synthesis: Opus queue.
- Sources confirmed real before inclusion. 2 failed searches → CLOSED-DELETED.
- THIN flag (not skip) where jurisdiction has no retrievable evidence after genuine attempt.
- RETRIEVAL-BLOCKED is distinct from THIN — use where language barrier prevents full-text access.
- Machine-translated retrieval: flag as `[MT]` in source list; do not treat as confirmed content.
- New language terms (AR/HI/ID/SW/BN): flag as `[UNVERIFIED]` until native-speaker review complete.
- All BPC entries from this programme carry `opus_synthesis: false` until Opus pass recorded.
