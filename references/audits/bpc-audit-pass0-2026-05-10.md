# BPC Audit — Pass 0 Findings
**Date:** 2026-05-10
**Auditor model:** Opus 4.7 (per system context; UI-set)
**Scope:** Full mechanical pass over all 98 BPC files in `references/bpc/`; deep read of 11 diagnostic files.
**Method:** Multi-surface audit per project-standards line 20 ("best practice ≠ code consensus") and the convergence-≠-evidence corollary added this session.
**Status:** Pass 0 of an N-pass audit. Findings are stage-bounded; no commits this pass.

---

## 0. Audit thesis (recap)

Project-standards line 20 (locked Core Doctrine 2026-04-24):

> Best practice means the most accommodating, thoughtful, respectful, dignified, and usable condition achievable for the disabled person… **A BPC `best_practice_synthesis` that derives its value solely from code consensus is in error.**

**Sharpened this session — Convergence ≠ Evidence:** Most-cited / highest-convergence indicates how many sources agree. It does not establish what is best for the disabled person. A converged value qualifies as best practice only if at least one of the following holds:

1. A Tier 1 / Co-1 source directly supports it as best for the population, OR
2. A Tier 2 / Co-2 source (DPO advocacy or OT CPG) explicitly recommends it as accommodating, OR
3. A Tier 3 systematic review concludes it is supported,

**AND** no higher-tier source recommends a more accommodating value for any reasonable in-population sub-segment.

If the only basis is "N standards agree on this number," the value is a **code-consensus default**, not best practice. It must be relabelled as such.

**Largest/most-extreme principle:** For each numerical specification, the audit identifies the source reporting the **largest / most accommodating / most extreme** value relevant to the population (especially the most-functionally-limited reasonable user). When the BPC selects a smaller value, the gap must be justified by Tier 1/Co-1 evidence or flagged as a code-consensus default.

**Operationalisation — Quantitative Ascending Search (QAS):** for each numerical parameter:
1. Start at the BPC's current value.
2. Search for evidence at incrementally higher values: +100mm, +200mm, +300mm…
3. At each increment, accept the value as a candidate best-practice if a **Tier 3 or better** source supports it for the population. Tier 3 or better = Tier 1 (OT clinical research), Co-1 (lived experience), Tier 2 (NGO/DPO advocacy), Co-2 (OT CPG), or Tier 3 (systematic reviews / meta-analyses + OT body guidelines). Tier 4 (international standards), Tier 5 (national beyond-code), and Tier 6 (codes) **never raise the ceiling**.
4. Stop when **N consecutive increments return no Tier 3+ support** (suggested N=2).
5. The highest value with valid Tier 3+ support becomes the audit's evidence-supported upper bound.

Starting from the BPC's value and asking "is it best?" is biased toward confirmation. Starting from successively higher values and asking "does evidence support this?" is biased toward finding the ceiling. The latter is what the project's doctrine actually requires.

[ASSUMPTION: tier numbering follows project-standards line 17 (Tier 3 = systematic reviews; locked Core Doctrine 2026-04-24). The guidebook-auditor SKILL.md uses a slightly different numbering (Tier 3 = OT CPG, Tier 4 = systematic review, Tier 7 = statutory code). This inconsistency is itself an audit finding — see §F-X4 below.]

---

## 0.1 QAS run — wheelchair turning circle (worked example)

Performed this pass for the canonical parameter the user flagged. Method: name every BPC value in the corpus, then web-search Tier 3+ sources for incrementally higher values until two consecutive increments return nothing.

### In-corpus values (descending)
| Source | Tier | 180° turn / circle | Notes |
|---|---|---|---|
| ESKEH/Invalidiliitto (FI) outdoor | 6 | 2500 mm | National code — does NOT qualify for QAS |
| Steinfeld 2006 RESNA (UDI 360° turn, all participants, sides open) | 3 | ~4200 mm | "Few participants or devices with very poor turning ability"; caveated; not a representative target |
| **Steinfeld 2006 RESNA (IDEA + BS8300 entire samples, 180° turn)** | **3** | **2400 mm** | **NOT cited in any BPC. Same paper as bariatric BPC's 1925mm citation.** |
| Steinfeld 2006 RESNA (UDI sub-sample, 180° turn, open-ended) | 3 | 1925 mm | Cited in `bariatric-turning-radius` BPC; UDI methodology allowed lengthening turn to reduce width — caveated |
| VA Barrier-Free Design Standard 2025 | 5 | 1830 mm | Bariatric care; federal standard |
| BS 8300-2 Annex G (UK) | 5 | 1800 mm | Power WC accommodation; Tier 5 |
| **IWA BPAG Edition 4 (2020) p.29** | **2 (DPO)** | **1800 mm** | Direct quote: "powered wheelchair which requires a 1800mm turning circle" |
| RHFAC CA / BS 8300 UK | 5 | 1700 mm | Acceptable where space-constrained |
| Disability Scotland TAG (GCIL 2014) | 2 (DPO) | **1500 mm** | DPO advocacy did NOT raise the value above code |
| ADA, DIN, NBR, KR 편의증진법, AS 1428.1, BFS, NZS 4121, GB 50763 | 6 | 1500–1525 mm | Code floor; rejected by mob_pg as "regulatory lag" |

### QAS sweep at +100mm increments above 1925mm
Search: "wheelchair turning circle 2000mm anthropometric study" / "turning radius 2100mm" / "turning circle 2200mm power wheelchair" / "turning 2300mm wheelchair" / "turning 2400mm" / "turning 2500mm"

| Increment | Tier 3+ support found? | Notes |
|---|---|---|
| 2000 mm | No specific Tier 3+ support at exactly this value | Various code/standard mentions; nothing peer-reviewed at this exact value |
| 2100 mm | No specific Tier 3+ support | |
| 2200 mm | No specific Tier 3+ support | User-supplied claim; not located in Disability Scotland TAG (which states 1500mm turning) or IWA BPAG (which states 1800mm turning). The 2200mm in Disability Scotland TAG is a **kitchen layout dimension** not turning. |
| 2300 mm | No specific Tier 3+ support | The 2300mm in IWA materials (Great Outdoors guide) is **suspended sign clear headroom**, not turning circle. |
| **2400 mm** | **YES — Steinfeld 2006 RESNA, Tier 3** | "IDEA and BS8300 results demonstrated that turning area clearances would have to be increased to 2400 mm (94.5 in.) compared to the current 1500-1525 mm (60 in.) to accommodate **their entire samples**." This is the same paper bariatric BPC already cites for the 1925mm UDI sub-sample. |
| 2500 mm | Tier 6 only (FI ESKEH outdoor) — does not qualify | |
| 2600 mm | No Tier 3+ found | |
| 2700 mm | No Tier 3+ found | Stop after 2 consecutive misses post-2400 (2500=Tier-6-only counts as miss; 2600=miss). |

### QAS verdict — wheelchair turning circle 180°

**Evidence-supported upper bound: 2400 mm (Steinfeld 2006 RESNA, Tier 3).**

This is the figure to accommodate the **entire IDEA + BS8300 samples** for a 180° turn. It is:

- 600 mm larger than the BPC's "best practice" of 1800 mm (`mobility-built-environment.md`, `accessible-bathroom-and-grab-bar.md`)
- 475 mm larger than the bariatric BPC's 1925 mm cited from the same paper
- 875 mm larger than ADA/AS/DIN/NBR code floor of 1500–1525 mm

The 1925 mm UDI sub-sample value currently in the corpus has methodological caveats noted in the source paper itself ("ends of turn open, allowing participants to lengthen out their turn and reduce its width"). The 2400 mm IDEA + BS8300 figure does not carry that caveat. Both are from the same paper. The corpus selectively cites the smaller value.

### Recommended remediation

1. **`mobility-built-environment.md` ladder revision:** add a "to accommodate entire sample" tier above the current 1800 mm best-practice ceiling, citing Steinfeld 2006 RESNA's 2400 mm figure for 180° turn. Frame as: "Universal Mode upper bound where space permits, supported by Tier 3 anthropometric evidence."
2. **`bariatric-turning-radius-built-environment.md` correction:** restore the 2400 mm figure that was selectively omitted. Currently the BPC cites only "1925 mm required to accommodate full UDI sample" but the same paper says 2400 mm to accommodate the **IDEA + BS8300 entire samples**. The BPC's own description ("the evidence-informed recommendation for bariatric-specific turning space in new build") understates what the paper actually supports.
3. **Cross-reference:** all turning-circle specifications should reference both the 1500 mm code floor (rejected per mob_pg pattern), the 1800 mm IWA/BS 8300 power-WC value, the 1925 mm UDI 180° figure (with methodological caveat), and the 2400 mm IDEA + BS8300 entire-sample figure. The BPC reader should see the full range from Tier 6 floor to Tier 3 ceiling, not just the code-consensus default.

### What was NOT found

- The user-supplied "2200 mm" claim for power WC turning is not directly supported by any Tier 3 source located this pass. The Disability Scotland TAG 2200 mm is a kitchen clear-space dimension (not turning); IWA BPAG explicitly states 1800 mm for power WC turning. If a Tier 3+ source for 2200 mm specifically exists, it has not been located in this pass — request from owner.
- Citation discrepancy: `mob_pg.md` cites "Steinfeld et al. 2010, n=500" but the 2006 RESNA paper (which contains the 2400 mm finding) reports IDEA Center n=275. The "Steinfeld 2010, n=500" reference may be a different publication (possibly the IDeA Center book) that I have not independently verified. **Citation-verifier task** — confirm "Steinfeld 2010, n=500" exists, retrieve it, check if it contains the 2400 mm figure.

### What the QAS values actually measure (geometry note — see F-X4 below)

The Steinfeld 2006 figures are **empirical swept-path measurements** taken with 3D digital probe + video of real wheelchair users executing turns in defined enclosures. They are not idealized turning circles. Specifically:

- The 1925 mm UDI 180° figure was measured with **open-ended bays** allowing participants to lengthen the turn — UDI users selected a less-tight maneuver geometry; the 1925 mm reflects the swept width with that optimization
- The 2400 mm IDEA + BS8300 180° figure was measured with **enclosed turning areas** — the value reflects the swept width when the user could not lengthen the turn
- The 4200 mm UDI 360° figure was measured with **all sides open**; the paper notes "at least one power wheelchair user required a much larger clearance"

This means the 2400 mm value is the more conservative (larger envelope) Tier 3 figure for accommodating a 180° turn within an enclosed space — closer to the actual design condition in a corridor or room. See F-X4 for the broader implications of geometry vs. swept path.

---

## 1. Surface S1 — Structural validation

| Outcome | Count |
|---|---:|
| PASS | 71 |
| FAIL | 0 (clean) |
| EXEMPT (frozen flat / merged stub / stub-not-run / deferred-non-standard) | 23 |
| SKIPPED (NON_BPC_FILENAMES) | 4 |
| **Total .md in `references/bpc/`** | **98** |

`validate_bpc.py` logic applied across the corpus produces zero structural failures on the in-scope set. The 2 flagged in my first sweep (`economics-sources.md`, `government-grant-programmes.md`) are `NON_BPC_FILENAMES` per the production validator — informational, not hallucinated, not BPCs.

**Finding S1.1 (informational):** structural integrity is currently clean. Phase 1 hooks (per `hook-workplan-guidebook.md`) targeting frontmatter-schema and citation-format will tighten this further; until then, validator at level-3 is sufficient.

---

## 2. Surface S2 — Status-flag distribution (non-exempt files)

| Status flag | Count | Notes |
|---|---:|---|
| `OPUS-SYNTHESIS` | 58 | Healthy — most BPCs have an Opus pass |
| `NO-DATA` flag (jurisdictional gap) | 57 | Expected — multilingual coverage incomplete |
| `[GAP-XXX]` reference | 28 | Linked into gap_register / SQLite |
| **`PROVISIONAL`** | **16** | High-stakes BPCs in this set; see §2.1 |
| `COMPLETE` | 13 | Structural completion |
| `[THIN-BASE]` | 12 | Disclosed evidence weakness |
| **`STUB`** | **10** | Best-practice-synthesis sections missing or placeholder; see §2.2 |
| `OPUS-PARTIAL` / `PROVISIONAL-RETAINED` | 9 | Opus synthesis with explicit caveats unresolved |
| `DEFERRED` | 6 | |
| `[UNVERIFIED]` | 5 | Per-claim flags |
| `MERGED` | 2 | Redirect stubs |

### 2.1 PROVISIONAL files of immediate concern

These BPCs are flagged PROVISIONAL but contain values being treated as guidebook policy — usable for Part 4 spec-writing only with explicit caveats. Each is a wheelchair-test risk site:

| File | PROVISIONAL why | Audit risk |
|---|---|---|
| `entrances-and-circulation/accessible-circulation-geometry.md` | Status: PARTIAL (PROVISIONAL); turning circle deferred to MOB BPC; Co-1 partial | **F1 (Convergence≠Evidence) on corridor; F2 (DEAF invisible).** See §4.1. |
| `population-general/mobility-built-environment.md` | "PROVISIONAL" appears in body re: ranges; status COMPLETE for jurisdiction coverage | F3 — bariatric/Steinfeld-2006 1925mm not incorporated. See §4.2. |
| `controls-and-hardware/reach-range-and-accessible-controls.md` | **STATUS: PROVISIONAL — 16 jurisdictions NOT-RUN; Co-1 0/24; Tier 5 3/24. Do not use as sole basis for specification writing** | Self-disclosed; nonetheless makes strong claims. See §4.4. |
| `entrances-and-circulation/residential-entry-and-threshold.md` | OPUS-PARTIAL + PROVISIONAL | Not yet examined this pass — flagged for next pass |
| `entrances-and-circulation/threshold-and-level-access.md` | OPUS-PARTIAL + PROVISIONAL | Flagged |
| `population-general/dementia-built-environment.md` | PROVISIONAL | Flagged |
| `population-general/intellectual-disability-built-environment-design.md` | PROVISIONAL | Flagged (IntD is also non-standalone code per RULE 2026-03-25) |
| `population-general/mental-health-built-environment.md` | PROVISIONAL | Flagged |
| `population-general/ndv-aut-built-environment-quantified-thresholds.md` | PROVISIONAL + STUB | See §2.2 |
| `health-and-symptom-management/pain-ofs-built-environment-design.md` | OPUS-PARTIAL + PROVISIONAL + STUB | High-stakes — pain/OFS values are evidence-thin per project-standards rule on EXPERT CONSENSUS disclosure |
| `kitchens-and-workspaces/residential-kitchen-and-task-surfaces.md` | OPUS-PARTIAL + PROVISIONAL | Flagged |
| `frameworks-and-methodology/co1-housing-research-global-south.md` | PROVISIONAL | Flagged |
| `frameworks-and-methodology/cross-population-case-studies.md` | PROVISIONAL | Flagged |
| `frameworks-and-methodology/residential-accessible-home-case-studies.md` | PROVISIONAL + STUB | Flagged |
| `economics/accessibility-feature-market-value-uplift-framing.md` | PROVISIONAL | Per RULE 2026-04-09, economics BPC was caught with 3 fabricated quantified findings; treat with extra skepticism |
| `economics/case-study-economics-financial-data.md` | PROVISIONAL + STUB | Flagged |

### 2.2 STUB files — best-practice-synthesis sections unfilled

These files exist as scaffolding but the synthesis content is placeholder. Any Part 4 specification citing these is unsupported until the synthesis is written:

- `frameworks-and-methodology/accessible-design-failures-poor-performance.md`
- `frameworks-and-methodology/cross-population-conflict-resolutions.md`
- `frameworks-and-methodology/residential-accessible-home-case-studies.md`
- `health-and-symptom-management/pain-ofs-built-environment-design.md` (best-practice section has `[STUB — see synthesis content above]` placeholders)
- `population-general/ndv-aut-built-environment-quantified-thresholds.md` (synthesis is `[STUB — pending Opus synthesis pass]`)
- `population-general/upper-limb-impairment-built-environment.md`
- `sensory-environment/school-environment-autism.md`
- `sensory-environment/sensory-processing-model-design-application.md`
- `sensory-environment/sensory-relief-space-design.md`
- `economics/case-study-economics-financial-data.md`

**Finding S2.1 (🟡):** The audit should not derive any best-practice claim from these 10 files until their synthesis sections are populated.

**Finding S2.2 (🔴):** `pain-ofs-built-environment-design.md` and `ndv-aut-built-environment-quantified-thresholds.md` are STUB **and** referenced by Part 4 specifications (e.g. RT60 ≤0.4s sourcing per synthesis-scan-2026-05-06 §B-II-01). Specs sourcing them are at minimum carrying THIN-BASE / EXPERT-CONSENSUS evidence weight that is currently undisclosed in the source BPC. Cross-check Part 4 attribution chain in next pass.

---

## 3. Surface S6/S7 — Population invisibility

### 3.1 The DEAF-invisible-circulation pattern

12 of 98 BPCs mention sign language, signers, or DeafSpace. The other 86 do not. Most of the 86 are correctly out-of-scope (acoustics, controls, thermal). But several should mention DEAF circulation needs and currently do not. The most damning:

| File | Should mention | Current state |
|---|---|---|
| `entrances-and-circulation/accessible-circulation-geometry.md` | Corridor width for two-signer conversation (Tier Co-1: 2440mm DSDG) | **Zero mention.** Corridor synthesis reasons entirely about wheelchair passing. |
| `population-general/mobility-built-environment.md` | Cross-reference to DEAF circulation requirements | Zero mention. |
| `wayfinding-and-signage/wayfinding-cognitive-science-spatial-design.md` | Visual sightlines + glazed corner principle from DSDG | Zero mention. |
| `wayfinding-and-signage/wayfinding-dementia-spatial-design.md` | Glazed-corner conflict with DEM compartmentalisation | Zero mention. (`deaf-acoustic-built-environment.md` Opus note correctly identifies this conflict but only from the DEAF side.) |
| `frameworks-and-methodology/cross-population-conflict-resolutions.md` | DEAF-vs-NDV/DEM spatial conflict | STUB |

**Finding S6.1 (🔴 — top-priority):** The DEAF population is **structurally invisible** in the corridor-width specification chain. The accessible-circulation-geometry BPC's "best practice 1800mm" treats the wheelchair-passing population as the entire population of interest. The deaf-spatial-design BPC says 2440mm primary; the deaf-acoustic BPC's Opus note even names this as a cross-population conflict; the circulation BPC reports neither the figure nor the conflict.

This is the canonical Convergence ≠ Evidence failure. 1800mm has high convergence across UK BS 8300, DE DIN 18040, NL care-setting standards (Tier 5–6). Tier Co-1/Tier 2 evidence specific to DEAF users supports 2440mm primary / 1830mm secondary. The BPC selects the converged value.

### 3.2 Other population-invisibility patterns to verify in next pass

- **Bariatric in general MOB**: `mobility-built-environment.md` mentions IDeA Center / power WC / scooter but does NOT cross-reference `bariatric-turning-radius-built-environment.md` (1925mm Steinfeld 2006). Bariatric is not a main-taxonomy code per RULE 2026-03-29 (BAR confined to Supplementary Volume), but the dimensional research it yields applies to large power WCs.
- **DBL in primary-routes specs**: DeafBlind users need both DEAF visual sightline AND VIS tactile wayfinding. Present in `population-general/deafblind-built-environment-design.md` but cross-ref into circulation/wayfinding BPCs not verified.
- **NDV/MH retreat from circulation**: The conflict between DeafSpace open-plan and NDV/MH compartmentalisation is identified once (deaf-acoustic Opus note) but no cross-population resolution exists (the cross-population-conflict-resolutions BPC is STUB).

---

## 4. Surface S2 deep-dive — diagnostic BPCs

### 4.1 `entrances-and-circulation/accessible-circulation-geometry.md` 🔴 — MULTIPLE FINDINGS

**Status:** PARTIAL (PROVISIONAL); OPUS-PARTIAL.

#### F1 — Corridor width: code-consensus default mislabelled "best practice"

**What the BPC says (lines 34–38, 51):**

> Single wheelchair passage: ≥915mm continuously (ADA); ≥900mm (DIN 18040-1/BS 8300 residential); ≥1200mm non-residential.
> Two wheelchair users passing: ≥1525mm (ADA); ≥1800mm (UK Part M non-residential best practice; care settings standard).
> Best practice for primary routes: 1800mm minimum…
> Power wheelchair users: ≥1500mm for comfortable single passage; ≥1800mm for passing.
>
> **Most inclusive provision:** … 1800mm corridor width on primary routes…

**Audit verdict:**

| Value | Source | Tier | Status |
|---|---|---|---|
| 1200mm non-residential single | UK Part M, DE DIN 18040-1 | Tier 6 | Code floor — NOT best practice |
| 1525mm two passing | ADA | Tier 6 | Code floor |
| 1800mm primary best practice | BS 8300, DIN 18040-1 (Tier 5–6) | Tier 5–6 | Code/standard consensus, not Tier 1/Co-1 |
| **2440mm primary** (DSDG ASL-derived) | Bauman/Gallaudet 2010, Vaughn 2018, Cloete & Rout 2025 (cross-cultural) | **Co-1, Tier 2, Tier 3** | **Highest in-corpus evidence-supported value — absent from this BPC** |
| 3050mm public exterior signing groups | DSDG | Co-1 | Absent |

**The 1800mm "best practice" is a code-consensus default, not Tier 1/Co-1 best practice.** The DEAF-population evidence base (independently corroborated: Vaughn 2018, Cloete & Rout 2025 scoping review, RIT InfoGuides, NEA report on Gallaudet, DesignWithDisabledPeopleNow) supports 2440mm primary. The BPC neither cites this evidence nor flags 1800mm as "DEAF-population insufficient."

The 1200mm non-residential figure is reported without any "REJECTED as design baseline" disclaimer of the kind `mobility-built-environment.md` correctly applies to ADA's 1524mm turning circle. It is treated as one of three valid alternatives ("≥915mm / ≥900mm / ≥1200mm").

**Recommended remediation:**

1. **Relabel** `1800mm` from "best practice" to **"two-wheelchair-passing minimum (Tier 5/6 code consensus)"**.
2. **Add corridor row for DEAF population**: 2440mm primary / 1830mm secondary (Tier Co-1 DSDG; Tier 3 cross-cultural Cloete & Rout 2025), with cross-language caveat (ASL-derived; possibly conservative for ASL group conversation; not yet validated for BSL/DGS/LSF/LIS/Auslan).
3. **Identify the most-accommodating Universal Mode value** the evidence supports — currently this looks like **≥2440mm for primary mixed-population corridors** where DEAF users and any-WC-type passing must coexist.
4. **Reject 1200mm explicitly** as a design baseline using the same pattern used for ADA 1524mm in mob_pg ("cited here as evidence of regulatory lag only, not as a permitted specification value").
5. **Add the cross-population conflict** (DeafSpace open-plan vs. NDV/MH compartmentalisation; vs. DEM identifiable bounded corridors) — currently only flagged in the DEAF-acoustic BPC Opus note; should be in the circulation BPC where the corridor specification actually lives.

#### F2 — Lift dimensions: same pattern, smaller magnitude

The BPC reports BS 8300's 1100×2000mm recommendation but selects 1100×1800mm as best practice in the "Most inclusive provision" line. The 1100×2000mm is the higher-evidence value (BS 8300 is Tier 5 with explicit accessibility intent, post-2018). Selecting 1800mm lift depth means choosing the smaller dimension between two BS 8300 values.

**Independent finding worth investigating:** The IDeA Center figure cited in the same BPC says "Power wheelchair users require 1400×1600mm minimum for independent use." 1400mm WIDTH is not present in any of the BPC's "best practice" values (which keep car width at 1100mm). The 1100mm lift width is the Tier 6 EN 81-70 minimum — not the IDeA-Tier-1-research-supported 1400mm.

**Recommended:** Flag 1400×1600mm (IDeA Center, Tier 1) as the user-research-supported minimum; flag 1100×2000mm BS 8300 as the largest standard-supported. Synthesize both — current BPC synthesizes neither.

#### F3 — Corridor reasoning structurally excludes DEAF and bariatric

The "Power wheelchair users" line (≥1500mm comfortable, ≥1800mm passing) is the BPC's most-extreme value reasoning. It does not mention:
- Sign-language conversation space (Tier Co-1: 2440mm)
- Bariatric WC dimensions (Tier 3: 1925mm Steinfeld 2006 — covered in `bariatric-turning-radius` BPC, not cross-referenced here)
- Walker / rollator + WC passing (no quantified data found in this corpus this pass)
- Service-animal accompaniment (VIS / DBL) — no quantified data found

**Recommended:** This BPC needs a "populations potentially under-served by selected value" disclosure in the same pattern used by `pain-ofs-built-environment-design` (`[EXPERT CONSENSUS — population]`).

### 4.2 `population-general/mobility-built-environment.md` 🟡 — EXEMPLAR with one gap

**This BPC does the audit thing correctly for ADA 1524mm:**

> ADA 1524 mm rejected as a design baseline — cited here as evidence of regulatory lag only, not as a permitted specification value.

This is the pattern the audit calls for. **Adopt this language wherever a code-floor value appears in a best-practice synthesis.**

**The one F3 gap:** `bariatric-turning-radius-built-environment.md` reports Steinfeld 2006 RESNA at **1925mm** for full UDI sample 180° turn, peer-reviewed Tier 3. This is **higher than the mob_pg's 1800mm "best practice"** and is the most extreme/most-accommodating value in the corpus for any kind of WC turning. The mob_pg ladder (1500/1700/1800) caps at 1800+ ("scooter and large power device"). The 1925mm is not incorporated.

**Recommended:** Either (a) extend the mob_pg ladder to 1900mm at the upper bound with Steinfeld 2006 citation, or (b) explicitly carve out bariatric/large-power-WC as Mode-S supplementary provision and document why the 1925mm doesn't apply to the general population. Currently the BPC reads as if 1800mm is the upper bound of evidence; that's not what the corpus contains.

[ASSUMPTION: The user's stated 2200mm power-WC turning value is not present as a turning-radius figure in any BPC fetched this pass — basis: text search across all 98 files returned no `2200mm.{0,40}turning|turning.{0,40}2200mm` match. The 2200×2200mm in `accessible-bathroom-and-grab-bar.md` is a ROOM dimension (zero-threshold wet room dual-transfer), not a turning circle. The closest extreme values in-corpus are: Steinfeld 2006 RESNA 1925mm (bariatric BPC), ESKEH/Invalidiliitto FI 2500mm "outdoor turning recommended for sähköpyörätuoli" (cited in mob_pg), VA Barrier-Free 1830mm bariatric care, VPL Barrier Free 1900mm bariatric. If the user has a specific source supporting 2200mm power-WC turning that is not in the BPC, please supply — I'll cross-check and integrate as the most-extreme finding.]

### 4.3 `bathrooms-and-wet-areas/accessible-bathroom-and-grab-bar.md` 🟢 — GOOD with caveats

**Structural integrity:** clean. Status: COMPLETE (24/24 jurisdictions; co1 25/24; tier5 22/24).

**Wheelchair-test:** mostly passes.
- Power WC turning: 1800×1800mm explicitly named as Tier 5 (BS 8300-2 Annex G) — not collapsed into 1500mm code consensus. ✅
- Grab bar load: 200kg SWL adopted (per fold-down spec Opus synthesis), explicitly upgraded from WHO 110kg "inadequate given KITE 1.3 kN peak force" — exemplary use of biomechanical evidence to override standards consensus. ✅
- WC seat 450mm median (400–500 range per jurisdiction) — range disclosed, median named, consistent with project-standards range discipline rule. ✅
- Vertical bars NEU/hemiplegic: Tier 1 sub-spec (Nakamura 2009, Kennedy 2015) added beyond standards-consensus horizontal bars. ✅

**Caveats (🟡):**
- **Room ≥2200×2200mm dual-transfer** is the chosen value. What is the most-accommodating value in the literature? This pass did not verify — flag for citation-verifier next pass. Specifically: does any Tier 1 paper or Co-1 source recommend a larger room? Habinteg, RCOTSS-Housing, AOTA Home Mod CPG, BS 8300-2 Annex G should be consulted.
- **Single-side minimum 1650×2200mm (BE) / 1600×1700mm (PT)** is reported alongside the 2200×2200mm best practice without explicit "code floor — not best practice" disclaimer. Pattern of mob_pg should be applied: BE/PT minimums are jurisdictional code floors; best practice is 2200×2200mm.
- **Door ≥900mm clear** — same as code-consensus value. Is there Tier 1/Co-1 evidence supporting a wider door for power WC + assistant configurations? CSA B651-23 is cited (Tier 6). No Tier 1/Co-1 evidence for >900mm appears in this BPC. Possible gap.
- DEAF not mentioned (mirror sightlines, visual alert placement in accessible WC for signing communication with assistant). May or may not be in-scope; flag for cross-pop pass.

### 4.4 `controls-and-hardware/reach-range-and-accessible-controls.md` 🔴 — SELF-DISCLOSED PROVISIONAL but used as if not

The status banner reads:
> **STATUS: PROVISIONAL — 16 jurisdictions NOT-RUN; Co-1 0/24; Tier 5 3/24. Do not use as sole basis for specification writing.**

…and the BPC then immediately proceeds to specify the 400–1100mm AFH reach zone as the "Most inclusive provision."

Tension between the banner and the body. The banner says "do not use as sole basis"; the body reads as authoritative.

**Audit findings:**
- **Co-1 0/24** is severe. Reach range is one of the most directly-affected-by-lived-experience parameters in the entire guidebook. Zero Co-1 coverage across 24 jurisdictions is a fundamental gap.
- **The 1220mm side-reach maximum** is correctly identified as a Co-1-driven improvement (LPA advocacy lowering the ADA 1370mm floor) — this is exemplary. ✅
- **The 1100mm "best practice for the most constrained users"** is internally derived ("design should eliminate the need for trunk displacement") rather than evidence-cited. This is a 🟡 — internal reasoning is valid but is logically (○) inferred, not (●) evidence-based per the marker scheme.
- **Door force ≤30N preferred** with AAATE 2016 Tier 1 citation — that's a legitimate Tier 1 anchor. ✅

**Recommended:** Flag the 400–1100mm zone as Co-1-derivative (LPA advocacy → ANSI A117.1 1220mm) but not Co-1-validated for the 1100mm sub-claim. Either find Co-1 evidence for the 1100mm or mark with ○ and add `[CONFIDENCE: medium — Co-1 absent for the constrained-user value]`.

### 4.5 `seating-and-rest/bariatric-turning-radius-built-environment.md` 🟡 — CONTAINS THE EXTREME VALUE

**Status:** DEFERRED-NON-STANDARD. Content not in standard BPC schema.

**The most-extreme turning-radius value in the corpus lives here:**

| Source | Tier | Value |
|---|---|---|
| Steinfeld et al. 2006 RESNA | 3 (peer-reviewed empirical) | 1925mm for full UDI sample 180° turn |
| VA Barrier-Free Design Standard 2025 | 5 (federal standard) | 1830mm (6'-0") bariatric patient care |
| Bariatric WC dimensions | — | up to 1220mm overall width |

**Audit verdict:** The DEFERRED-NON-STANDARD status means the BPC schema doesn't accept this format. But the underlying evidence is well-anchored (Steinfeld 2006 is peer-reviewed RESNA; VA standard is federal). The deferred status is a project-organizational issue, not an evidence quality issue.

**Recommended:** Resolve the schema issue (either upgrade this file to standard BPC format or designate it a supplementary-volume reference). In the meantime, the 1925mm value should be cited in `mobility-built-environment.md` as the evidence-supported upper bound for any WC turning-radius specification, with population-segment scoping (large power chairs / bariatric occupants).

### 4.6 `population-general/ndv-aut-built-environment-quantified-thresholds.md` 🔴 — STUB

The "Best-practice synthesis" section is:

```
**Most inclusive provision:** [STUB — see synthesis content above]
**Most targeted provision:** [STUB — see synthesis content above]
**Conflict resolution:** [STUB — see synthesis content above]
**Highest-ambition actionable specification:** [STUB — see synthesis content above]
**Opus synthesis note:** [STUB — pending Opus synthesis pass]
```

Yet this BPC is referenced by Part 4 specifications and by synthesis-scan-2026-05-06 (e.g. RT60 ≤0.4s convergence node).

**Finding S2.2 (🔴):** Any Part 4 spec citing this BPC as evidence is sourcing a stub. Audit must trace which specs cite it and either downgrade the citation or accelerate the Opus synthesis pass.

### 4.7 `communication-and-alerts/deaf-acoustic-built-environment.md` 🟢 — EXEMPLAR

This BPC handles convergence-vs-evidence correctly:

> **Cross-language convergence:** RT60 ≤ 0.4 s is the consensus best-practice target across all 14 languages and their governing standards (DIN 18041, BS 8300, BBR, NS 8175, BR18, Asetus 241, CTE HR, NBR 10152, NEN 9120 equivalent, Korean school standard). IEC 60118-4 is universally adopted as the hearing loop performance standard across all jurisdictions — the highest cross-language convergence of any DEAF-related specification.

…AND simultaneously provides Tier 1 anchoring:

> **Most targeted provision:** For cochlear implant users: source-to-listener distance to be not more than 3 m without assistive listening augmentation; reverberation to be treated as a primary design variable, not a secondary adjustment. CI users are more sensitive to reverberation than hearing aid users…

…AND the Opus note explicitly cites Tier 1 CI-specific support and Amlani & Russo 2016 for the STI-at-furthest-seat refinement. The convergence is reported but the best-practice claim rests on Tier 1 evidence too. Convergence ≠ Evidence is satisfied.

**Use this file as the template** for what convergent + evidence-based looks like in a guidebook BPC.

### 4.8 `communication-and-alerts/deaf-spatial-design.md` 🟢 — EXEMPLAR for honest evidence-base disclosure

The Opus note self-flags the evidence base:
> EVIDENCE BASE WARNING: This entire BPC derives primarily from a single institutional source (Gallaudet University DeafSpace Design Guidelines 2010) and its derivatives… These are Tier Co-1 specifications from a single Deaf community context (ASL), not validated across signed languages.

This is exactly how a BPC should self-disclose. The 2440mm corridor is correctly labelled Co-1/Tier 2 (single-source, single signed language); the cross-language caveat is preserved; the conflict with NDV/MH compartmentalisation is named.

**Use this file as the template** for evidence-base honesty when the corpus is thin.

---

## 5. Cross-cutting findings

### F-X1 — Internal contradiction: corridor width

The corpus contains contradictory best-practice values for primary corridor width:

| BPC | Best practice | Tier basis | Population modelled |
|---|---|---|---|
| `accessible-circulation-geometry.md` | 1800mm | Tier 5–6 (BS 8300, DIN 18040, NL care) | Wheelchair passing |
| `deaf-spatial-design.md` | 2440mm primary / 1830mm secondary | Co-1 / Tier 2 / Tier 3 | DEAF (ASL-derived) |
| `deaf-acoustic-built-environment.md` (Opus note) | Names the conflict | — | Cross-pop NDV/DEM |

These BPCs do not currently reconcile. The cross-population-conflict-resolutions BPC that should resolve it is **STUB**.

**Recommended:** Resolve the conflict in `cross-population-conflict-resolutions.md` (currently STUB). The Universal Mode answer for primary mixed-population corridors should be the more-accommodating value where no harm-asymmetry argues otherwise — which here is 2440mm (the wheelchair-passing minimum 1800mm is satisfied by 2440mm; the converse is not true). NDV/MH compartmentalisation is a Mode-S supplementary provision (retreat zones, bounded sub-spaces), not a primary-corridor argument.

### F-X2 — Code-floor values appearing in 17 BPCs without consistent rejection language

Files containing 1200mm corridor / 1500mm or 1525mm turning / 850/900mm door / 1220mm reach figures: 17 of the 71 in-scope BPCs.

| File | Code floors mentioned |
|---|---|
| `accessible-circulation-geometry.md` | corridor 1200, turning 1500/1525, door 850/900 |
| `mobility-built-environment.md` | corridor 1200, turning 1500/1525, door 850/900 |
| `accessible-bathroom-and-grab-bar.md` | turning 1500/1525, door 850/900 |
| `reach-range-and-accessible-controls.md` | door 850/900, reach 1220 |
| `residential-entry-and-threshold.md` | corridor 1200, door 850/900 |
| `stair-ramp-threshold-biomechanics-accessibility.md` | corridor 1200 |
| `threshold-door-hardware.md` | door 850/900 |
| `body-sizes-supplementary-populations.md` | door 850/900 |
| `ecological-psychology-haptic-affordances-built-environment.md` | corridor 1200 |
| `jurisdiction-matrix-accessibility-standards.md` | turning 1500/1525 |
| `visitability-residential-accessibility-minimum-standards.md` | door 850/900 |
| `pain-ofs-built-environment-design.md` | door 850/900 |
| `residential-kitchen-and-task-surfaces.md` | turning 1500/1525 |
| `upper-limb-impairment-built-environment.md` | turning 1500/1525 |
| `accessible-laundry-room-design.md` | turning 1500/1525, reach 1220 |
| `accessible-design-economics-cost-premium.md` | corridor 1200 |
| `economics-sources.md` (excluded) | turning 1500/1525 |

**Audit task for next pass:** for each of these 17, verify whether the code-floor value is (a) explicitly rejected as a design baseline (mob_pg pattern — ✅), (b) reported as a code-citation context only, or (c) silently retained as a valid alternative best-practice value (failure). Categorize each.

### F-X3 — "Most cited" vs "best practice" linguistic conflation

The convergence-pattern grep found multiple instances of phrasing like "Aligned on best practice; differ at minimum" (`accessible-circulation-geometry.md` divergent findings table). This phrasing implies code-author agreement is itself the best practice metric. Per the audit thesis, it isn't.

**Recommended doctrine update:** In `voice-style_SKILL.md` (if not already present), forbid "aligned on best practice" / "consensus best practice" without an immediate Tier 1/Co-1 citation. The pattern should be:

> "Aligned on **code-consensus value of X**, [supported by | divergent from] Tier 1 evidence [cite]"

…not:
> "Aligned on best practice"

[ASSUMPTION: voice-style_SKILL.md may already have this rule but I have not yet read it this session — flagged for next pass.]

---

### F-X4 — Geometry framing failure: "turning circle" assumes a pivot the wheelchair cannot perform

The entire BPC corpus uses "turning circle" / "turning radius" language as if wheelchairs rotate around a fixed central axis. Most wheelchairs cannot. The relevant concept is **swept path** (or "swept envelope" — the area traced by the chair's furthest projecting points during a turn) — not an idealized circle.

**Drive-system geometry, confirmed across MDA Quest (Tier 2), industry technical literature, and ADA T-shape provision:**

| Drive system | Approximate pivot | Swept path vs footprint | Multi-point turn needed in tight spaces? |
|---|---|---|---|
| Manual (rear-axle drive) | Near rear axle | Larger — footplates/casters extend forward; swept path includes user feet | Often |
| Power **mid-wheel drive (MWD)** | Between drive wheels (closest to true pivot) | Slightly larger than footprint — front and rear casters trace arcs | Sometimes |
| Power **rear-wheel drive (RWD)** | Near rear | Larger — front of chair (legrest, casters) swings wide | Frequently |
| Power **front-wheel drive (FWD)** | Near front | Larger — rear of chair swings wide | Frequently |
| **Scooter** (3- or 4-wheel) | None — Ackermann-steered like a car | Requires forward + reverse multi-point turn | **Always** |

Implication: a "1500mm turning circle" specification works only for users whose chair approximates a true pivot — that excludes scooters entirely, RWD power chairs in tight 180° turns without multi-point maneuver, and most manual users with extended footplates. The IWA BPAG's explicit acknowledgement that scooters need much more space is right; the prevailing code language hides this.

**ADA's T-shaped turning space** (60" square minimum for manual; 94" square for power/scooter/reclining per ADA Section 304.3.2 alternative) exists in the standards literature precisely because the circle is not always feasible. The project's BPCs do not currently surface T-shape vs. circle as alternative geometries.

**Steinfeld 2006 RESNA values are empirical swept-path measurements** (3D digital probe + video, sample n=275 IDEA + n=50 UDI). They measure what users actually swept during a 180° or 360° turn within defined or open-ended bays. They are *not* idealized turning circles. The audit's QAS finding (2400 mm IDEA + BS8300 entire sample) is therefore evidence-supported as a real-world swept-path requirement, not just a geometric figure.

**Recommended remediation:**

1. **Language audit across all BPCs:** replace "turning circle" with "180° turning clear floor area" or "swept envelope for 180° maneuver" wherever the value functions as a clearance specification (not a description of geometric rotation). "Turning circle" should be reserved for the geometric construction of an inscribed circle, not for the design specification.
2. **Drive-system disclosure** in `mobility-built-environment.md` and `accessible-circulation-geometry.md`: any specification value should name which drive system(s) it accommodates. The current BPC implies one value fits all drive systems, which is false.
3. **T-shaped alternative space** (per ADA): add as a Mode P alternative to the circle for spaces where the circle dimension is not achievable. Cite explicitly. The Steinfeld 2006 paper notes that T-shaped space provisions are an existing ADA-ABA construct.
4. **Multi-point turn provision for scooters:** scooter users cannot pivot. They need a forward+reverse maneuver envelope, geometrically different from a circle. This is currently absent from the corpus.
5. **Universal Mode rejection of pivot-only specifications:** any code value treated as Universal Mode (e.g. 1500 mm circle) implicitly excludes scooter users from independent access. Per project-standards rule on Universal Mode rejection (RULE 2026-03-28 for DEAF acoustic isolation), the same logic applies here: if a Universal Mode specification excludes a population segment, it isn't Universal.

This finding **does not invalidate** the QAS dimensional analysis above — the Steinfeld swept-path values stand. It supplements it: the BPC's framing problem is upstream of the dimensional problem.

---

### F-X5 — Tier numbering inconsistency between project-standards and guidebook-auditor SKILL

`project-standards.md` line 17 (locked Core Doctrine 2026-04-24):
- Tier 1 = OT clinical research
- Co-1 = lived experience
- Tier 2 = NGO/DPO advocacy
- Co-2 = OT CPG
- Tier 3 = systematic reviews + meta-analyses + OT body guidelines
- Tier 4 = international standards
- Tier 5 = national beyond-code frameworks
- Tier 6 = statutory codes

`guidebook-auditor_SKILL.md` (Format Rules §4.1):
- Tier 1 = OT clinical research
- Co-1 = Lived experience
- Tier 2 = NGO/DPO advocacy
- **Tier 3 = OT CPG**  ← different from project-standards
- **Tier 4 = systematic review / meta-analysis**  ← different
- Tier 5 = international standard
- Tier 6 = national beyond-code framework
- **Tier 7 = statutory code**  ← project-standards has no Tier 7

This is a **doctrinal inconsistency** at the canonical-rule level. Per project-architecture v2.3 §"Conflict resolution," skill content overrides PI on execution mechanics, but doctrine sits in PI/governance, and project-standards is canonical doctrine. The guidebook-auditor SKILL needs to align to project-standards numbering, OR project-standards needs to be amended. Until resolved, audits using "Tier N" notation are ambiguous: the same value could be labelled Tier 3 (CPG) or Tier 4 (systematic review) depending on which scheme is in use.

**Recommended:** doctrine-recheck cadence (per project-standards RULE 2026-04-30 03:15 — A13 doctrine-recheck) should pick this up at next RULE_REVISION trigger. In the meantime, every audit document should declare which scheme it uses (this audit declares: project-standards numbering).

---

## 6. Pass 0 limitations / what wasn't checked

- **Citation reality (S3)**: No DOIs verified this pass; gated by research-log-manager LOG cycle. Defer to citation-verification pass.
- **Quantified-claim integrity (S4)**: The 2026-04-09 audit caught 3 fabricated quantified findings in the economics BPC. This pass did not re-verify; defer to verification pass.
- **86 of 98 BPCs not deep-read**: Pass 0 was a mechanical scan + 11 deep reads. The "wheelchair-test" finding (F1) needs to be applied file-by-file across the remaining files. Estimated 4–6 sessions.
- **The user's asserted 2200mm power-WC turning value**: not located in the corpus. Either external source unincorporated, or approximation, or different parameter than turning radius. User callout pending.
- **Skill triggers / SQLite gap-filing**: Pass 0 produces findings, not yet filed as gaps in `data/guidebook.db`. Will file via `python3 scripts/db.py add-gap` in next session once findings prioritized.
- **Voice-style review on flagged passages**: deferred.
- **Adversarial-research protocol on the 12 verified citations from session 2026-05-09**: not re-verified this pass.

---

## 7. Self-bias disclosure

**[SELF-AUTHORED — bias risk]** I'm the auditor. The previous session caught me at 67% adjustment rate when the owner spot-checked. The same failure mode (conflating "evidence on the topic" with "evidence supporting the specific claim") is the canonical Convergence ≠ Evidence failure I'm now using as the audit criterion. There is meaningful risk that I'm producing audit findings that match the criterion rhetorically without actually verifying whether the cited Tier 1/Co-1 evidence supports the most-extreme-value claim. Mitigations:

- Findings F1 (corridor) cross-checked via independent web search confirming Vaughn 2018 / Cloete & Rout 2025 / RIT InfoGuides on 2440mm. ✅
- Finding F-X1 (internal contradiction) is text-on-text comparison; no inference. ✅
- Findings F2/F3 (corpus extreme values) are name-cited but not verified that the cited paper actually contains the cited number. For Steinfeld 2006 RESNA 1925mm: this needs source-document verification; the 2026-04-09 audit hallucination history applies. Flag for next pass with citation-verifier protocol.
- Finding S2 status counts are mechanical pattern matches; high reliability.
- Finding S6.1 (DEAF invisibility) is observational from text search across 98 files; verifiable.

[BIAS: confirmation — basis: I want the audit to find what the user described. I should explicitly check whether any BPC I've read DOES correctly handle the wheelchair-test that I might be missing. The deaf-acoustic-built-environment.md and accessible-bathroom-and-grab-bar.md are exemplars I noted (§4.7, §4.3); if I'm only finding failures, that's the bias firing. I've named exemplars to counter-balance.]

---

## 8. Proposed Pass 1 sequencing

1. **Pass 1A (next)** — extend the wheelchair-test deep-read to the remaining 14 PROVISIONAL BPCs. Verify whether code-floor values are (a) rejected, (b) cited-context, or (c) silently retained. Output per-file findings in same format as §4.
2. **Pass 1B** — citation-verifier on the 4 most-extreme-value claims surfaced in §4.1, §4.2, §4.3, §4.5. Confirm the cited papers contain the cited numbers. Use research-log-manager CHECK/LOG protocol per standing rule #4.
3. **Pass 1C** — STUB resolution priority list. The 10 STUB files with downstream Part 4 citations are higher priority than STUBs with no downstream. Build the trace.
4. **Pass 1D** — cross-population conflict resolutions (currently STUB). The corridor-width DEAF/NDV/DEM conflict is concrete enough to draft a resolution; would need owner sign-off as governance rather than research.
5. **Pass 1E** — gap-filing in SQLite for findings raised here.
6. **Pass 1F** — voice-style review of the 17 BPCs with code-floor language. Apply the "code-consensus value of X, [supported by | divergent from] Tier 1" pattern.

Owner decides sequence.

---

**End Pass 0.**
