## visual-fire-alarm-seizure-safety

**Updated:** 2026-03-30 (v4 schema synthesis)  **Original search:** 2026-03-26 05:30  **Evidence tier range:** 3–4  **Opus synthesis:** YES [OPUS-SYNTHESIS] — TARGETED-RETRIEVAL

**SYNTHESIS VALIDITY:** PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION
(See PI rule #10; cohort defined by DR-2026-05-23. Evidence cited herein predates the 2026-05-23 metadata-quality rehabilitation. Claims requiring Phase E.2g reverification.)

**Status:** TARGETED RETRIEVAL (not full v4 run). 0.5–1 Hz flash rate provides adequate safety margin below the 3 Hz lower bound of photosensitive epilepsy risk (Harding test range 3–60 Hz).

### Best-practice synthesis
**Most inclusive provision:** All VADs synchronised; flash rate 0.5–1 Hz (minimum effective); supplementary vibrotactile + voice alarm for NEU/NDV/AUT populations
**Most targeted provision:** Where photosensitive populations are primary occupants, voice alarm system as primary notification with VAD as supplementary only
**Conflict resolution:** DEAF/DBL require visual notification; NEU/NDV at seizure risk from same. Resolution: synchronisation + minimum flash rate + supplementary channels. Zoning not required if synchronisation is implemented.
**Highest-ambition actionable specification:** Synchronised VADs at 0.5–1 Hz + voice alarm + vibrotactile in sleeping areas; safety disclosure on all B-10 specifications

### Key sources

| REF-ID | Authors | Year | Title | Tier | Jurisdiction | Notes |
|---|---|---|---|---|---|---|
| VFA-01 | Jordan, J.B. & Vanderheiden, G.C. | 2024 | International Guidelines for Photosensitive Epilepsy. ACM TACCESS 17(3):1–35. DOI:10.1145/3694790. PMC11872230 | 3 | INT | 0.5–1 Hz safety margin |
| VFA-02 | BSI | 2010 | BS EN 54-23:2010 — Fire detection: visual alarm devices | 4 | EU/UK | Flash rate 0.5–2 Hz |
| VFA-03 | NFPA | 2022 | NFPA 72-2022 — National Fire Alarm and Signaling Code | 6 | US | Flash rate 1–3 Hz |
| VFA-04 | Epilepsy Foundation | n.d. | Professional Advisory Board — photosensitive epilepsy recommendations | 2 | US | https://www.epilepsy.com |
| VFA-05 | Martins da Silva, A. & Leal, B. | 2017 | Photosensitivity and epilepsy. Seizure 50:209–218. PMID:28532712 | 3 | INT | Harding test range 3–60 Hz |
| VFA-06 | Fisher, R.S., Acharya, J.N., French, J.A. et al. | 2022 | Visually sensitive seizures: An updated review by the Epilepsy Foundation. Epilepsia 63(4):739-768. DOI:10.1111/epi.17175 | 3 | INT | Most comprehensive current clinical review; confirms 3 Hz lower bound |
| VFA-07 | ISO | 2016 | ISO 9241-391:2016 — Ergonomics of human-system interaction: Requirements for the reduction of photosensitive seizures | 4 | INT | https://www.iso.org/standard/56350.html |

---

### Concept boundary notes
| Language | Native alias | Map | Warning |
|---|---|---|---|
| EN | visual alarm, strobe alarm, VAD, photosensitive epilepsy | visual-fire-alarm-seizure-safety | Cross-population conflict entry: DEAF notification vs. NEU/NDV seizure risk |
| DE | optische Alarmierung, photosensitive Epilepsie | — | |

### Consensus findings
| Finding | Sources confirming | Tier |
|---|---|---|
| Photosensitive epilepsy risk begins at ≥3 Hz (Harding test range 3–60 Hz) | Jordan & Vanderheiden 2024; Martins da Silva & Leal 2017 | 3 |
| 0.5–1 Hz flash rate provides adequate safety margin | Jordan & Vanderheiden 2024 | 3–4 |
| Synchronisation of VADs prevents cumulative flash rate exceeding thresholds | BS EN 54-23:2010; NFPA 72-2022 | 4 |
| DEAF/DBL populations require visual fire notification | All accessibility standards | 4–5 |

### Divergent findings
| Topic | Position A | Position B | Cause |
|---|---|---|---|
| VAD flash rate | NFPA 72: 1–2 Hz permitted | Photosensitive epilepsy evidence: 0.5–1 Hz safer | Standard vs. evidence-based conservative specification |
| Primary notification channel | DEAF: visual as primary | Photosensitive: voice as primary | Population-specific risk; resolve with multi-channel approach |

### NO-DATA / THIN
| Jurisdiction | Language | Reason | Co-1? | Tier 5? |
|---|---|---|---|---|
| — | — | Targeted retrieval only; full multilingual research not conducted | — | — |
| — | — | No standard integrates DEAF notification needs with photosensitive epilepsy risk | — | — |
| — | — | Vibrotactile alarm evidence limited to sleeping areas; waking-hours effectiveness not quantified | — | — |

### Citation mining
**Date:** 2026-05-04 08:30
| Source | Direction | New sources added |
|---|---|---|
| Jordan & Vanderheiden 2024 (VFA-01) | Forward/Backward | Fisher 2022 Epilepsy Foundation updated review (VFA-06); ISO 9241-391 (VFA-07) |
| Martins da Silva & Leal 2017 (VFA-05) | Forward | Fisher 2022 (VFA-06) same network |
**Notes:** Fisher 2022 (DOI:10.1111/epi.17175) is the Epilepsy Foundation's updated review of visually sensitive seizures — most comprehensive current clinical evidence. Confirms 3 Hz lower bound but with population-dependent variation. ISO 9241-391 is the international ergonomics standard for photosensitive seizure reduction in human-system interaction — complements the fire alarm standards.

### Bottom-up findings (functional deficit pass)
Not yet run.

## Metadata

```yaml
slug: visual-fire-alarm-seizure-safety
population: DEAF, DBL, NEU, NDV
last_updated: 2026-05-04
co0006_migration: true
citation_mining_date: 2026-05-04
```
