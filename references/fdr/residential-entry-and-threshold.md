# FDR Findings — residential-entry-and-threshold
**Slug:** `residential-entry-and-threshold`
**Topic directory:** `entrances-and-circulation`
**FDR run date:** 2026-04-08
**Status:** COMPLETE — threshold/ramp geometry and entry security/recognition scenarios complete
**Sources:** ADA §405/§406/§303; National Ramp residential ramp guide; HandiRamp residential ramp slope; RCOT HAwD 2019; OT clinical reasoning; TDH FDR cross-reference (FDR-TDH-01 to -06)

---

## FDR-RET-01 — d465/d450 → residential threshold and ramp (residential-specific parameters)

**Note:** FDR-TDH-01 to -06 cover door hardware; this slug captures residential ramp and threshold geometry distinct from commercial ADA.

| Parameter | Value | Condition | Source | Tier | Delta |
|---|---|---|---|---|---|
| Residential ramp gradient — preferred | 1:20 (5%); maximum 1:12 (8.3%); 1:12 absolute maximum per ADA for public; residential typically follows similar practice for safety | WC, mobility aids: 1:12 is navigable for self-propelled manual WC on short runs; 1:20 preferred for power WC, fatigue, and ambulant users; steeper than 1:12 unsafe for most WC users | National Ramp; HandiRamp; ADA §405 | Tier 5–6/Co-2 | CONFIRMS 1:12 max; **NOVEL** — 1:20 preferred gradient for residential context and fatigue populations absent from BPC |
| Landing at door — flat surface requirement | ≥1220×1220mm (4×5ft) flat landing at door face; ≥1524×1524mm (5×5ft) if ramp turns at door | WC: door must be operable from level surface; insufficient landing prevents safe door operation while maintaining WC position | ADA §405.7; National Ramp | Tier 5–6 | CONFIRMS; **NOVEL** — larger 5×5ft landing when ramp turns at door absent from BPC |
| Threshold at base of ramp | Zero or ≤6mm threshold between ramp foot and interior; no abrupt step between ramp and floor | WC + ambulant: ramp eliminates step but if threshold added at interior base, WC wheel catches and ambulant user trips — ramp and threshold must be designed as a unit | ADA §303; OT clinical reasoning | Tier 5–6 | **NOVEL** — ramp-to-interior threshold as compound specification absent from BPC |
| Residential ramp width | ≥914mm (36 inch) clear between handrails | WC + bariatric: 36 inch minimum accommodates standard WC; bariatric WC requires ≥1200mm — specify width at design stage per user | National Ramp; ADA §405.5 | Tier 5–6 | CONFIRMS; REFINES with bariatric exception |
| Handrail — residential ramp | Required when ramp rise >152mm (6 inch) or horizontal run >1828mm (72 inch); bilateral preferred even when not required | WC, fatigue, ambulant: bilateral handrails allow load-sharing and provide access regardless of affected side; residential code allows unilateral but OT best practice is bilateral | ADA §405.8; National Ramp; OT clinical reasoning | Tier 5–6/Co-2 | CONFIRMS handrail; **NOVEL** — bilateral preferred even when not required, with clinical reasoning absent from BPC |

---

## FDR-RET-02 — d440/d310 + cognitive/visual impairment → residential entry security interface

**Sources:** ADA Section 809.5.5.2; 2N accessibility survey; PMC10852902 Safe Home Program; NAD housing discrimination guidance; OT clinical reasoning (Kane, CAPS/CDS)

| Parameter | Value | Condition | Source | Tier | Delta |
|---|---|---|---|---|---|
| Visitor identification — viewer | 180-degree wide-angle viewer at two heights: 1500mm AFF (standing) + 1050–1200mm AFF (seated WC); prism type | VIS partial + MOB seated: viewer usable from both positions; prism clarifies fish-eye image | ADA Section 809.5.5.2; OT reasoning | Tier 5–6 | CONFIRMS dual-height; REFINES with prism spec |
| Video intercom — multi-modal | Audible tone + visible signal (strobe/LED) + smartphone push; visible signal in sleeping areas with deactivation control | DEAF: audio-only = inaccessible; VIS: audio insufficient for visitor ID; DEM: complex interface confusing | ADA Section 809.5.5; 2N survey (43% need pictograms); NAD guidance | Tier 5–6/Co-2 | REFINES — adds multi-modal and deactivation requirement |
| Call-status pictograms | Visual icons on outdoor panel: ringing / in-call / door-open | DEAF visitor: cannot hear audio confirmation of door release; pictogram confirms action | 2N accessibility survey | Co-2/Tier 5 | **NOVEL** — call-status pictograms on entry panel absent from BPC |
| Induction loop at intercom | T-coil loop at outdoor panel and indoor station | DEAF with aids/CI: background noise renders audio unusable without loop; 21% of MDU projects require | 2N survey | Co-2/Tier 5 | **NOVEL** — induction loop at intercom absent from BPC |
| DEM entry security config | Keypad inside (not outside); double-keyed exterior locks contraindicated (fire egress); high-mounted latch + camouflage | DEM: inside keypad prevents unwanted exit; double-cylinder deadbolts violate egress code | PMC10852902; Kane CAPS/CDS | Co-2 | **NOVEL** — DEM-specific entry security configuration absent from BPC |
| Entry ID — VIS + DEM | Braille on alarm button; audio door-open confirmation; tactile contrast on call button | VIS: needs audible/tactile confirmation; DEM: single-button call preferred over directory | 2N (Braille on Sentrio); ADA | Co-2/Tier 5 | **NOVEL** — combined Braille + audio + tactile entry specification absent from BPC |

**Clinical reasoning (DEM anti-wandering vs fire egress):** Entry security for dementia conflicts with fire egress. OT solution is layered: camouflage + high-mounted latch + alert sensor — none violating egress code. PMC10852902 found devices altering home appearance were rejected by carers. Tier 2 co-design domain.

**Clinical reasoning (multi-population entry):** Single entry must serve VIS (audio+tactile), DEAF (visual+loop), DEM (simplified+anti-wandering), MOB (height-accessible). Specification: every entry intercom provides audio + visual + tactile + loop as simultaneous parallel channels. Tier 0 convergence.
