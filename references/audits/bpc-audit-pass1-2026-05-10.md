# BPC Audit — Pass 1 Findings (A–D)
**Date:** 2026-05-10
**Auditor model:** Opus 4.7
**Predecessor:** `references/audits/bpc-audit-pass0-2026-05-10.md` (committed `851545a`)
**Scope:** Pass 1 sub-passes A (PROVISIONAL deep-read), B (citation completeness), C (STUB downstream trace), D (cross-pop corridor conflict resolution).
**Status:** Pass 1 complete. No file commits except this audit document.

---

## Pass 1A — PROVISIONAL deep-read

Pass 0 §2.1 listed 16 PROVISIONAL files. 4 covered in Pass 0 §4. The 12 remaining read this pass. Two findings reverse Pass 0's classification.

### Pass 1A summary table

| File | Real status | Wheelchair-test verdict | Notes |
|---|---|---|---|
| `entrances-and-circulation/residential-entry-and-threshold.md` | PROVISIONAL — 11/24 jur NOT-RUN; **Co-1 0/24** | 🟡 | Power WC mentioned; bariatric/scooter/DEAF invisible. 850mm minimum door without "code-floor" disclaimer; 1500×1500 landing is code-floor. Best/minimum language correct for door, but no disclaimer that 850mm is below evidence-supported best for power WC + assistant configurations. |
| `entrances-and-circulation/threshold-and-level-access.md` | PROVISIONAL — 11/24 jur NOT-RUN; **Co-1 0/24** | 🟢 | Functional reasoning correctly tied to WC caster geometry (75mm typical caster cannot reliably navigate >6mm upstand). 13mm/15mm specifications anchored in physics, not code consensus. Direction-of-travel (DE reducing to 10mm) correctly noted as evidence of convergence to tighter standards. |
| `population-general/dementia-built-environment.md` | Tier 3–5; not actually PROVISIONAL (Pass 0 false positive — "PROVISIONAL" in body referenced other files) | 🟢 | Tier 3 systematic-review base (Marquardt & Schmieg 2009); quantified lighting (300/500 lux); cross-pop conflict with VIS named (complementary, not conflicting). Honest about the provisional aspects without flagging the whole BPC as such. |
| `population-general/intellectual-disability-built-environment-design.md` | PROVISIONAL — every spec carries `[TIER 4–5; no quantified architectural standard in any jurisdiction; March 2026]` | 🟢 (epistemic transparency) / 🟡 (existence question) | Per project-standards RULE 2026-03-25 (`IntD is not a standalone population code; provisions are proxied through DEM and NDV`), this BPC arguably should not exist as a population-general entry. Its content is correct in disclosing the absence of quantified architectural standards. Flag for governance review: should this BPC be retired in favour of cross-references in DEM and NDV BPCs? Currently retained as v9.0 interim with full review deferred to v10.0. |
| `population-general/mental-health-built-environment.md` | **PARTIAL — Phase 3 ready; not PROVISIONAL** (Pass 0 false positive — "PROVISIONAL" appeared in body as supersession marker `[OPUS-SYNTHESIS 2026-03-30 — supersedes PROVISIONAL 2026-03-18]`) | 🟢 EXEMPLAR | 57 Tier 1/Co-1 mentions. Trauma-informed design (TID) framework anchored in Tier 1: Husum 2010 (n=1,016 across 32 wards), van der Schaaf 2013 (n=23,868 across 199 wards), Faerden 2022 (Cohen's d=2.0 patient support, 1.7 staff support), Weltens 2023 (OR 5.36 overcrowding→aggression). DEAF cross-conflict named (open sightline vs predictable spatial sequence) with explicit conflict note. Should be cited as the template for Tier 1-anchored synthesis. |
| `health-and-symptom-management/pain-ofs-built-environment-design.md` | PROVISIONAL — 10/24 jur NOT-RUN; 7/14 languages | 🟢 (despite PROVISIONAL) | Synthesis is well-reasoned: PAIN warmth vs OFS cool conflict resolved per harm-asymmetry doctrine (default cool 18-21°C protects MS/SCI neurological harm; supplemental warmth for PAIN). Universal Mode candidates correctly qualified ("retreat room 500m² threshold and entrance seating 5m distance are Co-1/Co-2 derived — mark as Universal Mode CANDIDATE pending higher-tier validation"). Self-aware about the gap. **Pass 0 §2.2 STUB classification was wrong** — synthesis section is fully populated; the `[STUB ...]` markers I detected were in unrelated bullet points. Remove from STUB list. |
| `kitchens-and-workspaces/residential-kitchen-and-task-surfaces.md` | PROVISIONAL — 19/24 jur, tier5 8/24 | 🔴 | Specifies "ø1500mm turning" — same code-floor value as `accessible-circulation-geometry.md`. Bariatric (LPA) population mentioned but no QAS upgrade applied: no power-WC-accommodating turning value in the kitchen specification. Steinfeld 2006 RESNA 2400mm (entire-sample 180°) not invoked. **Same Convergence ≠ Evidence failure as the corridor BPC.** |
| `frameworks-and-methodology/co1-housing-research-global-south.md` | COMPLETE (Pass 1A initial regex false-negative — synthesis is at `## best_practice_synthesis` lowercase) | 🟢 | Co-1 Global South corpus; 30 confirmed sources; 20 Tier 1/Co-1 mentions. Honest about scope decision. Pass 0 §2.1 PROVISIONAL flag was based on body text reference, not file's own status. Reclassify. |
| `frameworks-and-methodology/cross-population-case-studies.md` | PARTIAL — 7 jurisdictions covered; academic pass complete; Co-1 partial; financial PROVISIONAL/GREY | 🔴 | **No `Best Practice Synthesis` section header found.** This BPC is structurally incomplete — exactly the file that should have resolved the corridor-width DEAF/NDV/DEM cross-population conflict (per Pass 0 §F-X1) but doesn't. Pass 1D (below) drafts the resolution that would have lived here. |
| `frameworks-and-methodology/residential-accessible-home-case-studies.md` | COMPLETE — Opus synthesis 2026-03-27 (regex false-negative — synthesis present at `## Best Practice Synthesis` line 339 + `### Best-practice synthesis` line 417) | 🟢 | 79 Tier 1/Co-1 mentions across 13 jurisdictions. Strong evidence base. Pass 0 §2.2 STUB classification was wrong (initial regex matched a stray bullet `[STUB...]` somewhere). Remove from STUB list. |
| `economics/accessibility-feature-market-value-uplift-framing.md` | PROVISIONAL — Opus 4.7 two-session run | 🟡 | Sophisticated three-channel analysis (supply-side relabeling, demand-side WTP, alternative-uplift channels). Quantified claim 🔴: "**60% revenue premium** for same physical care under 'village' architectural framing" (Avandell NJ vs US memory-care average). **Per RULE 2026-04-09 (economics BPC fabrication audit), this is exactly the high-risk pattern to verify.** Defer to Pass 1B citation-verifier next session. |
| `economics/case-study-economics-financial-data.md` | PARTIAL — Opus pending | 🔴 STUB synthesis | All four "Most..." fields and Opus note are `[STUB]`. 17/26 cases GREY; only 5 VERIFIED. Block use as evidence basis until Opus synthesis runs. |

### Pass 1A reclassification of Pass 0 §2.1 status flags

**Reclassify out of PROVISIONAL concern set:**
- `population-general/dementia-built-environment.md` — Pass 0 false positive
- `population-general/mental-health-built-environment.md` — Pass 0 false positive (supersession marker)
- `frameworks-and-methodology/co1-housing-research-global-south.md` — Pass 0 false positive
- `frameworks-and-methodology/residential-accessible-home-case-studies.md` — Pass 0 false positive

**Reclassify out of STUB concern set (Pass 0 §2.2):**
- `health-and-symptom-management/pain-ofs-built-environment-design.md` — STUB markers not in synthesis section
- `frameworks-and-methodology/residential-accessible-home-case-studies.md` — synthesis present

**Confirmed PROVISIONAL with substantive risk** (i.e. PROVISIONAL **and** wheelchair-test concerns):
- `entrances-and-circulation/accessible-circulation-geometry.md` (Pass 0 §4.1 — corridor)
- `entrances-and-circulation/residential-entry-and-threshold.md` (this pass)
- `kitchens-and-workspaces/residential-kitchen-and-task-surfaces.md` (this pass)
- `controls-and-hardware/reach-range-and-accessible-controls.md` (Pass 0 §4.4)
- `population-general/mobility-built-environment.md` (Pass 0 §4.2 — Steinfeld 2400mm gap)
- `population-general/intellectual-disability-built-environment-design.md` (existence question)
- `economics/accessibility-feature-market-value-uplift-framing.md` (high-risk quantified claims)
- `economics/case-study-economics-financial-data.md` (STUB)

**Substantive risk count: 8 BPCs.** Smaller than Pass 0's flag-count of 16. Of these 8, **5 share the corridor/turning code-floor pattern** (corridor, residential entry, kitchen, reach, MOB). That cluster is the audit's most-actionable wave: a single language convention + QAS application would address all 5 simultaneously.

---

## Pass 1B — Citation completeness (extreme-value verifications)

### Verified this pass
- **Steinfeld 2006 RESNA paper** — full text retrieved from `resna.org/sites/default/files/legacy/conference/proceedings/2006/Research/Outcomes/Steinfeld.html`. Confirmed: paper contains 1925mm (UDI 180° sub-sample), **2400mm (IDEA + BS8300 entire samples 180°)**, ~4200mm (UDI 360° all sides open). The 2400mm figure is real, peer-reviewed, in the same paper the bariatric BPC cites. **The bariatric BPC's selection of 1925mm over 2400mm from the same paper is a citation-completeness failure.**
- **DSDG / DeafSpace 2440mm corridor** — independently corroborated via Vaughn 2018 (DeafScape — Tier 2), Cloete & Rout 2025 (Acta Structilia scoping review — Tier 3), RIT InfoGuides, NEA blog, DesignWithDisabledPeopleNow.
- **IWA BPAG p.29** — confirmed direct quote: "powered wheelchair which requires a 1800mm turning circle" (Tier 2 DPO). 2300mm value found in IWA materials but is for *suspended sign clear headroom*, not turning.
- **Disability Scotland TAG (GCIL 2014) — turning circle = 1500mm** in kitchens. The 2200mm in the same document is a kitchen layout dimension, not turning. (Tier 2 DPO advocacy did not raise the turning value above code consensus.)

### Pending verification (deferred — research-log-manager LOG cycle required)
- **`Steinfeld 2010, n=500`** cited in `mob_pg.md` but the 2006 RESNA paper reports IDEA Center n=275. The 2010 reference may be a later book/report; needs independent retrieval to confirm: (a) reference exists, (b) sample size is genuinely 500, (c) whether it contains 2400mm or higher figures than the 2006 paper.
- **`Avandell NJ $12,000/month vs US memory-care average ~$7,500/month → 60% revenue premium`** in `accessibility-feature-market-value-uplift-framing.md`. Per RULE 2026-04-09 fabrication audit (3 instances caught in economics BPC), this is exactly the high-risk template. Need primary sources for both Avandell NJ pricing and "US memory-care average ~$7,500/month."
- **`van der Schaaf 2013 (n=23,868 across 199 wards)`** in mental-health BPC. Tier 1 effect-size claim deserves verification given high cross-cutting impact.
- **`Faerden 2022 Cohen's d = 2.0 patient support`** — Tier 1 effect size. Verify primary.
- **`Weltens 2023 OR 5.36 overcrowding→aggression`** — verify primary.

These deferred verifications form the Pass 1B continuation queue. Each requires `research-log-manager CHECK` first per standing rule #4.

### Pass 1B method note

Citation-verifier protocol per `skills/citation-verifier_SKILL.md` should run on the deferred items. The pattern that worked this pass — full-text fetch via web_fetch, exact-string verification of cited numbers, cross-check across independent sources — should be the default. The bariatric-BPC selective-quote pattern (cite the smaller value from a paper that also reports a larger value) is a specific failure mode worth grepping for: extract every paper cited in the corpus, check whether more-extreme values from those papers are also cited.

---

## Pass 1C — STUB downstream trace

Pass 0 §2.2 listed 10 STUB BPCs. Pass 1A reclassified 2 (`pain-ofs`, `residential-accessible-home-case-studies`) → 8 actual STUBs.

Searched `parts/v10/part03.md`, `part04.md`, `part05.md`, `part11.md` for slug references. Results:

| STUB BPC | Part 4 references | Risk | Action |
|---|---|---|---|
| `sensory-processing-model-design-application` | **2 mentions in part04.md** | 🔴 | Cited as evidence basis for Category A/F sensory specs (Source: CON-0040; sensory-processing-model BPC Opus synthesis). But the BPC's `Best-practice synthesis` section is `[STUB — pending Opus synthesis pass]`. Part 4 reader sees a citation suggesting evidence base; if they fetch the BPC the synthesis section is unfilled. |
| `sensory-relief-space-design` | **1 mention in part04.md** | 🔴 | Same pattern — cited as Opus-synthesis evidence basis but synthesis is STUB. |
| `upper-limb-impairment-built-environment` | **2 mentions in part04.md** | 🔴 | Cited as evidence basis for D2-30 (overhead ceiling specs): `Evidence: upper-limb-impairment-built-environment BPC; KITE Research structural load data.` Synthesis is STUB. |
| `ndv-aut-built-environment-quantified-thresholds` | 0 mentions | 🟡 | Not yet cited downstream — STUB resolution lower priority. But synthesis-scan-2026-05-06 §B-II-01 references this for RT60 ≤0.4s convergence; if that synthesis lands, the citation chain will break. |
| `school-environment-autism` | 0 mentions | 🟢 | No downstream impact. Lower priority. |
| `accessible-design-failures-poor-performance` | 0 mentions | 🟢 | No downstream impact. |
| `cross-population-conflict-resolutions` | 0 mentions | 🔴 (structural) | No mentions because it's STUB. **This is the structural gap that should resolve F-X1 (corridor-width DEAF/NDV/DEM conflict).** Currently no Part 4 / Part 5 spec can cite it because it doesn't exist. Pass 1D drafts the resolution. |
| `case-study-economics-financial-data` | 0 mentions | 🟡 | Economics-specific; verify part11 separately. |

**Pass 1C verdict (🔴):** Three STUB BPCs (`sensory-processing-model-design-application`, `sensory-relief-space-design`, `upper-limb-impairment-built-environment`) are actively cited as evidence basis in Part 4 specifications. Part 4 readers following the citation chain encounter `[STUB — pending Opus synthesis pass]` placeholders.

**Recommended remediation:**
1. **Priority STUB resolution queue:** these 3 BPCs first.
2. **Part 4 disclosure:** until the STUB synthesis is filled, every Part 4 citation to a STUB BPC should carry a `[BPC SYNTHESIS PENDING]` flag visible to the reader.
3. **Hook candidate:** Phase 2 hook (per `hook-workplan-guidebook.md`) — pre-commit check that no Part 4 spec cites a BPC whose `Best-practice synthesis` section is `[STUB...]`.
4. **`cross-population-conflict-resolutions` STUB** is the highest-stakes structural gap because it would resolve F-X1. See Pass 1D.

---

## Pass 1D — Cross-population conflict resolution: corridor width

The conflict (Pass 0 §F-X1):
- **DEAF** needs primary corridor 2440mm (Co-1, Tier 2-3) + glazed/unobstructed sightlines through corridor junctions (DSDG, Vaughn 2018, Cloete & Rout 2025).
- **NDV/MH** (PTSD anti-entrapment) needs predictable spatial sequence + retreat zones + no ambush points.
- **DEM** needs identifiable bounded corridor sections (loop plan; Marquardt & Schmieg 2009).
- **Existing position:** `accessible-circulation-geometry.md` says 1800mm primary; `deaf-spatial-design.md` says 2440mm primary; `deaf-acoustic.md` Opus note flags the conflict; `cross-population-conflict-resolutions.md` is STUB.

### Drafted resolution (for review, not commit)

**Reframe:** the apparent conflict largely dissolves under closer examination of what each population's evidence actually requires.

| Population | Spatial property required | Width-related? | Genuinely conflicts with 2440mm primary corridor? |
|---|---|---|---|
| DEAF | Width for two-signer side-by-side + glazed sightlines | Yes — needs 2440mm | — |
| NDV/MH (PTSD) | No ambush points, exit always visible, no blind corners | No — geometric/visual property, not width | **No** — glazed intersections are explicitly anti-ambush, not pro-ambush |
| DEM | Loop plan, identifiable bounded compartment sections, landmarks at decision points | No — topology + landmark, not width | **No** — bounded sections operate at building plan level, not corridor cross-section |
| MOB (general) | Two-WC passing 1525mm (ADA); 1800mm preferred (BS 8300); 2400mm Steinfeld 2006 entire-sample | Yes — 2440mm exceeds | **No** — wider value also satisfies narrower requirement |
| OFS / PAIN | Rest seating intervals 25–30m; recline-capable | No — width-independent | **No** — wider corridor allows more flexible seating placement |

**Draft Universal Mode rule for primary mixed-population corridors:**

> Primary mixed-population corridors to be ≥2440mm clear width with glazed (transparent or visually-permeable) intersections at all corridor junctions. Bounded compartmentation (residential clusters, retreat zones, sensory rooms) accessed FROM primary circulation, not within it. Loop-plan topology for DEM-populated environments preserves at building-plan level; corridor cross-section is independent of loop topology.

**Why this is not a corridor-width compromise:**
- 2440mm satisfies wheelchair-passing, two-signer conversation, and Steinfeld 2006 entire-sample turning evidence simultaneously.
- Glazed intersections satisfy DEAF visual sightline AND NDV/MH anti-ambush — these are the **same spatial property** described from two clinical perspectives, not opposing ones.
- DEM compartmentalisation operates at the building-plan level (which clusters are bounded), not corridor cross-section.
- Retreat zones (NDV/MH per `mental-health-built-environment.md`, sensory per A-16) are **off-corridor adjacent spaces**, not corridor-width-dependent.

**What the resolution does NOT solve:**
- Some DEM design literature (per `dementia-built-environment.md`) recommends "single-corridor or continuous-loop floor plan" — interpretable as implying a *narrow* defined corridor. This is a literature framing issue: the DEM clinical evidence (Marquardt & Schmieg 2009) is about *loop topology*, not corridor narrowness. The narrowness is a vestigial assumption, not a clinical requirement. Recommend the DEM BPC clarify this in its next synthesis revision.
- Cost: 2440mm primary corridor uses more floor area than 1800mm. This is a Mode-P trade-off (Mode P = the inclusive aspiration; Mode 6 / code = the floor). Per project doctrine, the cost-driven argument for narrower corridors is a Mode 6 argument, not a best-practice argument.
- Residential applications: domestic dwellings rarely have 2440mm corridors. The resolution applies to **non-residential and care/healthcare/educational settings** where mixed populations are anticipated. Single-occupancy domestic settings remain Mode S (occupant-co-designed).

### Recommended next action

This draft resolution should land in `references/bpc/frameworks-and-methodology/cross-population-conflict-resolutions.md` (currently STUB). Drafting the BPC body itself is a Stage C content task, not a Pass 1 audit task — flag for owner sign-off before authoring.

The resolution depends on:
1. Owner concurrence on the reframing (genuine conflict or apparent conflict?).
2. DEM BPC update to clarify "loop plan" vs "narrow corridor" distinction.
3. Cross-reference into `accessible-circulation-geometry.md` and `mobility-built-environment.md`.

---

## Pass 1 self-bias disclosure

**[SELF-AUTHORED — bias risk]** Pass 1 includes 4 reclassifications of my own Pass 0 findings (pain-ofs, mental-health, residential-accessible-home-case-studies, co1-housing-research-global-south). Pattern: my Pass 0 status-flag detection used regex matches that produced false positives when "PROVISIONAL" or "STUB" appeared in supersession notes or unrelated bullet contexts. The reclassifications go in the direction of **fewer concerns**, which would be flattering if I were marking my own work less critically. Cross-check: each reclassification is verifiable by direct read of the file (the Opus 4.6 supersession note in mental-health-built-environment.md, the lowercase synthesis header in co1-housing-research-global-south.md, etc.). The reclassifications are mechanical, not judgment-driven — but the under-detection in Pass 0 was real, and a future audit pass should re-examine the regex.

[BIAS: confirmation — basis: I'm motivated to find evidence the audit is making progress. Mitigation: the substantive findings remain and increased — F1, F2, F3, F-X1, F-X2, F-X3, F-X4, F-X5 from Pass 0 plus new STUB-downstream-citation finding from Pass 1C. The headline (corridor 2440mm; turning 2400mm Steinfeld; 17 BPCs with code-floor language; 3 STUBs cited as Part 4 evidence basis) is unchanged in direction; the reclassifications affect file-level concern flags, not the audit's substantive case.]

---

## Pass 1 limitations / what remains

- **Pass 1B verifications still owed:** Steinfeld 2010 n=500 confirmation; van der Schaaf 2013 n=23,868 confirmation; Faerden 2022 Cohen's d=2.0 confirmation; Weltens 2023 OR 5.36 confirmation; Avandell NJ $12k vs $7.5k pricing for the 60% framing-premium claim. All require research-log-manager CHECK/LOG cycle.
- **86 of 98 BPCs not deep-read at the wheelchair-test level.** Pass 1A covered 12 PROVISIONAL files. The remaining ~74 need application of the same QAS / wheelchair-test framework. Estimated 4–6 sessions.
- **Cross-population-conflict-resolutions BPC drafting** (Pass 1D output) is governance-level work, not audit. Owner sign-off needed.
- **STUB resolution priorities** (3 cited STUBs first) need Opus synthesis sessions per file. Sequence-decision is owner.
- **Hook Phase 2 candidate:** the "Part 4 cites a STUB BPC" check is mechanical — would be a strong Phase 2 hook. Pre-commit check that for every BPC referenced in Part 4 prose, the BPC's `Best-practice synthesis` does not begin with `[STUB`.
- **Tier-numbering inconsistency** (Pass 0 §F-X5) requires doctrine-recheck cadence trigger to resolve.
- **Voice-style review** (Pass 0 §F-X3 "aligned on best practice" pattern) deferred.
- **Adversarial-research re-application** to the Pass 1B verifications: not yet done.

## Proposed Pass 2 sequencing

1. **Pass 2A** — apply wheelchair-test + QAS to the 5 confirmed-substantive-risk PROVISIONAL files left from Pass 1A: residential-entry, kitchen, reach-range, MOB-general, accessibility-economics. Generate proposed remediation text (still no commits).
2. **Pass 2B** — citation-verifier on Pass 1B deferred items under research-log-manager protocol.
3. **Pass 2C** — propose draft `cross-population-conflict-resolutions` BPC using Pass 1D resolution as starting point, for owner sign-off.
4. **Pass 2D** — `BPC-cited-STUB` hook proposal for Phase 2 hook workplan.
5. **Pass 2E** — gap-filing in SQLite for accumulated Pass 0/1 findings.

Owner decides sequence.

---

**End Pass 1.**
