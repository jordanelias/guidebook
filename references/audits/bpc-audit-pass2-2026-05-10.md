# BPC Audit — Pass 2 Findings (A, C, D) + Handoff (B, E)
**Date:** 2026-05-10
**Auditor model:** Opus 4.7
**Predecessors:** `bpc-audit-pass0-2026-05-10.md` (`851545a`), `bpc-audit-pass1-2026-05-10.md` (`ba150fe`)
**Scope:** Pass 2A (remediation drafts for 5 PROVISIONAL files), Pass 2C (cross-population-conflict-resolutions BPC body draft), Pass 2D (Phase 2 hook proposal); Pass 2B and 2E handed off.
**Status:** Pass 2A/C/D complete; nothing committed to repo except this audit document. Drafted BPC text is proposal-only — owner sign-off required before the BPCs themselves are edited.

---

## Pass 2A — Remediation drafts (5 PROVISIONAL files)

Each draft is proposal text, not a commit. Each replaces a specific paragraph or table in the named BPC. Apply via `toc-editor` workflow if structural; via `str_replace` if textual; via Change Order if cross-references touched.

### 2A.1 `entrances-and-circulation/accessible-circulation-geometry.md` 🔴

**Current "Corridor clear widths" subsection** treats 1200mm non-residential single passage and 1525mm two-WC passing as valid alternatives. DEAF population invisible. Proposed replacement:

> **Corridor clear widths:**
>
> - **Code-floor values (Tier 6 — not best practice):** 915mm continuous single passage (ADA); 900mm residential single passage (DIN 18040-1, BS 8300); 1200mm non-residential single passage (UK Part M, DIN 18040-1); 1525mm two-WC passing (ADA). These are reference baselines only. Per `mobility-built-environment.md` pattern, code-floor values are cited here to record regulatory baselines, not as permitted design specifications.
> - **Tier 5 standards values:** 1800mm primary route two-way passing (BS 8300, DIN 18040-1, UK Part M non-residential best practice); 1500mm comfortable single passage for power-WC users; 1800mm power-WC passing. Adequate where DEAF population is not anticipated and only wheelchair-passing geometry governs.
> - **Tier Co-1 / Tier 2 / Tier 3 best practice (DEAF-inclusive primary corridors):** 2440mm primary corridors with glazed/transparent intersections (DSDG Bauman 2010 Co-1; DeafScape Vaughn 2018 Tier 2; Cloete & Rout 2025 Acta Structilia 32(2):238–263 Tier 3 cross-cultural scoping review). Required where signed conversation is anticipated; serves wheelchair-passing simultaneously. 1830mm (6 ft) acceptable on secondary corridors only. 3050mm (10 ft) public exterior pathways where signing groups anticipated.
> - **Tier 3 swept-path evidence:** Steinfeld 2006 RESNA reports 2400mm clear floor area to accommodate IDEA + BS8300 entire-sample 180° turn — converges with the DEAF 2440mm primary. Different evidence streams, same dimensional conclusion.
> - **Cross-population conflict** (DeafSpace open-plan vs NDV/MH compartmentalisation vs DEM loop-plan): resolved at the building-plan level, not corridor cross-section. Per `cross-population-conflict-resolutions.md` (pending — see Pass 2C draft below). Glazed intersections satisfy both DEAF visual sightline and NDV/MH anti-ambush requirements simultaneously.
>
> **Most inclusive provision:** Primary mixed-population corridors ≥2440mm clear width with glazed intersections; secondary corridors ≥1830mm; non-residential single-passage corridors where DEAF/scooter use not anticipated ≥1800mm two-way; residential single passage ≥1500mm power-WC clear. Code-floor values (915–1525mm) cited as regulatory baseline only, not specified as design targets.

**Also remove or recast** the divergent-findings table row "Corridor minimum non-residential | UK Part M (1200mm min; 1800mm two-way) | DE DIN 18040-1 (1200mm min; 1800mm recommended) | **Aligned on best practice; differ at minimum**" — the "aligned on best practice" wording is the F-X3 conflation. Recast as:

> Aligned on **code-consensus value of 1800mm two-way; 1200mm single-passage code floor**. Code consensus is not best practice per project-standards line 20. Best practice = 2440mm primary mixed-population per DEAF Co-1 evidence; 1800mm reflects pre-DEAF-evidence two-WC-passing convergence.

### 2A.2 `population-general/mobility-built-environment.md` 🟡

**The exemplar BPC** (Pass 0 §4.2). The single gap: Steinfeld 2006 RESNA's 2400mm IDEA + BS8300 entire-sample value not incorporated. Proposed addition to the **"Highest-ambition actionable specification" line:**

> **Current:** "Turning space ≥1800 mm diameter [Co-1/Tier 1 — IDeA Center / VA / Habinteg/RCOTSS]; 1700 mm acceptable where space-constrained..."
>
> **Proposed:** "Turning space ≥1800 mm diameter for typical power-WC accommodation [Co-1/Tier 2 — IWA BPAG p.29; Tier 5 — BS 8300-2 Annex G]; **2400 mm where IDEA + BS8300 entire-sample swept-path evidence governs (Steinfeld et al. 2006 RESNA, Tier 3 — peer-reviewed empirical anthropometry; figure represents IDEA Center n=275 + BS8300 sample 180° turn within enclosed bay).** 1925 mm acceptable where UDI sub-sample 180° methodology applies (open-ended bay; same paper, smaller sub-sample). 1700 mm acceptable where space-constrained..."

**Also clarify the "turning circle" framing per Pass 0 §F-X4:**

> Add Opus note: "All values above are *swept-envelope* clear floor areas measured by Steinfeld et al. and BS 8300 anthropometric studies, not idealised turning circles. They reflect what wheelchair users actually swept during 180° maneuvers in defined bays. Drive-system-dependent variation: mid-wheel-drive (MWD) power chairs swept-path closest to circle; rear-wheel-drive (RWD) and front-wheel-drive (FWD) power chairs require larger envelopes due to caster swing; scooters cannot pivot and require multi-point maneuver geometry. ADA T-shaped turning space (60" manual / 94" power per Section 304.3.2) is the standards-recognised alternative for spaces that cannot accommodate a circle."

**Also flag for citation verification (Pass 2B handoff):** the "Steinfeld et al. 2010, n=500" reference in the current BPC. The 2006 RESNA paper reports IDEA Center n=275, not n=500. The n=500 reference may be a different (later) Steinfeld publication; verify exists and contains the figures cited.

### 2A.3 `controls-and-hardware/reach-range-and-accessible-controls.md` 🔴

**Current banner** says "STATUS: PROVISIONAL — 16 jurisdictions NOT-RUN; Co-1 0/24; Tier 5 3/24. Do not use as sole basis for specification writing." But body asserts 400–1100mm reach zone authoritatively.

**Proposed reframe of the synthesis:**

> **Most inclusive provision:** All operable controls (switches, sockets, door hardware, intercoms, letterbox controls, security panels) within the reach zone 400–1100mm AFH. **The 1100mm upper bound is internally derived from clinical reasoning ("design should eliminate the need for trunk displacement") rather than direct Tier 1/Co-1 evidence; mark with ○. Co-1 evidence base is 0/24 — represents a gap at this scope.** The 1220mm side-reach maximum is Co-1-driven (LPA advocacy → ANSI A117.1 lowering from 1370mm) ●.
>
> **[GAP — REACH-Co1-COVERAGE]** Co-1 verification of the 1100mm constrained-user upper bound has not been performed in any of 24 jurisdictions. The value is plausible but not lived-experience-validated. Treat as Mode P starting point pending Co-1 work.

**Apply STATUS-banner consistency:** the banner says "do not use as sole basis"; the body should not write authoritative claims without disclosing the gap inline. Insert disclosure paragraph at top of synthesis:

> *Synthesis below derives from Tier 5–6 standards (3/24 jurisdictions Tier 5 confirmed) and Tier 1 force-threshold evidence (AAATE 2016, door force ≤30N at 94.7% WC user acceptance). Where claims rest on internal clinical reasoning rather than direct evidence, claims are marked ○ with the basis named. Pending Co-1 work, this BPC is not the sole basis for Part 4 specification writing.*

### 2A.4 `entrances-and-circulation/residential-entry-and-threshold.md` 🟡

**Current spec** has 850mm minimum door without code-floor disclaimer; 1500×1500mm landing as code-floor. **Co-1 0/24** is severe given residential entry is a high-Co-1-relevance domain.

**Proposed insertion (after current "Highest-ambition actionable specification"):**

> **Code-floor disclosure:** The 850mm door minimum is the CSA B651-23 code value for power-WC clear width (Tier 6). 900mm is the BS 8300 / DIN 18040-1 standards value (Tier 5). Power-WC + assistant configurations (assistant beside, not behind) require ≥1000mm clear per Habinteg Wheelchair Housing Design Guide 2018 (Tier Co-2 — RCOT/Habinteg authored). Where assistant-accompanied entry is anticipated, 900mm is sub-best-practice; specify ≥1000mm.
>
> **Landing 1500×1500mm** is the BS 8300 / DIN 18040-1 turning-circle-derived code-floor value. Per `mobility-built-environment.md` Steinfeld 2006 RESNA evidence (2400mm IDEA + BS8300 entire-sample 180° turn), and per IWA BPAG Tier 2 1800mm power-WC turning, residential entry landings sized to accommodate power-WC users should provide ≥1800mm × ≥1800mm clear of door arc. Specify 1500×1500 only as Mode 6 code-compliance fallback where space cannot be made.
>
> **[GAP — RES-ENTRY-Co1]** This BPC's Co-1 coverage is 0/24. Residential entry is a domain where lived-experience evidence is dense (entry frustrations recurrent in Co-1 corpora — see CRPD Article 9 implementation observations, IDA compilations). Co-1 work owed.

### 2A.5 `kitchens-and-workspaces/residential-kitchen-and-task-surfaces.md` 🔴

**Current spec** uses "ø1500mm turning" as Universal Mode kitchen turning. Same code-floor as `circ.md`. Bariatric (LPA) population mentioned but no power-WC upgrade.

**Proposed replacement of "Highest-ambition actionable specification" turning value:**

> **Current:** "...turning ø1500mm; sink ≤150mm depth..."
>
> **Proposed:** "...turning swept-envelope: 1800mm clear floor area for typical power-WC kitchen maneuver [Co-1/Tier 2 — IWA BPAG p.29; Tier 5 — BS 8300-2]; **2400mm where IDEA + BS8300 entire-sample evidence applies (Steinfeld 2006, Tier 3)**, particularly for kitchens serving bariatric or large-power-WC users. 1500mm code-floor turning circle (Tier 6) only where space cannot be made and Mode-S co-design assesses the user's specific chair geometry; not Universal Mode best practice for kitchens accommodating any power-WC user."

**Also** acknowledge LPA / bariatric: "Kitchens for users with large body habitus (LPA / bariatric configurations) require swept-envelope 1900mm minimum per VA Barrier-Free Design Standard 2025 Tier 5; Steinfeld 2006 reports 1925mm UDI for full sample 180° turn within open-ended bay (Tier 3)."

### 2A.6 `economics/accessibility-feature-market-value-uplift-framing.md` (Pass 2B handoff)

**Per RULE 2026-04-09** (economics BPC fabrication audit caught 3 fabricated quantified findings), this BPC's Channel 3a claim — `Avandell NJ: $12,000/month vs US memory-care average ~$7,500/month → 60% revenue premium` — is exactly the high-risk pattern. **Defer to Pass 2B** under research-log-manager `CHECK` / `LOG` protocol. Do not modify BPC body until citation verifier runs.

---

## Pass 2C — Draft body for `cross-population-conflict-resolutions.md`

Currently STUB. The drafted body below resolves Pass 0 §F-X1 (corridor-width DEAF/NDV/DEM conflict) plus three other cross-population conflicts surfaced by audit findings. Owner sign-off required before this lands as a BPC commit. Drafted in standard BPC format per `_template.md`.

---

```markdown
## cross-population-conflict-resolutions

**Updated:** 2026-05-10  **Original search:** 2026-05-10  **Evidence tier range:** Tier 1–Tier 3  **Opus synthesis:** YES [OPUS-SYNTHESIS-PROVISIONAL]
**Status:** PROVISIONAL — initial draft from BPC audit Pass 2C; covers 4 conflicts (corridor width; spatial enclosure; thermal default; lighting kelvin). Cross-population conflict registry from `synthesis-scan-2026-05-06.md` to be merged in next pass.

### Concept boundary notes
| Language | Native alias | Map | Warning |
|---|---|---|---|
| EN | cross-population conflict; harm-asymmetry resolution; broadest-benefit assessment | ✓ CLEAN | — |

### Best-practice synthesis

This BPC resolves spatial conflicts where two or more population codes have evidence-supported preferences on the same parameter. Resolution method per project-standards rule (RULE 2026-04-29 19:06 — values-based conflicts via broadest-benefit assessment; harm-asymmetry per RULE 2026-03-30 23:30):

1. Verify the conflict via Step-0 variable-conflation check (RULE 2026-03-30 23:30) — confirm the populations operate on the same physical variable.
2. If function-based (one population suffers physical harm from the wrong default): apply harm-asymmetry. Default protects higher-harm population; supplementary provision serves lower-harm population.
3. If values-based (no harm asymmetry): apply broadest-benefit assessment per evidence-methodology.md §4.

#### Conflict 1 — Corridor width: DEAF vs NDV/MH vs DEM

**Apparent conflict (per Pass 0 §F-X1):**
- DEAF Co-1/Tier 2/Tier 3 evidence (DSDG Bauman 2010; Vaughn 2018; Cloete & Rout 2025) requires ≥2440mm primary corridor width + glazed intersections for two-signer side-by-side conversation
- NDV/MH (PTSD) Tier 1 evidence (Faerden 2022; Wilson 2023) requires no ambush points, exit always visible, predictable spatial sequence
- DEM Tier 3 evidence (Marquardt & Schmieg 2009 systematic review) requires identifiable bounded compartment sections (loop plan, landmarks at decision points)

**Step-0 variable check:** the populations describe three different physical variables conflated as one:
- DEAF: corridor *cross-section width* (and intersection visibility)
- NDV/MH: *visual sightline geometry* (corner visibility from approach distance)
- DEM: *building plan topology* (loop / dead-end / bounded zones)

**Variables disambiguated, the conflict largely dissolves:**

| Population | Spatial property required | Conflict with 2440mm primary corridor + glazed intersections? |
|---|---|---|
| DEAF | Width 2440mm + glazed intersections | — (the recommendation) |
| NDV/MH (PTSD) | No ambush points + exit sightline | **No** — glazed intersections eliminate ambush; wider corridor reduces approach-distance escalation |
| DEM | Loop topology + bounded compartments + landmarks | **No** — operates at building plan level; corridor cross-section is independent |
| MOB power-WC | Two-WC passing 1525–1800mm | **No** — 2440mm exceeds requirement |
| MOB Steinfeld evidence | 2400mm 180° entire-sample swept-path | **No** — converges, not conflicts |
| OFS / PAIN | Rest seating intervals 25–30m | **No** — width-independent |

**Resolution (Universal Mode primary mixed-population corridors):**

> Primary mixed-population corridors to be ≥2440mm clear width with glazed (transparent or visually-permeable) intersections at all corridor junctions. Bounded compartmentation (residential clusters, retreat zones, sensory rooms) accessed FROM primary circulation, not within it. Loop-plan topology for DEM-populated environments preserves at building-plan level; corridor cross-section is independent of loop topology.

**Why this is not a corridor-width compromise:**
- 2440mm satisfies wheelchair-passing, two-signer conversation, and Steinfeld 2006 entire-sample 180° turning evidence simultaneously.
- Glazed intersections satisfy DEAF visual sightline AND NDV/MH anti-ambush — these are the same spatial property described from two clinical perspectives.
- DEM compartmentalisation operates at the building-plan level, not corridor cross-section.

**Residual divergence (not yet resolved):**
- Some DEM design literature recommends "single-corridor or continuous-loop floor plan" — interpretable as implying a *narrow* defined corridor. The DEM clinical evidence (Marquardt & Schmieg 2009) is about *loop topology*, not corridor narrowness. Vestigial framing assumption rather than clinical requirement. DEM BPC update owed: clarify "loop plan" ≠ "narrow corridor."
- Cost: 2440mm primary corridor uses more floor area than 1800mm. This is a Mode-P trade-off (best practice vs code floor). Cost-driven reductions are Mode-6 / Tier-7 arguments, not best-practice arguments.
- Residential applications: domestic dwellings rarely have 2440mm corridors. Resolution applies to non-residential / care / healthcare / educational settings where mixed populations are anticipated. Domestic single-occupancy → Mode S occupant-co-designed.

**Synthesis approach:** convergent (variables disambiguated; same physical recommendation satisfies all populations).

#### Conflict 2 — Thermal ambient default: PAIN vs MS / SCI / NEU

**Per RULE 2026-04-07 00:22 + RULE 2026-04-09:** PAIN (FMS) requires warmth (cold pain hypersensitivity); MS / SCI / NEU require cool ambient (Uhthoff phenomenon at >22°C; SCI tetraplegia thermoregulation impairment).

**Step-0 variable check:** same physical variable (ambient temperature). Variables not conflated.

**Harm-asymmetry analysis:**
- MS Uhthoff: neurological deterioration is irreversible / potentially permanent; recovery requires cooling and time
- SCI tetraplegia: heat stroke risk in severe cases (Tier 1 — clinical neurology evidence)
- FMS warmth-relief: pain symptom (reversible; not progressive); warmth provides relief but absence does not produce harm equivalent to MS deterioration

**Resolution (per `pain-ofs-built-environment-design.md` and `thermoregulation-built-environment.md`):**

> Default ambient temperature 18–21°C (cool default protects MS / SCI / NEU higher-harm populations). Individual local warmth provision for FMS / PAIN occupants (heated seating, radiant panel, additional clothing insulation) as supplementary provision. Where individual control is unavailable, default-cool prevails over default-warm.

**Synthesis approach:** divergent (genuine disagreement on default value); resolved by harm-asymmetry; both populations served via default + supplementary provision.

#### Conflict 3 — Spatial enclosure: DeafSpace open-plan vs NDV/SENS retreat / DEM compartmentation

**Apparent conflict (per `deaf-acoustic-built-environment.md` Opus note):** DeafSpace 2440mm + glazed = visually permeable / open spatial gestalt; NDV/SENS retreat = enclosed bounded zones; DEM compartmentation = bounded loop sections.

**Resolved via Conflict 1 above:** primary circulation is open + glazed; retreat / bounded zones are *adjacent off-corridor spaces*, not corridor functions. The "open vs bounded" frame applies to *zone type within the building*, not to the corridor itself.

**No genuine conflict** at the corridor level. Conflict at the building-plan level is resolved by zoning: primary circulation (open + glazed) + retreat zones (enclosed + acoustically-isolated) + compartments (bounded clusters).

#### Conflict 4 — Lighting Kelvin temperature: VIS / DEM warm vs DEAF / NDV cool

**[FORWARD-FLAGGED — not resolved this draft]** Multiple populations have lighting-kelvin preferences: VIS warm (3000K) for low-glare reading; DEM warm 2700–3000K for evening orientation; DEAF cool 4000–5000K for sign-language facial-expression contrast; NDV/SENS user-controllable. Resolution method: time-of-day variable lighting + user-control. To be resolved in next pass — out of scope for this draft.

### Consensus findings

| Finding | Languages with evidence | Tier |
|---|---|---|
| Variable conflation produces apparent conflicts that dissolve under disambiguation | EN | Methodological — project-standards RULE 2026-03-30 23:30 |
| Harm-asymmetry governs divergent function-based conflicts | EN, DE, NO, FR (proxied via clinical literature) | 1–3 |
| Glazed corridor intersections serve both DEAF visual sightline and NDV/MH anti-ambush | EN | Co-1 / Tier 2 (DSDG; Faerden 2022 inferred) |
| DEM loop plan operates at building-plan topology, not corridor cross-section | EN | Tier 3 (Marquardt & Schmieg 2009 reinterpreted) |

### Divergent findings

| Topic | Position A | Position B | Cause |
|---|---|---|---|
| Corridor width primary | 1800mm BS 8300 (wheelchair-passing) | 2440mm DSDG (two-signer) | Population evidence base differs (DEAF Co-1 not consulted in BS 8300 development) |
| DEM "single-corridor or continuous-loop" interpretation | Narrow defined corridor | Loop topology with any cross-section | Vestigial framing assumption in design literature; no Tier 1 evidence for narrowness specifically |

### NO-DATA / THIN

| Domain | Reason |
|---|---|
| Co-1 cross-cultural validation of 2440mm | DSDG ASL-derived; BSL/DGS/LSF/LIS/Auslan spatial grammars not measured |
| Cost-benefit Mode-P primary corridor 2440mm vs 1800mm | No published lifecycle costing |
| Loop-plan topology + 2440mm interaction with DEM cohort outcomes | No POE comparing 1800 vs 2440 within loop-plan facilities |

### Citation mining

| Source | Direction | New sources added |
|---|---|---|
| Cloete & Rout 2025 | Backward | DSDG Bauman 2010 (already in deaf-spatial-design BPC) |
| Marquardt & Schmieg 2009 | Cross-ref | Already in dementia-built-environment BPC |
| Steinfeld 2006 RESNA | Cross-ref | Pending IDeA Center 2010 publication retrieval (Pass 2B handoff) |

### Key sources

| REF-ID | Authors | Year | Title | Tier | Jurisdiction | Notes |
|---|---|---|---|---|---|---|
| XPC-01 | Bauman, H-D. | 2010 | DeafSpace Design Guidelines (Gallaudet) | Co-1 / Tier 2 | US | Cross-ref deaf-spatial-design BPC |
| XPC-02 | Cloete, M. & Rout, M. | 2025 | DeafSpace in built school environment: scoping review. *Acta Structilia* 32(2):238–263 | 3 | INT/ZA | Cross-cultural validity |
| XPC-03 | Steinfeld, E., Maisel, J. L., Feathers, D. | 2006 | Wheeled Mobility Space Requirements and Maneuvering: International Comparison. *RESNA 2006 Proceedings* | 3 | US/UK/AU/CA | 2400mm IDEA + BS8300 180° entire sample |
| XPC-04 | Marquardt, G. & Schmieg, P. | 2009 | Dementia-Friendly Architecture: Environments that Facilitate Wayfinding in Nursing Homes. *Am J Alzheimers Dis Other Demen* 24(4):333–340 | 3 | DE | Loop plan topology |
| XPC-05 | Faerden, A. et al. | 2022 | [Cited in mental-health-built-environment BPC] — patient-control RCT, Cohen's d = 2.0 | 1 | NO | Cross-ref MH BPC; verify primary per Pass 2B |
| XPC-06 | van der Schaaf, P. et al. | 2013 | Multivariate analysis 199 wards n=23,868 (cited in MH BPC) | 1 | NL | Verify primary per Pass 2B |
| XPC-07 | Project standards RULE 2026-04-29 19:06 | 2026 | Values-based broadest-benefit assessment | (governance) | INT | Project doctrine |
| XPC-08 | Project standards RULE 2026-03-30 23:30 | 2026 | Harm-asymmetry resolution; Step-0 variable conflation check | (governance) | INT | Project doctrine |

### Bottom-up findings

None this draft — placeholder for FDR-derived cross-pop interactions per `synthesis-scan-2026-05-06.md` (separate session).

## Metadata

```yaml
slug: cross-population-conflict-resolutions
population: ALL
last_updated: 2026-05-10
co0006_migration: true
status: PROVISIONAL
audit_provenance: bpc-audit-pass2-2026-05-10
covers: corridor-width-deaf-ndv-dem; thermal-default-pain-ms; spatial-enclosure-deafspace-retreat; (forward-flagged) lighting-kelvin
```
```

---

## Pass 2D — Hook proposal: `bpc-stub-cited-by-part4`

Add to `hook-workplan-guidebook.md` Phase 2.

**Hook ID:** `bpc-stub-cited-by-part4`
**Enforcement level:** 4 (Code hook with RuntimeError per architecture spec §"Enforcement spectrum")
**Trigger:** pre-commit on any change to `parts/v10/part04*.md`, `parts/v10/part05*.md`, `parts/v10/part06*.md`, `parts/v10/part07*.md`, or any file in `references/bpc/`.

**Logic:**

```python
# scripts/check_bpc_stub_citation.py
import re, sys, os, glob
from pathlib import Path

BPC_DIR = Path('references/bpc')
PART_DIR = Path('parts/v10')
STUB_RE = re.compile(r'\[STUB[^\]]*\]', re.IGNORECASE)

# 1. Identify STUB BPCs (synthesis section contains [STUB...])
stubs = set()
for bpc in BPC_DIR.rglob('*.md'):
    if bpc.name in {'index.md', '_template.md'}: continue
    content = bpc.read_text()
    syn = re.search(r'#{2,4}\s*Best.?practice\s*synthesis(.+?)(?=\n#{2,4}\s|\Z)',
                    content, re.IGNORECASE | re.DOTALL)
    if syn and STUB_RE.search(syn.group(1)):
        stubs.add(bpc.stem)

# 2. For each Part 4/5/6/7 file, scan for citations of STUB slugs
violations = []
for part in PART_DIR.glob('part0[4-7]*.md'):
    content = part.read_text()
    for stub in stubs:
        if stub in content:
            for line_n, line in enumerate(content.split('\n'), 1):
                if stub in line:
                    violations.append((part.name, line_n, stub, line.strip()[:120]))

if violations:
    print("VIOLATION: Part file cites BPC whose synthesis is STUB", file=sys.stderr)
    for p, n, s, l in violations:
        print(f"  {p}:{n}: cites '{s}' (BPC synthesis is STUB)", file=sys.stderr)
        print(f"    {l}", file=sys.stderr)
    sys.exit(1)
sys.exit(0)
```

**Failure code:** `BPC_STUB_CITED_BY_PART`
**Bypass:** PR modifying the script + ADR.
**Phase 1 dependency:** none (independent of frontmatter / commit-format hooks).

**Justification:** Pass 1C found 3 cases of this pattern in current corpus (`sensory-processing-model-design-application`, `sensory-relief-space-design`, `upper-limb-impairment-built-environment`). The hook prevents regression after each STUB is resolved.

---

## Pass 2 self-bias disclosure

**[SELF-AUTHORED — bias risk]** The Pass 2A drafts and the Pass 2C cross-pop BPC body are *my proposed text* for the project's BPCs. Two specific risks:

1. **The Pass 2C BPC body resolves F-X1 with a draft I authored.** The "convergent — variables disambiguated" framing is plausible but rests on my reading of how DEM clinical evidence actually maps onto corridor geometry. A DEM specialist might disagree with the claim that "loop plan" doesn't imply narrowness. Marquardt & Schmieg 2009 needs primary-source re-read to confirm whether they specify cross-section width or only topology. Defer to citation verification + DEM-domain review.

2. **Drafted text uses categorical voice in places ("to be ≥2440mm").** Per project-standards RULE 2026-04-26 19:25 (specification voice tier-located), categorical "shall be / to be" is retired except for code-citation contexts. The drafts above largely use "to be" in synthesis statements that should follow the Mode P pattern: "[Tier evidence] supports [value]." Flagged for prose-style-checker run before the BPC text actually lands.

[BIAS: I want the audit to deliver actionable remediation — basis: the user has been pushing for action. Mitigation: every draft is labelled "proposal-only — owner sign-off required"; nothing is committed except this audit document. Drafts can be discarded without project-state change.]

---

## Pass 2B handoff — citation verification queue

**Hand off to fresh session under `research-log-manager CHECK` / `LOG` protocol** per standing rule #4. Each item below is a discrete verification task; load via `python3 scripts/db.py coverage --slug <slug>` before retrieving primary sources.

### High-priority queue (Tier 1 effect-size claims with cross-cutting dependencies)

| # | Claim | Source as cited | Verify | Risk if wrong |
|---|---|---|---|---|
| **2B.1** | "Steinfeld et al. 2010, n=500" (in mob_pg.md) | Likely IDeA Center book/report 2010 | (a) reference exists at n=500; (b) contains 2400mm 180° turn figure or higher; (c) sample composition documented | mob_pg's foundational citation; if wrong, the whole "1500/1700/1800 ladder" loses its Tier 1 anchor |
| **2B.2** | "van der Schaaf 2013, n=23,868 across 199 wards" (in mental-health BPC) | Cited as Tier 1 | (a) primary paper retrievable; (b) sample sizes match; (c) "private space per patient" effect size as claimed | MH BPC's most-cited Tier 1 anchor; multiple Part 4 citations downstream |
| **2B.3** | "Faerden 2022, Cohen's d = 2.0 patient support" (in mental-health BPC) | Tier 1 RCT | (a) primary paper retrievable; (b) effect size d=2.0 actually reported; (c) intervention vs control description | High-effect-size claim; per RULE 2026-04-09 high-risk pattern |
| **2B.4** | "Weltens 2023, OR 5.36 overcrowding→aggression" (in mental-health BPC) | Tier 1 | (a) primary paper retrievable; (b) OR 5.36 actually reported; (c) what threshold defines "overcrowding" | OR claim; verify exact value not paraphrased |
| **2B.5** | "Avandell NJ $12,000/month vs US memory-care average ~$7,500/month → 60% revenue premium" (in accessibility-feature-market-value-uplift-framing) | Per RULE 2026-04-09 highest-risk fabrication template | (a) Avandell NJ pricing primary source; (b) "US memory-care average ~$7,500/month" source; (c) is the "60% premium" calculation 12000/7500=1.6 ratio actually attributed in the source? | Economics BPC, prior fabrication history; this is exactly the pattern flagged 2026-04-09 |

### Method note

For each: (1) `db.py coverage --slug <slug>` first; (2) web-fetch primary source; (3) text-search exact numbers in primary; (4) document outcome in search-log; (5) `db.py log-mining` per `research-log-manager_SKILL.md` §LOG. If unverifiable after 2 search attempts, mark `[UNVERIFIED-QUANT]` per project-standards rule (2026-04-09).

---

## Pass 2E handoff — gap-filing in SQLite

**Hand off to fresh session.** Each accumulated finding from Pass 0/1/2 needs `db.py add-gap` invocation per `evidence-auditor_SKILL.md` §5 logging conventions. Total: ~14 gap entries.

### Gaps to file

| # | Description | Category | Priority | Skill | Section |
|---|---|---|---|---|---|
| 2E.01 | Corridor 2440mm DEAF best-practice not cited in `accessible-circulation-geometry.md` (Pass 0 §F1 / 4.1) | AUDT | P1 | bpc-auditor | accessible-circulation-geometry |
| 2E.02 | Steinfeld 2006 2400mm IDEA + BS8300 entire-sample 180° turn not cited in `mob_pg.md` or `bariatric-turning-radius` BPC (Pass 0 §F2 / 4.2 + Pass 1B) | AUDT | P1 | citation-verifier | mobility-built-environment |
| 2E.03 | Reach BPC 1100mm constrained-user upper bound is internally derived ○; Co-1 0/24 (Pass 0 §4.4) | EG | P2 | research-log-manager | reach-range-and-accessible-controls |
| 2E.04 | DEAF population structurally invisible in 5 circulation/wayfinding BPCs (Pass 0 §S6.1 / 3.1) | AUDT | P1 | guidebook-auditor | (cross-cutting) |
| 2E.05 | Internal contradiction between `circ.md` (1800mm) and `deaf-spatial-design` (2440mm) corridor (Pass 0 §F-X1) | AUDT | P1 | bpc-auditor | (cross-cutting) |
| 2E.06 | 17 BPCs use code-floor values without rejection language (Pass 0 §F-X2) | AUDT | P2 | bpc-auditor | (cross-cutting) |
| 2E.07 | "Aligned on best practice" linguistic pattern conflates convergence with evidence (Pass 0 §F-X3) | AUDT | P2 | guidebook-auditor | (cross-cutting) |
| 2E.08 | Geometry framing failure — "turning circle" assumes pivot (Pass 0 §F-X4) | EG | P1 | guidebook-auditor | (cross-cutting) |
| 2E.09 | Tier numbering inconsistency: project-standards vs guidebook-auditor SKILL (Pass 0 §F-X5) | AUDT | P1 | doctrine-recheck | governance |
| 2E.10 | 3 STUB BPCs cited as evidence basis in Part 4 (Pass 1C) | AUDT | P1 | bpc-auditor | (cross-cutting) |
| 2E.11 | Co-1 0/24 in `residential-entry-and-threshold` (Pass 1A) | EG | P2 | research-log-manager | residential-entry-and-threshold |
| 2E.12 | Kitchen turning 1500mm code-floor; no power-WC upgrade (Pass 1A) | AUDT | P2 | bpc-auditor | residential-kitchen-and-task-surfaces |
| 2E.13 | IntD BPC existence question per RULE 2026-03-25 (Pass 1A) | EG | P3 | guidebook-auditor | intellectual-disability-built-environment-design |
| 2E.14 | Avandell-NJ 60% revenue premium claim per RULE 2026-04-09 high-risk template (Pass 1A / 2B.5) | AUDT | P1 | citation-verifier | accessibility-feature-market-value-uplift-framing |

### Method per evidence-auditor SKILL.md §5

```bash
# Example for 2E.01:
python3 scripts/db.py add-gap \
  --category AUDT \
  --priority P1 \
  --description "DSDG 2440mm primary corridor not cited in accessible-circulation-geometry.md best-practice synthesis; DEAF population structurally invisible from circulation BPC. See bpc-audit-pass0-2026-05-10.md §F1." \
  --skill bpc-auditor \
  --section accessible-circulation-geometry \
  --session bpc-audit-2026-05-10
# Repeat for 2E.02 through 2E.14
# Then: python3 scripts/db.py gaps --status OPEN  # confirm 14 inserted
# Then: commit DB
```

---

## What this audit deliberately did NOT do

- **Modify any BPC, Part 4 prose, or other project-content file.** All audit outputs are diagnostic + draft proposals committed to `references/audits/` only. Per `<workflow>` and project-standards on Change Order requirements: any structural change requires `toc-editor` workflow + Change Order, which is owner-driven.
- **File the gaps in SQLite.** Hand-off to Pass 2E. The gap categorisation should be confirmed by owner before bulk insertion.
- **Run citation-verifier on the Pass 2B queue.** Hand-off. These need rigour that won't survive my current context state.
- **Apply the Pass 1D resolution to the DEM BPC** (clarify "loop plan" vs "narrow corridor"). Owner-level domain decision.
- **Adjudicate the IntD BPC's existence question.** Per project-standards RULE 2026-03-25 — IntD provisions proxy through DEM and NDV. Owner decision whether to retire `intellectual-disability-built-environment-design.md` or retain as v9.0 interim. Pass 1A flagged but did not resolve.

## Audit provenance summary

| Pass | Date | Artifact | Commit | Lines |
|---|---|---|---|---|
| 0 | 2026-05-10 | `references/audits/bpc-audit-pass0-2026-05-10.md` | `851545a` | 527 |
| 1 | 2026-05-10 | `references/audits/bpc-audit-pass1-2026-05-10.md` | `ba150fe` | 184 |
| 2 | 2026-05-10 | `references/audits/bpc-audit-pass2-2026-05-10.md` | (this commit) | (see below) |

## Substantive finding count

| Code | Topic | Pass |
|---|---|---|
| F1 | Corridor width: code-consensus default mislabelled | Pass 0 §4.1 |
| F2 | Lift dimensions: same pattern, smaller magnitude | Pass 0 §4.1 |
| F3 | Corridor reasoning structurally excludes DEAF and bariatric | Pass 0 §4.1 |
| F-X1 | Internal contradiction: corridor width across BPCs | Pass 0 §5 |
| F-X2 | 17 BPCs with code-floor language | Pass 0 §5 |
| F-X3 | "Aligned on best practice" linguistic conflation | Pass 0 §5 |
| F-X4 | Geometry framing: "turning circle" assumes pivot | Pass 0 §5 |
| F-X5 | Tier numbering inconsistency | Pass 0 §5 |
| Pass 1C | 3 STUB BPCs cited as Part 4 evidence | Pass 1 §1C |
| Pass 1A | 5 confirmed PROVISIONAL files with substantive risk | Pass 1 §1A |
| QAS turning | Steinfeld 2006 2400mm not in corpus | Pass 0 §0.1 |
| Convergence ≠ Evidence | Methodological rule formalised | Pass 0 §0 |
| Largest-source / QAS | Method formalised | Pass 0 §0 + §0.1 |

---

**End Pass 2.**
