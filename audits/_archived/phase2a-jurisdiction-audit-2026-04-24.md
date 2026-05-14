# Phase 2A — Jurisdiction Coverage Audit
**Generated:** 2026-04-24 06:31
**Scope:** 93 BPC slug files × 49 registry jurisdictions
**Method:** Automated extraction of NO-DATA/THIN tables and Consensus "Jurisdictions confirming" columns

---

## Coverage Summary

| Status | Count | Jurisdictions |
|---|---|---|
| COVERED (confirming evidence, ≤0 NO-DATA gaps) | 6 | AU, CA, EU, ISO, UK, US |
| PARTIAL (confirming evidence, some gaps) | 14 | BE, BR, CH, DE, DK, FI, FR, IE, JP, NO, NZ, PT, SE, SG |
| PARTIAL-THIN (confirming evidence, >5 gap slugs) | 5 | CN, ES, IT, KR, NL |
| NO-DATA (no confirming evidence found) | 0 |  |
| ABSENT (no mention at all in BPC) | 24 | AR, BD, CL, CO, CR, EC, EG, ET, GH, GT, ID, IN, INT, KE, MA, MX, NG, PE, PH, TH, TZ, UN, UY, ZA |

---

## Jurisdiction Detail

| Jurisdiction | Status | Confirmed slugs | NO-DATA slugs | Priority gaps |
|---|---|---|---|---|
| AR | ABSENT | 0 | 0 | — |
| BD | ABSENT | 0 | 0 | — |
| CL | ABSENT | 0 | 0 | — |
| CO | ABSENT | 0 | 0 | — |
| CR | ABSENT | 0 | 0 | — |
| EC | ABSENT | 0 | 0 | — |
| EG | ABSENT | 0 | 0 | — |
| ET | ABSENT | 0 | 0 | — |
| GH | ABSENT | 0 | 0 | — |
| GT | ABSENT | 0 | 0 | — |
| ID | ABSENT | 0 | 0 | — |
| IN | ABSENT | 0 | 0 | — |
| INT | ABSENT | 0 | 0 | — |
| KE | ABSENT | 0 | 0 | — |
| MA | ABSENT | 0 | 0 | — |
| MX | ABSENT | 0 | 0 | — |
| NG | ABSENT | 0 | 0 | — |
| PE | ABSENT | 0 | 0 | — |
| PH | ABSENT | 0 | 0 | — |
| TH | ABSENT | 0 | 0 | — |
| TZ | ABSENT | 0 | 0 | — |
| UN | ABSENT | 0 | 0 | — |
| UY | ABSENT | 0 | 0 | — |
| ZA | ABSENT | 0 | 0 | — |
| CN | PARTIAL-THIN | 2 | 7 | accessible-circulation-geometry, residential-entry-and-threshold, ALL-ROOMS |
| ES | PARTIAL-THIN | 5 | 7 | cognitive-wayfinding-design, mobility-built-environment, accessible-laundry-room-design |
| IT | PARTIAL-THIN | 9 | 11 | cognitive-wayfinding-design, residential-kitchen-and-task-surfaces, visual-impairment-built-environment |
| KR | PARTIAL-THIN | 7 | 6 | accessible-circulation-geometry, residential-kitchen-and-task-surfaces, residential-entry-and-threshold |
| NL | PARTIAL-THIN | 9 | 8 | deafblind-built-environment-design, accessible-laundry-room-design, ALL-ROOMS |
| BE | PARTIAL | 5 | 3 | cognitive-wayfinding-design, residential-entry-and-threshold, ALL-ROOMS |
| BR | PARTIAL | 5 | 3 | accessible-circulation-geometry, residential-kitchen-and-task-surfaces, ALL-ROOMS |
| CH | PARTIAL | 7 | 3 | cognitive-wayfinding-design, residential-entry-and-threshold, ALL-ROOMS |
| DE | PARTIAL | 17 | 4 | IntD, intellectual-disability-built-environment-design, deaf-spatial-design |
| DK | PARTIAL | 8 | 3 | residential-kitchen-and-task-surfaces, residential-entry-and-threshold, ALL-ROOMS |
| FI | PARTIAL | 6 | 5 | residential-kitchen-and-task-surfaces, residential-entry-and-threshold, ALL-ROOMS |
| FR | PARTIAL | 12 | 4 | neurodivergent-built-environment, NDV, ALL-ROOMS |
| IE | PARTIAL | 8 | 2 | residential-entry-and-threshold, ALL-ROOMS |
| JP | PARTIAL | 9 | 3 | accessible-circulation-geometry, ALL-ROOMS, reach-range-and-accessible-controls |
| NO | PARTIAL | 17 | 5 | residential-kitchen-and-task-surfaces, DEAF, ALL-ROOMS |
| NZ | PARTIAL | 3 | 3 | cognitive-wayfinding-design, residential-entry-and-threshold, ALL-ROOMS |
| PT | PARTIAL | 9 | 4 | cognitive-wayfinding-design, residential-kitchen-and-task-surfaces, accessible-laundry-room-design |
| SE | PARTIAL | 12 | 3 | residential-kitchen-and-task-surfaces, ALL-ROOMS, reach-range-and-accessible-controls |
| SG | PARTIAL | 8 | 3 | residential-kitchen-and-task-surfaces, residential-entry-and-threshold, ALL-ROOMS |
| AU | COVERED | 18 | 0 | — |
| CA | COVERED | 14 | 0 | — |
| EU | COVERED | 5 | 0 | — |
| ISO | COVERED | 13 | 0 | — |
| UK | COVERED | 19 | 0 | — |
| US | COVERED | 14 | 0 | — |


---

## Slugs with Highest NO-DATA Burden (scope-gate candidates)

Slugs exceeding 10 NO-DATA jurisdiction entries are candidates for scope-gating
(restricting to EN/multilingual scope rather than attempting per-jurisdiction synthesis).

| Slug | NO-DATA entries |
|---|---|
| ALL-ROOMS | 49 |
| residential-entry-and-threshold | 11 |
| DEAF | 10 |
| reach-range-and-accessible-controls | 10 |
| residential-kitchen-and-task-surfaces | 9 |
| deaf-spatial-design | 7 |
| MOB | 6 |
| cognitive-wayfinding-design | 6 |
| DBL | 5 |
| NDV | 5 |
| accessible-circulation-geometry | 5 |
| accessible-design-failures-poor-performance | 5 |
| deafblind-built-environment-design | 5 |
| mobility-built-environment | 5 |
| neurodivergent-built-environment | 5 |
| accessible-laundry-room-design | 5 |


---

## Top Coverage Gaps by Jurisdiction

Jurisdictions with the most NO-DATA entries across slugs — highest research priority:

| Jurisdiction | NO-DATA slugs | Notes |
|---|---|---|


---

## FROZEN Slug Warning

Note: Several root-level slug files contain `<!-- FROZEN -->` headers indicating
they are historical archives. Jurisdiction coverage data from FROZEN files should
be treated as indicative only; canonical data is in the topic subdirectory slugs.

FROZEN files detected (root level): ALL-ENV.md, ALL-FW.md, ALL-ROOMS.md, DBL.md,
DEAF.md, DEM.md, IntD.md, MOB.md, NDV-MH.md, NDV.md, NEU.md, OFS.md, PAIN.md, VIS.md,
thermoregulation-built-environment.md (15 files)

Active canonical slugs: 78 (in topic subdirectories)

---

## Recommended Actions

1. **Scope-gate candidates** — jurisdictions with >8 NO-DATA slugs and no foreseeable 
   research path: CN (ZH), IT, KR — formally mark as scope-gated in affected slugs.
   
2. **Research priority** — jurisdictions partially covered with active evidence base:
   ES, PT, NL (despite thin output), NO, FI — targeted searches may yield additional entries.
   
3. **FROZEN file review** — the 15 root-level slug files flagged FROZEN should be 
   confirmed as superseded by their topic-subdirectory equivalents before next BPC update.
   
4. **ALL-ROOMS.md** — highest single-slug NO-DATA burden; review whether it is still
   the correct consolidation point or if jurisdiction data should migrate to subdirectory slugs.
