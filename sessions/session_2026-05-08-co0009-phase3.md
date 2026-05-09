# Session: 2026-05-08/09 — Comprehensive Build + Speculative Flagging + Search Coverage
**Model:** Opus 4.6
**session_close:** 2026-05-09
**next_action:** 11 OPEN gaps. 30/91 items carry SPECULATIVE flags. search_languages/search_coverage tables populated (1134 + 1863 rows). Future research sessions should target NOT-RUN language/jurisdiction combinations for SPECULATIVE items.
**blockers:** None.

## Speculative flagging (30/91 items = 33%)
| Type | Count | Examples |
|---|---|---|
| No jurisdiction mandates | 6 | K-02 tactile maps, K-03 haptic zones, K-04 vibrotactile, B-01 circadian, A-13 sound masking prohibition |
| Exceeds all national codes | 4 | E-03 ramp 1:20 (codes 1:12 to 1:17), E-08 corridor 1200mm (code 1000mm) |
| Compound profiles / Mode P | 21 | Population-specific dimensions for SCI, OFS, DEM, NEU |

## Search coverage (populated from BPC data)
| Table | Rows | Status |
|---|---|---|
| search_languages | 1134 | 14 languages × 81 slugs |
| search_coverage | 1863 | 23 jurisdictions × 81 slugs |

Language coverage: EN 59%, DE 53%, JA 40%, FR 38%, ZH 31%, KO 26%.
Jurisdiction coverage: NO 78%, UK 67%, US 64%, DE 64%, AU 42%, JP 33%.

## Cross-jurisdictional verification
- Ramp: DIN 18040 6% (1:17), NBR 9050 8.33% (1:12), ADA 1:12 → guidebook 1:20 most conservative
- Door force: DIN 25N, ADA 22.2N, BS 8300 20N → guidebook 22N within consensus

## 11 OPEN gaps
| Gap | Category | Item | Issue |
|---|---|---|---|
| GAP-040 | RP/P2 | B-10 | Novel alarm timing |
| GAP-027 | RP/P2 | G-04 | Novel OFS bathroom |
| GAP-012 | RP/P2 | I-01 | UPL+DEM compound |
| GAP-076 | RP/P3 | A-12 | Auracast THIN BASE |
| GAP-097 | RP/P3 | B-02 | Lip-reading lighting |
| GAP-154 | RP/P3 | D-08 | Pictogram evidence |
| GAP-019 | RP/P3 | E-03 | SCI-specific gradient |
| GAP-238 | RP/P3 | H-03 | Captioning evidence |
| GAP-008 | RP/P3 | I-01 | Force threshold primary research |
| GAP-260 | RP/P3 | K-05 | Thermal evidence |
| GAP-264 | AUDT/P3 | SYSTEMIC | Multilingual coverage gaps |
