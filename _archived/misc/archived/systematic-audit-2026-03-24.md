# Systematic Audit Report
**Date:** 2026-03-24 21:35
**Scope:** Skill ecosystem, workplan, literature reviews, guidebook v9.0
**Reviewer:** Claude (Opus 4.6 Extended)
**Method:** Direct inspection of GitHub state files, /mnt/project/ source files, guidebook body text
**Approach:** Structural → Research Infrastructure → Content → Cross-Cutting Insights

---

## 0. Session State Summary

**Last session:** 2026-03-20 23:15
**Next planned action:** Phase 0 Session 0-A — build `github-io`, `file-splitter`, `evidence-marker`; update `framing-checker`, `evidence-auditor`, `item-specification-writer`
**Gap register:** 100 OPEN (15 P1, 66 P2, 16 P3) · 34 CLOSED · 3 REVIEW
**Workplan:** v10.0 Integrated — 25 sessions across 6 phases. No sessions executed yet. Phase 0 (skills) is first.

---

## 1. Skill Ecosystem Audit

### 1.1 Inventory Reconciliation

**31 skill files** exist in `/mnt/project/`. The PI skill registry lists 30 skills (26 registered + 4 retired). Discrepancy analysis:

| Condition | Count | Items |
|---|---|---|
| In /mnt/project/ AND in PI registry | 27 | Core operational set |
| In /mnt/project/ but NOT in PI registry | 4 | `keyword-lookup`, `research-log-manager` (defined in PI body, no separate file), `vol2-item-formatter`, `toc-editor` |
| In PI registry but NOT in /mnt/project/ | 3 | `research-log-manager` (by design — inline), `citation-miner` (to build), `sensory-coherence-checker` (to build) |
| Retired in PI but still in /mnt/project/ | 0 | Clean — retired skills removed |

**Finding 1.1a:** `keyword-lookup` is in /mnt/project/ but not in the PI skill registry. Either it's retired (remove file) or active (add to registry). **Action:** Classify and reconcile.

**Finding 1.1b:** `vol2-item-formatter` is in /mnt/project/ and referenced in the ecosystem audit as needing update, but is not listed in the PI skill registry table. **Action:** Add to PI registry.

**Finding 1.1c:** `workplan-orchestrator_SKILL-1.md` in /mnt/project/ — note the `-1` suffix suggests a versioning artifact. Should be `workplan-orchestrator_SKILL.md`. **Action:** Rename on next skill update.

### 1.2 Skills Needed for v10.0 (Not Yet Built)

| Skill | Purpose | Blocking Phase | Complexity |
|---|---|---|---|
| `github-io` | Standardised commit infrastructure | Phase 0 — blocks everything | High |
| `file-splitter` | Decompose master doc to per-Part files | Phase 4 | Medium |
| `evidence-marker` | ●/○ classification and audit | Phase 3 + 5 | Medium |
| `bulk-renumber` | Context-aware §-reference rewriting | Phase 4 | High |
| `citation-miner` | Backward + forward citation mining | Phase 2 | Medium |
| `sensory-coherence-checker` | Sensory consistency across room matrices | Phase 5 | Medium |

**Finding 1.2a:** Six skills need building before the workplan can proceed. Three block Phase 0. The workplan correctly sequences these first.

### 1.3 Skills Needing Update for v10.0

Per the ecosystem audit document, 10 skills need updates:

| Skill | Core gap | Impact if not fixed |
|---|---|---|
| `framing-checker` | No BAR-in-Vol-I check; no ●/○ marker awareness | Misses two most important v10.0 rules |
| `evidence-auditor` | No ●/○ verification mode | Can't audit primary v10.0 evidence quality system |
| `item-specification-writer` | No ●/○; no illustration note; no K-category template | Every item needs second pass |
| `cross-reference-resolver` | No K-category codes; no per-Part file awareness | Phase 4 QA breaks |
| `structure-auditor` | Expected heading patterns assume old numbering | Flags correct v10 numbering as errors |
| `chunk-assembler` | Assumes single master document | Assembly fails for v10 architecture |
| `workplan-orchestrator` | Part numbering map references old structure | Sessions start with wrong context |
| `session-consolidator` | No per-Part file awareness for reconciliation | Can't verify multi-file state |
| `vol2-item-formatter` | No ●/○ system; no new Part numbering | Formats to old spec |
| `citation-verifier` | No HARVEST mode for bibliography assembly | Can't build master bibliography |

**Finding 1.3a:** The ecosystem audit (2026-03-20) is thorough and correctly prioritised. No additional update needs identified beyond what it already captures.

### 1.4 Skill-to-Phase Dependency Map

```
Phase 0: github-io ← ALL downstream skills
         file-splitter ← Phase 4
         evidence-marker ← Phases 3, 5
         + 10 skill updates
Phase 1: No new skills needed (editorial decisions are human)
Phase 2: citation-miner ← citation mining step in multilingual-research
Phase 3: evidence-marker (must exist)
Phase 4: bulk-renumber + file-splitter (must exist)
Phase 5: sensory-coherence-checker (must exist)
```

**Finding 1.4a:** The critical path runs through `github-io`. Without it, every subsequent session wastes ~100-200 tokens per commit and risks SHA conflicts. This is correctly identified as Session 0-A, Day 1.

---

## 2. Literature Review and Research Infrastructure Audit

### 2.1 Search-Log Completeness (Critical)

| Metric | Current | Required (per Protocol v4) | Gap |
|---|---|---|---|
| Total slugs | 66 (62 unique) | — | 4 duplicates |
| With `jurisdiction_coverage` block | 8 | All slugs | **88% missing** |
| `co1_attempted: true` | 76 instances | ≥12/24 per slug | Most slugs under-attempted |
| `co1_attempted: false` | 124 instances | — | 62% of jurisdictions not Co-1 attempted |
| `tier5_attempted: true` | 75 instances | ≥16/24 per slug | Most slugs under-attempted |
| `tier5_attempted: false` | 125 instances | — | 63% not Tier 5 attempted |
| With `native_aliases` | 17 | All slugs | **74% missing** |
| With `concept_boundary_warnings` | 17 | All slugs | **74% missing** |
| With `citation_mining` | 20 | All slugs | **70% missing** |
| With `best_practice_synthesis` | **0** | All slugs | **100% missing** |

**Finding 2.1a — CRITICAL:** Zero search-log entries contain a `best_practice_synthesis` field. This is a mandatory field per Protocol v4 and the pre-LOG completeness gate. This means **no slug in the search-log would pass the current pre-LOG check**. Every entry is effectively pre-v4 legacy.

**Finding 2.1b — CRITICAL:** Only 8 of 66 slug entries have a `jurisdiction_coverage` block. The remaining 58 entries lack per-jurisdiction tracking entirely. These entries cannot be evaluated for completeness under Protocol v4.

**Finding 2.1c:** The gap between Protocol v4 requirements and existing search-log entries is systemic, not incidental. Protocol v4 was established 2026-03-19 — most slugs were searched before that date and were never backfilled.

**Implication:** The v10.0 workplan Phase 2 research sessions cannot rely on CHECK returning COMPLETE for any existing slug. Every slug that survived Phase 1 editorial decisions will need a gap assessment against v4 criteria, even if it was recently searched.

### 2.2 Duplicate and Inconsistent Slug Entries

**Duplicate slugs in search-log:**

| Slug | Occurrences | Dates |
|---|---|---|
| `mobility-built-environment` | 2 | 2026-03-19 23:45, 2026-03-19 19:17 |
| `visual-impairment-built-environment` | 2 | 2026-03-17 18:30, 2026-03-19 19:17 |
| `neurological-built-environment` | 2 | 2026-03-17 19:30, 2026-03-19 00:10 |
| `dementia-built-environment` | 2 | 2026-03-17 19:30, 2026-03-19 00:18 |

**Finding 2.2a:** Four core population slugs have duplicate entries. The research-log-manager should locate and update an existing entry, not append a second one. This is likely a parsing bug — the LOG action isn't finding the existing slug when it already exists.

**Pipe-suffix slugs (inconsistent naming):**
Seven slugs use `|POPULATION` suffixes (e.g., `room-acoustic-performance|ALL`). The slug-registry convention is `{domain-descriptor}|{POPULATION-CODE}` but the search-log normalisation rule says "No pipe suffixes." These are contradictory.

**Finding 2.2b:** Slug naming convention needs a single, enforced rule. The search-log says no pipes; the slug-registry uses pipes. Recommend: pipes in slug-registry only (infrastructure key); search-log uses pipe-free normalised form.

### 2.3 BPC Completeness

| Metric | Count |
|---|---|
| BPC entries | 59 |
| PROVISIONAL flags | 13 |
| Duplicate BPC entries | 1 (`deafblind-built-environment-design` appears twice) |

**Finding 2.3a:** The BPC has 59 entries for 62 unique slugs — 3 slugs have no BPC entry at all. These should be identified and either logged or explained.

**Finding 2.3b:** 13 PROVISIONAL flags is 22% of entries. These entries are explicitly marked as insufficient basis for specification writing. The v10.0 workplan Phase 2 research should prioritise upgrading PROVISIONAL entries for populations that survive Phase 1 editorial decisions.

### 2.4 Protocol v4 Compliance Timeline

The research protocol was significantly upgraded on 2026-03-19. Before that date, research runs used a different (weaker) protocol:

| Search-log date | Protocol era | Key difference |
|---|---|---|
| Before 2026-03-19 | Pre-v4 | Academic DBs searched before Co-1/Tier 2; no jurisdiction-level tracking; no native_aliases requirement; no citation mining |
| 2026-03-19 onward | v4 | Co-1/Tier 2 first; 24-jurisdiction tracking; native_aliases mandatory; citation mining mandatory |

**Finding 2.4a:** 51 of 66 slug entries predate Protocol v4. Their search order was inverted (academic DBs before Co-1). GAP-PROTO-01 correctly identifies this. The practical consequence: these slugs may have adequate academic evidence but systematically under-retrieved lived experience and DPO/NGO evidence.

**Finding 2.4b:** The 8 slugs with `jurisdiction_coverage` blocks all date from 2026-03-19 or later — confirming that jurisdiction-level tracking was only introduced with Protocol v4.

### 2.5 Evidence Coverage by Population (Synthesis)

Cross-referencing the critique report (§1.2), BPC entries, and gap register:

| Population | BPC slug(s) | Evidence adequacy | Key gap |
|---|---|---|---|
| MOB | `mobility-built-environment` (COMPLETE, 24 jx) | ADEQUATE | Narrow clinical base (3 primary sources 1988-2012); GAP-071 Tier 5 sources not retrieved |
| VIS | `visual-impairment-built-environment` | ADEQUATE | — |
| DEAF | `deaf-spatial-design`, `deaf-acoustic-built-environment` | STRONG | Co-1 genuinely co-primary (DeafSpace/Gallaudet) |
| NEU | `neurological-built-environment` | WEAK | No dedicated NEU OT intervention studies; relies on PAS 6463 |
| DEM | `dementia-built-environment` | STRONG | Best-evidenced non-MOB category |
| NDV | `neurodivergent-built-environment` | ADEQUATE | ASPECTSS is strong but narrow |
| NDV/MH | `mental-health-built-environment` | WEAK | Limited sources |
| PAIN | `chronic-pain-built-environment` | WEAK | Thinnest evidence of any main-taxonomy population |
| DBL | `deafblind-built-environment` | ADEQUATE given novelty | No Tier 1 OT research at all (GAP-DBL-BE-01) |
| OFS | `OFS-built-environment` | WEAK | New category; almost no built-environment evidence |
| IntD | `intellectual-disability-built-environment-design` | INSUFFICIENT | Placeholder only (GAP-CR-11) |

**Finding 2.5a — Pattern:** The populations where this guidebook adds the most value (PAIN, OFS, NDV/MH, IntD) are exactly where the evidence base is weakest. The critique report identified this. The v10.0 workplan Phase 2 correctly targets these populations for research, but with the caveat that Phase 1 editorial decisions may reduce scope.

**Finding 2.5b — Unremarked connection:** The Co-2 tier (OT Clinical Practice Guidelines) is structurally defined in §1.5 but has NO listed sources and NO body text anywhere in the guidebook. CAOT, AOTA, RCOT, WFOT, and COTEC all publish CPGs relevant to environmental modification. This is a significant structural gap — an entire evidence tier is empty. The v10.0 workplan Session 8 (P2-R1) correctly identifies this as a task, but it's buried in the session plan rather than flagged as a standalone P1 gap.

**Recommendation:** Add a P1 gap register entry for Co-2 population. This is an evidence architecture gap, not a content gap — it affects the credibility of the entire evidence hierarchy.

---

## 3. Guidebook v9.0 Structural Audit

### 3.1 Section Numbering Collisions (P1 — GAP-CR-02)

| Part | Heading uses | Collision with |
|---|---|---|
| Part 9 (Engineering) | §9.0–§9.5 | — |
| **Part 10 (Consultants)** | **§9.1–§9.8** | **Part 9** |
| Part 11 (DAR) | §11.0–§11.7 | — |
| Part 12 (Economics) | §12.0–§12.10 | — |
| **Part 13 (Case Studies)** | **§12.01–§12.14** | **Part 12** |
| Part 5 (Residential) | §6.x (in some sub-tables) | Part 6 |

**Finding 3.1a:** Part 10 is the worst collision — it reuses the entire §9.x numbering scheme from Part 9. Lines 5019–5242 show §9.1 through §9.8 headings inside Part 10. A reader looking for "§9.2" will find two entirely different sections (Engineering Brief Templates vs. Occupational Therapist).

**Finding 3.1b:** Part 13 case studies use §12.xx numbering, colliding with Part 12 Economics. This is visible at lines 5899–6129.

**Finding 3.1c:** The v10.0 workplan resolves this through Phase 4 renumbering (single pass after content is final). This is the correct approach — fixing numbering before content changes would require a second renumber pass.

### 3.2 BAR References in Volumes 1–3 (P1 — GAP-STRUCT-01)

BAR should not appear anywhere in Volumes 1–3 per standing rule. Current violations found:

| Location | Content | Line(s) |
|---|---|---|
| §1.4.3 body text | "MOB, VIS, NEU, DEM, NDV, BAR, OFS" | ~249 |
| §1.4.5 body text | "The BAR, DBL, and OFS categories…" | ~283 |
| §2.9 heading | "§2.9 BAR (→ Supp Vol IV)" — redirect stub | ~370 (ToC) |
| §3.3 Co-occurrence matrix | Full BAR row and BAR column retained | 731, 733 |
| §3.3 matrix note | "BAR entries retained for cross-reference continuity (Option B interim)" | 854 |
| Part 5/6 room matrices | BAR columns in multiple matrix tables | 1290, 1337, 1351, 1364, 1377, 1389 |
| NOT-RETROFITTABLE table | BAR references | 880, 883 |
| DAR Register | BAR entries | 893 |
| Part 4 worked examples | BAR references in hospital case | 1130, 1137, 1485, 1781, 1807, 1842, 1846, 1856, 1885, 1919 |

**Finding 3.2a:** BAR appears approximately 25–30 times in Volumes 1–3. The "Option B interim" note at the co-occurrence matrix (line 854) explains why — BAR entries were retained for cross-reference continuity during the transition. However, this directly contradicts the standing rule "No BAR mention permitted anywhere in Volumes 1–3."

**Finding 3.2b:** The v10.0 workplan Phase 3 includes BAR removal as part of each Part's writing session. The co-occurrence matrix BAR row/column is specifically called out. This is correctly planned.

### 3.3 Phantom Item Cross-References (P1 — GAP-CR-03)

| Phantom item(s) | Referenced in | Exists in Part 7? | Status |
|---|---|---|---|
| I-04, I-05, I-06 | Engineering tables (Part 9), matrices, NOT-RETROFITTABLE table | **No** — Part 7 Category I ends at I-03 | Specified in engineering tables but homeless in Part 7 |
| J-01 through J-05 | Matrices, worked examples, engineering tables | **No** — Part 7 has no Category J at all | BAR-specific items; should be struck per GAP-STRUCT-01 |
| H-05 | Engineering tables, sensory zone references | **Partial** — referenced in engineering tables with specs but no standalone Part 7 entry | Nurse Call / Emergency Pull Cord — exists as engineering item, not design item |
| VI-02, VI-03, VI-08 | Cross-reference lines in Part 7 items | **No** — "VI-" numbering scheme doesn't exist | Legacy numbering artifact |

**Finding 3.3a — Novel insight:** I-04, I-05, and I-06 are NOT truly phantom — they have detailed engineering specifications in Part 9 (lines 4792-4793, 4821, 4884-4885, 4918, 4942, 4964-4965, 4981, 5000-5001). They describe: I-04 (Accessible Bathroom — Drainage Channel), I-05 (Hoist and Ceiling Track — Motor Power), I-06 (Kitchen for UPL Users — Power at Accessible Height). These are fully specified engineering coordination items that were never given matching Part 7 design specification entries. They need to be either:
- **(a)** Promoted to full Part 7 items (they are architecturally significant — I-04 and I-05 carry ×20-40 retrofit multipliers), or
- **(b)** Reclassified as engineering-only items with a new prefix (e.g., M-xx for MEP items), clearly distinct from design specification items.

Option (a) is recommended: I-04 and I-05 are NOT-RETROFITTABLE items with the highest cost multipliers in the guidebook. They deserve full Part 7 entries with population applicability, evidence basis, and specification ranges.

**Finding 3.3b:** J-items are BAR-specific. Per GAP-STRUCT-01, the entire Category J should be struck from Volume 2. The corresponding content lives in the Supplementary Volume §IV. The remaining J-references in matrices and worked examples need to be either deleted or redirected to Supplementary Volume codes.

**Finding 3.3c:** "Part 11I §8.4" appears at least 8 times in Appendix B and C items (BIO-01 through BIO-05, TC-01 through TC-05). "Part 11I" is not a valid reference in the document — it appears to be a legacy reference from a prior version's structure where Part 11 had a subsection "I" (possibly an older numbering where DAR content was subdivided differently). Every "Part 11I §8.4" reference needs updating to the correct v9.0/v10.0 target. The content these refer to does not exist.

**Finding 3.3d:** VI-02, VI-03, VI-08 are remnants from a numbering system that predates the current A-through-K category scheme. These are dead references that should be deleted in Phase 3.

### 3.4 ToC-to-Body Mismatch (P1 — GAP-CR-05)

The ToC at lines 29–100 states:
- Category H: Controls & Technology (H-01–H-05) — but Part 7 body only has H-01 through H-04 as standalone items
- Category I: Upper Limb (I-01–I-03) — correct for Part 7, but engineering tables have I-04/I-05/I-06
- No Category J listed in ToC — but J-items are referenced 15+ times in body text
- Part 2 order in ToC doesn't match body: ToC lists "§2.9 BAR (→ Supp Vol IV)" but the v10.0 plan requires alphabetical sort (DBL, DEAF, DEM, IntD, MOB…)

**Finding 3.4a:** The ToC is a snapshot of an intermediate state. It will be rebuilt from scratch in Phase 4 after content is final. No action needed now, but this confirms the critique report's assessment.

### 3.5 Master Bibliography (P1 — GAP-CR-01)

Lines 6130–6141 contain 12 lines of meta-description and zero actual references. The document references dozens of sources throughout its body text — Koontz, Rodosky, Waters, Bettarello, Marquardt, Mostafa, Ulrich, Kaplan, Clark, DbI, ISO standards, national codes — but none appear in a consolidated bibliography.

Part 12 (Economics) has its own reference section (lines 5829–5886) with categorised sources by language group — this is the only functioning bibliography in the document.

**Finding 3.5a:** The Part 12 bibliography is well-structured and could serve as a template for the master bibliography. The v10.0 workplan Session 20 includes bibliography assembly via `citation-verifier` HARVEST mode. This requires the HARVEST mode to be built first (Phase 0).

### 3.6 Part 8 — Cross-Population Conflict Resolutions (Deferred)

Part 8 is explicitly deferred to v10.0. But references to it appear throughout:
- "§8.4.4", "§8.4.6", "§8.4.8", "§8.4.10", "§8.4.11", "§8.4.12" in various item cross-references
- "Part 8 §8.4" in appendix items
- §3.4 contains 12 co-occurrence entries that function as Part 8 interim content

**Finding 3.6a:** The content for Part 8 already exists — it's scattered across §3.4 (12 entries) and individual item cross-reference notes. The v10.0 workplan Phase 3 Session 15 absorbs §3.4 into §4.9. This is the correct approach: consolidate rather than create new.

---

## 4. Content and Evidence Audit

### 4.1 Evidence Hierarchy Internal Consistency

The seven-tier hierarchy (§1.5) is well-designed. One structural gap:

**Co-2 (OT Clinical Practice Guidelines) is entirely unpopulated.** The tier is defined but has:
- No listed source organisations
- No body text explaining what CPGs qualify
- No item specifications citing Co-2 evidence

Relevant Co-2 sources that should be identified and positioned:
- CAOT (Canadian Association of Occupational Therapists) environmental modification CPGs
- AOTA (American Occupational Therapy Association) home modification practice guidelines
- RCOT (Royal College of Occupational Therapists) — Housing Adaptations Without Delay (2019)
- COTEC (Committee of Occupational Therapists in Europe)
- WFOT (World Federation of Occupational Therapists) position statements

**Finding 4.1a:** The Co-2 gap is more significant than it appears. The evidence hierarchy claims seven tiers, but effectively operates on six. This undermines the hierarchy's credibility because Co-2 is specifically designed to bridge the gap between individual clinical research (Tier 1) and advocacy guidelines (Tier 2). An empty Co-2 tier means there's no mechanism for incorporating professional consensus evidence.

### 4.2 Specification Evidence Markers

The v10.0 workplan introduces the ●/○ system (evidence-based vs. inferred). The current v9.0 document does not use this system. Audit of actual evidence coverage in Part 7 items:

From the co-occurrence matrix at line 854, items already carry ● or ○ markers in the matrix. But these markers are NOT present in the Part 7 item specifications themselves. The matrix uses them as applicability indicators, not evidence quality indicators.

**Finding 4.2a:** There is a conceptual ambiguity: the matrix ● means "this item applies to this population" while the v10.0 ● means "this specification has evidence support." These are different claims. The v10.0 workplan needs to address this: either the matrix markers change to a different symbol for applicability, or the evidence markers use a different symbol to avoid confusion.

### 4.3 DAR — Strongest Practical Contribution

The DAR principle is consistently applied:
- Part 11 provides the framework
- Room matrices include DAR provisions tables
- NOT-RETROFITTABLE table identifies irreversible items
- Cost multiplier data (£40 vs. £3,000 / 75× for grab bar blocking) is concrete and compelling
- Part 12 builds the economic case on DAR foundation

**Finding 4.3a:** DAR is the document's most practically consequential contribution and is well-integrated. No action needed beyond the Phase 3 concision pass.

### 4.4 Case Studies — Under-Leveraged

Part 13 contains 14 case studies with verified outcomes, cost data, and cross-references. This is strong content. However:

**Finding 4.4a — Unremarked connection:** The case studies contain the strongest evidence for several specifications that are marked as weakly evidenced elsewhere:
- De Hogeweyk (§12.09): 50% lower antipsychotic rates, 94% independent wayfinding — this is Tier 1-equivalent outcome data for DEM wayfinding specs (D-01, D-09). But it's in Part 13, not cited in the Part 7 items.
- DSDC audit (§12.10): 30-40% reduction in agitation from acoustic intervention — directly supports A-01/A-04 specifications. Not cited in the Part 7 items.
- Lyngby-Taarbæk (§12.06): Acoustic retrofit producing measurable behavioural outcomes — supports the cost-effectiveness argument for A-category items. Partially cross-referenced.

**Recommendation:** Phase 3 writing sessions should systematically mine Part 13 case study outcomes and back-reference them into Part 7 item specifications. This would upgrade several items from ○ (inferred) to ● (evidence-based) without new research.

### 4.5 IntD — Honest but Strategically Unclear

§2.12 is refreshingly honest about being a placeholder. The interim provisions (apply DEM wayfinding, NDV sensory provisions) are clinically reasonable proxies. The multilingual research targets (Lebenshilfe DE, Vilans NL, Plena inclusión ES) are correctly identified.

**Finding 4.5a:** The v10.0 workplan DEC-05 asks whether IntD gets a full evidence review or a condensed ○-marked proxy paragraph. This is the right question. Given that IntD has co-occurrence with DEM, NDV, and NEU at HIGH frequency, the proxy approach (apply DEM + NDV + MOB provisions with honest ○ disclosure) is more defensible than a thin evidence review that overstates what's known.

### 4.6 Cross-Population Conflict — The Document's Intellectual Frontier

The 12 co-occurrence guidance entries (§3.4) represent the document's most original intellectual work. Several insights found nowhere else in accessibility literature:

- MOB+OFS: energy expenditure budget governs circulation — not just supplements MOB
- NEU+PAIN: Uhthoff's thermal conflict is irresolvable at population level; zoned thermal management with individual supplemental heating is the correct compromise
- NDV+MH: sensory retreat must be at ground-floor level (no lift for crisis access)
- VIS+DBL: DBL provisions subsume VIS; VIS items are necessary-but-insufficient for DBL

**Finding 4.6a — Unremarked connection:** The cross-population conflict resolution content is the document's strongest claim to intellectual originality. But it's currently scattered between §3.4 (12 entries), individual item notes (passim), and phantom "§8.4.x" references. The v10.0 workplan correctly consolidates this into §4.9, but the importance of this content is understated in the workplan. It should be flagged as the highest-value content in the entire document — the material most likely to be cited by other practitioners and frameworks.

---

## 5. Cross-Cutting Findings

These are connections, patterns, and systemic issues that span multiple audit domains.

### 5.1 The Protocol v4 / Pre-v4 Divide

The research protocol upgrade on 2026-03-19 created a de facto two-tier research base:
- **Post-v4 slugs** (~15): Have jurisdiction-level tracking, native aliases, concept boundary warnings, and (in principle) Co-1-first search order.
- **Pre-v4 slugs** (~51): Lack jurisdiction tracking, lack native aliases, searched in wrong order (academic DBs first).

**The practical consequence:** Phase 2 research cannot simply CHECK pre-v4 slugs and consume them. Every pre-v4 slug needs at minimum:
1. A gap assessment: which jurisdictions were covered? Which Co-1 sources were attempted?
2. A decision: is the existing evidence adequate despite protocol inversion, or does it need re-running?

**Recommendation:** Add a Phase 2 preliminary step: "Pre-v4 Slug Triage." For each surviving pre-v4 slug, assess whether Co-1/Tier 2 evidence was adequately captured despite the inverted search order. Many slugs may have adequate evidence because Co-1 sources were found incidentally during academic searches. But this needs verification, not assumption.

### 5.2 The Evidence-Originality Inverse

The critique report identified that evidence is weakest where the guidebook adds the most value (novel populations). This audit extends that observation:

| Content type | Evidence quality | Intellectual originality | Strategic value |
|---|---|---|---|
| MOB/DEM/VIS provisions | Strong | Low (well-covered by existing standards) | Baseline — necessary but not differentiating |
| DEAF/DBL provisions | Moderate-Strong | High (DeafSpace, Protactile) | High — few other guides cover this |
| Cross-population conflicts | Mixed | **Very High** — unique in the field | **Highest** — nowhere else synthesised |
| PAIN/OFS provisions | Weak | High (new territory) | High but risky without evidence |
| Economics (Part 12) | Strong | Moderate (builds on existing cost studies) | High — practical weapon for practitioners |

**Implication for Phase 1 editorial decisions:** The scope filter "Is this directly relevant to an architect?" is correct, but should be supplemented with "Is this content we uniquely provide?" The cross-population conflict content, DEAF/DBL provisions, and economics case are the document's competitive advantages. Generic MOB provisions are necessary but not what distinguishes this guidebook from existing standards.

### 5.3 The Engineering Items Bridge

Finding 3.3a revealed that I-04, I-05, I-06 exist as fully specified engineering coordination items but lack Part 7 design specification entries. This is a systemic pattern: the Engineering and Coordination section (Part 9) contains specification-grade content that the Item Specification Library (Part 7) doesn't capture.

Other engineering items that may deserve Part 7 promotion:
- E-12 (Emergency Evacuation — Evacuation Lift Power) — referenced in engineering tables with detailed specs
- H-05 (Nurse Call / Emergency Pull Cord) — full engineering spec at line 4880 but no Part 7 design entry

**Recommendation:** Phase 1 editorial decisions should include a review of Part 9 engineering items for promotion to Part 7. The promotion criterion: "Would an architect need to make a design decision about this item, or is it purely an engineering coordination item?" I-04 (drainage for zero-threshold shower) and I-05 (ceiling hoist structural provision) are clearly design decisions.

### 5.4 The Case Study Evidence Loop

Finding 4.4a identified that Part 13 case studies contain outcome data that could strengthen Part 7 item evidence classifications. The full loop:

```
Part 7 item (e.g., A-01 Acoustic Zoning) → marked ○ (inferred)
↓
Part 13 (e.g., §12.06 Lyngby-Taarbæk, §12.10 DSDC Audit)
contains outcome data: 30-40% agitation reduction from acoustic intervention
↓
This is Tier 2-3 evidence for A-01 effectiveness
↓
A-01 could be upgraded from ○ to ● if case study evidence is formally cited
```

This loop exists for multiple items. Systematically closing it during Phase 3 writing sessions would upgrade the evidence classification of perhaps 10-15 items without any new research.

### 5.5 Slug-to-Item Mapping Gap

There is no explicit mapping between BPC slugs and Part 7 item codes. A practitioner reading the BPC for `deaf-spatial-design` cannot see which Part 7 items that slug's evidence supports. Conversely, a Part 7 item's evidence citation does not reference back to the BPC slug where the evidence was collected and synthesised.

**Recommendation:** The BPC entry schema should include a `part7_items` field listing all items the slug's evidence informs. The Part 7 item template should include a `bpc_slugs` field. This creates a bidirectional evidence traceability chain: BPC → Item Specification → BPC.

This could be implemented as a `cross-reference-resolver` enhancement — adding BPC↔Item traceability as a verification pass.

### 5.6 The Residential Primacy Argument

The v10.0 rules establish "Residential = Tier 2 default" (every person lives somewhere; every residence should tailor itself to the people who live there). This is a strong argument that appears in the project-standards rules but is not yet prominently framed in the guidebook body text.

**Finding 5.6a:** The residential primacy argument is the logical foundation for why this guidebook prioritises home modification evidence over public building evidence. It should be stated explicitly in §1.3 (Designing for the Individual) or §1.4.6 (Application to Residential Design). Currently, §1.4.6 exists (line 291) but may not carry this argument with sufficient force.

### 5.7 The Scalability Question

The v10.0 workplan envisions 25 sessions. At ~1 session per conversation, with context limits requiring new conversations per session, this is a significant undertaking. The critical path:

- Phase 0 (Sessions 1-3): Skills. Must complete before anything else.
- Phase 1 (Sessions 4-7): Editorial decisions. Must complete before Phase 2.
- Phase 2 (Sessions 8-12): Research. Can be narrowed by Phase 1 decisions.
- Phase 3 (Sessions 13-20): Writing. 8 sessions of content editing.
- Phase 4 (Sessions 21-22): Structure. Single renumbering pass.
- Phase 5 (Sessions 23-25): QA and assembly.

**Finding 5.7a:** The workplan is well-sequenced but ambitious. The critical risk is Phase 1 scope decisions — if the Decision Register doesn't narrow scope significantly, Phase 2-3 will require all 25 sessions. If it narrows aggressively (which the author's direction toward "architects and designers" suggests), Phases 2-3 could compress.

---

## 6. Prioritised Recommendations

### P0 — Do Now (Phase 0 prerequisites)

1. **Reconcile skill inventory:** Add `vol2-item-formatter` and `keyword-lookup` to PI registry (or retire `keyword-lookup`). Rename `workplan-orchestrator_SKILL-1.md`.
2. **Build github-io first.** Everything else depends on it.
3. **Add P1 gap for Co-2 tier.** GAP-CO2-01: "Co-2 evidence tier (OT Clinical Practice Guidelines) is defined but empty. Populate with CAOT, AOTA, RCOT, COTEC, WFOT sources before v10.0 publication."

### P1 — Phase 1 Decision Support

4. **Promote I-04 and I-05 to full Part 7 items.** They are NOT-RETROFITTABLE items with ×20-40 cost multipliers — among the highest-impact items in the guidebook. Currently they exist only as engineering coordination entries.
5. **Flag cross-population conflict content (§3.4 → §4.9) as highest-value content.** The editorial scope filter should protect this material from condensation.
6. **Resolve ●/○ ambiguity.** The matrix uses ● for "applies to population"; v10.0 uses ● for "evidence-based." Define distinct symbols or contexts.

### P2 — Phase 2 Research Planning

7. **Add pre-v4 slug triage step.** Assess all 51 pre-v4 slugs for Co-1/Tier 2 adequacy before deciding which need re-running.
8. **Fix duplicate slug entries** (4 duplicates in search-log). Merge to most recent entry.
9. **Enforce slug naming convention.** No pipes in search-log; pipes only in slug-registry infrastructure keys.
10. **Systematically mine Part 13 case studies** for evidence that could upgrade Part 7 items from ○ to ●.

### P3 — Architecture Improvements

11. **Add BPC↔Item bidirectional mapping.** `part7_items` field in BPC; `bpc_slugs` field in item specs.
12. **Define backfill requirements for pre-v4 slugs.** Minimum: add `jurisdiction_coverage` summary, `native_aliases`, `best_practice_synthesis` to the 8-15 most critical pre-v4 entries.

---

## 7. State File Health Summary

| File | Size | Last updated | Health |
|---|---|---|---|
| `gap_register.md` | 45 KB / 184 lines | 2026-03-20 | ⚠ 100 OPEN items; needs Phase 1 triage |
| `references/project-standards.md` | 40 KB | 2026-03-20 | ✓ Current; 8 new rules from last session |
| `references/search-log.md` | 199 KB / 2,886 lines | 2026-03-19 | ⚠ 88% missing jurisdiction_coverage; 4 duplicates |
| `references/best-practices-compendium.md` | 265 KB / 2,572 lines | 2026-03-19 | ⚠ 13 PROVISIONAL; 1 duplicate entry |
| `references/slug-registry.md` | 90 KB / 1,053 lines | 2026-03-18 | ✓ Comprehensive |
| `references/toc.md` | 23 KB | 2026-03-20 | ⚠ Stale — will be rebuilt Phase 4 |
| `references/standards-registry.md` | 12 KB | — | ✓ |
| `sessions/` | 22 files | 2026-03-20 23:15 | ✓ |
| `workplan/v10-0-integrated.md` | 23 KB / 413 lines | 2026-03-20 | ✓ Current workplan |
| `workplan/ecosystem-audit-phase0.md` | 20 KB / 294 lines | 2026-03-20 | ✓ Phase 0 detail |

---

*End of Systematic Audit Report*
