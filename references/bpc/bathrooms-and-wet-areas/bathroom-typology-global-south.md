# BPC Entry — bathroom-typology-global-south
**Topic:** bathrooms-and-wet-areas
**Status:** COMPLETE — Opus synthesis complete

**SYNTHESIS VALIDITY:** PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION
(See PI rule #10; cohort defined by DR-2026-05-23. Evidence cited herein predates the 2026-05-23 metadata-quality rehabilitation. Claims requiring Phase E.2g reverification.)

> **RE-DERIVATION FIRST PASS — 2026-07-20** (`session_2026-07-20-bathroom-typology-global-south-rederivation`, WS2 of
> `workplan/evidentiary-base-research-plan-2026-07-19.md`). The retracted synthesis below is **not** yet rewritten — it
> remains retracted. What changed: the slice's live evidence base has been re-derived from zero (`source_slug_links`
> 0 → 8, `bpc_metadata.evidence_state` RETRACTED-PRE-REHAB → **PARTIAL**), each source re-retrieved via a real tool call
> and passed through an adversarial refutation pass. New verified base (`data/guidebook.db`, DB is source of truth):
> - **REF-00877** (BTG-1, T2 SR/meta-analysis, INT) — Sprouse et al. 2024, shared-sanitation SR — *Cluster 4*.
>   Supersedes the retracted synthesis's garbled "ScienceDirect 2025, 93 studies, 22 countries" citation.
> - **REF-00878** (BTG-2, T3, ID) — Daniel et al. 2023, inclusive-sanitation access for PWDs, Indonesia — *Cluster 2*.
> - **REF-00879** (BTG-3, T3, ID) — Sokhibi et al. 2025, universal-design accessible toilet + Javanese culture — *Cluster 2*.
> - **REF-00880** (BTG-4, T4, INT) — WHO/UNICEF JMP 2023 (3.5bn without safely managed sanitation) — *Cluster 4 context*.
> - **REF-00881** (BTG-5, Co-1 grey, ID) — the Sejong / Setengah Jongkok semi-squat toilet — *Cluster 2 exemplar*.
> - **REF-00077 / REF-00770 / REF-00065** (BTG-6/7/8, deduped existing standards, BR/ID/JP) — NBR 9050:2020,
>   Permen PUPR 14/PRT/M/2017, MLIT 建築設計標準 — *Clusters 1/2/3*.
>
> Audit movement: grade **F (rank 73, 0.0) → B (rank 24, 68.3)**. The "Solano LAC review" named in the retracted
> synthesis did NOT re-retrieve and was **dropped** (anti-fabrication gate). `best_practice_synthesis` remains
> **BLOCKED** pending an Opus-class rewrite (per the skill's capability floor — this was a Sonnet search pass).
> `search_complete=0`: no Co-1 field pass beyond the Sejong exemplar; squat-toilet dimensional specification remains
> a genuine open gap. See `references/search-log/bathrooms-and-wet-areas/bathroom-typology-global-south.md`.

**GAP:** GAP-LRP-04 (P1)
**Phase:** 1-D (Session 1)
**Last updated:** 2026-04-07 00:33
**opus_synthesis:** true [OPUS-SYNTHESIS 2026-04-07]
**Relationship to existing BPC:** Supplementary to accessible-bathroom-and-grab-bar (Opus-synthesised, COMPLETE, 24 jurisdictions). Addresses typology variants absent from existing BPC.

---

## Evidence Summary

### Cluster 1 — Open-plan wet room: accessible principle aligns with dominant Global South typology

The zero-threshold open-plan wet room with floor drain is the most accessible bathroom configuration (existing BPC confirmed). This typology is standard across South/Southeast Asia, MENA, and much of Sub-Saharan Africa. The design challenge is not adoption of a new typology — it is specifying accessible elements within the existing open-plan context:
- Floor gradient toward drain: ≥1:50, not steeper than 1:40 (steeper gradients impede wheelchair stability)
- Non-slip surface: wet COF ≥0.5 (unglazed ceramic, sealed concrete, or non-slip vinyl)
- WC grab bar at existing BPC specification (bilateral fold-down, ≥200 kg SWL, 650–900mm AFF)
- Fold-down shower seat if shower incorporated in wet room area
- Washbasin at accessible height (720–740mm AFF) with knee clearance

These specifications are achievable within local construction norms without specialist materials.

### Cluster 2 — Squat toilet: primary unresolved design problem (zero evidence)

4 billion people globally use squat toilets. PubMed: zero results for accessible squat toilet design. One documented solution exists:

**Sejong Toilet (Indonesia, 2022, Co-1/Tier 1):** Plan International / Nusa Cendana University / DPO co-design. Semi-squat (setengah jongkok) height — lower than standard seated WC but higher than floor-level squat pan. Wheelchair transfer height. Water-efficient (50% reduction vs. seated WC). Front opening for Indonesian manual wash custom. Circle-flush mechanics. Result of multiple prototypes tested by DPO participants. This is the global state-of-the-art in accessible squat toilet design and it is a single unpublished DPO project.

Informal adaptations documented (MIUSA, Co-1): wheelchair positioned over squat pan; curtain replacing door for WC width; wheel removal for narrow doorway; portable commodes as alternative.

RESNA 2012 (India): Explicit statement that Indian accessible standards are copied US/UK and do not match Indian disability population (squat users; polio survivors without wheelchairs; narrow doorways).

### Cluster 3 — Split facility (Japan): comprehensive accessible design model

Japan 多目的トイレ (multipurpose/barrier-free toilet) — mandated by Barrier-Free New Law 2006. Public standard: gender-neutral, WC with backrest and grab rails, ostomate sink, change table, automatic flush, automatic lid, washbasin with lever tap, emergency call. Residential standard: toilet adjacent to bedroom, ≥750mm doorway (800mm WC), sliding or outward door, L-shaped grab rail, ≥1300mm toilet room length, ≥500mm assistance space, step-free path to bathroom. Bathing area (洗い場): separate room, step-free wet zone, grab bar at bath entry.

Design implication for jurisdictions with split-facility norm (India aspirational, Korea, parts of Southeast Asia): each room must be individually accessible AND the route between them step-free within the dwelling. A single combined accessible bathroom does not resolve accessibility if toilet and bath are in separate rooms.

### Cluster 4 — Shared/communal facility: within-scope gap

Shared sanitation is the dominant bathroom typology for over 1 billion informal settlement residents (UNICEF/WHO: 3.5 billion without safely managed sanitation 2022). Systematic review (ScienceDirect 2025, 93 studies, 22 countries): disability is named as a vulnerability group; no accessible design evidence exists for shared sanitation. UN-DESA good practices 2016 includes Ethiopia sanitation case — normative framing but no design specification.

---

## best_practice_synthesis

**Opus synthesis:** YES [OPUS-SYNTHESIS 2026-04-07]

### Typology-Classified Specification Table

| Typology | Transfers from existing BPC | Requires new/variant specification | No evidence — gap flag |
|---|---|---|---|
| **1. Open-plan wet room** | All five accessible principles transfer directly: threshold (zero-threshold with floor drain), surface (wet COF ≥0.5), space (1500mm turning), support (grab bars per existing BPC), controls (lever taps, accessible height). | Floor gradient specification: ≥1:50, ≤1:40 (wheelchair stability constraint on drainage slope). Material options expanded: unglazed ceramic, sealed concrete, non-slip vinyl (cost-appropriate alternatives to porcelain tile). | None — this typology IS the best-practice specification. |
| **2. Squat toilet** | Grab bar specification transfers (wall-mounted support for lowering/rising). Space requirement transfers (≥900mm clear width for approach). | **Cannot be specified from existing evidence.** The Sejong Toilet (Indonesia) is the only documented accessible squat adaptation. It provides a design concept (semi-squat height enabling wheelchair transfer) but not a validated specification. | PRIMARY GAP: no peer-reviewed accessible squat toilet design exists globally. The Sejong Toilet is Co-1/Tier 1 but unpublished and from a single site. The guidebook cannot specify an accessible squat toilet from this evidence base. |
| **3. Split facility** | Each room individually: all five principles transfer per room. Japan residential standard provides the reference specification (≥750mm door, ≥1300mm room length, L-shaped grab rail, sliding/outward door). | Inter-room pathway specification: step-free route between toilet room and bathing room within the dwelling, ≥900mm clear width, adequate lighting. This is an addition to existing BPC which assumes combined bathroom. | None — Japan's Barrier-Free guidance provides complete split-facility specification. |
| **4. Shared/communal** | Five accessible principles apply to the shared facility itself (threshold, surface, space, support, controls). | Additional requirements beyond existing BPC: (a) lockable accessible stall with privacy; (b) step-free approach path from dwelling to facility; (c) lighting on approach path; (d) single-sex option where culturally required; (e) proximity to dwelling (maximum travel distance TBD — no evidence for specification). | PARTIAL GAP: WASH literature names disability as vulnerability group but provides no design specifications. Approach path and proximity specifications have no evidence base. |
| **5. Outdoor/semi-outdoor (pit latrine)** | — | — | OUT OF SCOPE: no constructed structure to specify. Noted for completeness. |

### Sejong Toilet — Citation Validity Assessment

The Sejong Toilet (Indonesia, 2022) is citable as Co-1/Tier 1 evidence under the guidebook's evidence hierarchy:
- It is a documented DPO-led participatory design process (Plan International + Nusa Cendana University + disabled user testing).
- Multiple prototypes were tested by DPO participants before final design.
- The design addresses a real functional gap (squat-to-seated transition at wheelchair transfer height) that no other documented solution addresses.

**However, it cannot serve as a specification source** because:
- It is unpublished in peer-reviewed literature.
- It is a single-site innovation without replication.
- No dimensional specifications, load ratings, or material requirements are documented in accessible sources.

**Guidebook treatment:** The Sejong Toilet should be cited as the only known accessible squat toilet innovation, with a research gap flag directing primary research to validate and document its specifications. The guidebook should not attempt to reverse-engineer specifications from the project description.

### Shared Sanitation — Scope Decision

Per the co1-housing-research-global-south scope decision: the guidebook's scope is formal new construction and planned retrofit. Shared communal sanitation in informal settlements is out of scope for design specifications.

**However,** shared sanitation in formal construction contexts (e.g., worker dormitories, refugee camps built to code, social housing with shared facilities) is within scope. For these contexts:
- One accessible stall per shared facility, meeting all five accessible principles.
- Step-free approach path from dwelling unit to shared facility.
- Lockable door with accessible hardware (lever handle, ≤900mm AFF).
- Privacy provisions (full-height partition, visual screen at entry).
- Adequate lighting on approach path (≥100 lux at floor level).
- Maximum travel distance from dwelling to accessible facility: no evidence exists. Flag as [GAP: shared-sanitation-proximity — no evidence for maximum acceptable travel distance to shared accessible sanitation].

### Evidence Hierarchy

| Tier | Count | Assessment |
|---|---|---|
| Tier 1 / Co-1 | 3 | D1 (Sejong Toilet DPO), D3 (MIUSA wheelchair traveller), D12 (US wet bath Co-1) |
| Tier 1 (non-Co-1) | 1 | RESNA 2012 India |
| Tier 3 | 2 | ScienceDirect 2025 systematic review; Solano LAC review |
| Tier 4–6 | 6 | Japan Barrier-Free; UN-DESA; UNICEF/WHO; BCA Singapore |

**Confidence:** HIGH for open-plan wet room (existing BPC transfers directly). HIGH for split facility (Japan specification is comprehensive). LOW for squat toilet (single unpublished source). LOW for shared sanitation (no design evidence). Typology 5 out of scope.

---

## co1_pass_summary
D1: Indonesia (DPO co-design, Sejong Toilet). D3: MIUSA (wheelchair traveller squat adaptation strategies). D12: US Co-1 wet bath lived experience.

## Sources (12 confirmed)
See search log for full table.

## Key sources

[STUB — this BPC file is a deferred non-standard file. Full research pass pending (Block 5 decision required). See gap register for status.]

## Metadata

```yaml
slug: bathroom-typology-global-south
population: MOB, ALL
last_updated: 2026-04-19
status: DEFERRED-NON-STANDARD
note: Non-standard BPC file. Full content deferred pending project decision.
```
