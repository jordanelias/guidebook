## Multi-Population Conflict Matrix — ACOUSTIC-LVL (Background Noise & Amplification)
**Date:** 2026-03-29 01:15
**Domain:** ACOUSTIC-LVL — Background noise level, speech amplification, sound masking
**Populations served:** DEAF, DEM, NDV/AUT, NDV/SENS, NEU, PAIN, OFS
**Classification:** [INTER-GROUP] — different occupants in shared space
**Overall status:** LARGELY ALIGNED with two focal conflicts (SFA amplification; sound masking)

### Domain Decomposition

On examination, ACOUSTIC-LVL decomposes into five sub-parameters with distinct conflict profiles:

| Sub-parameter | Pop A need | Pop B need | Conflict? |
|---|---|---|---|
| RT60 (reverberation) | DEAF: ≤ 0.3 s (Iglehart 2020, Tier 1; ANSI/ASA S12.60) | NDV/AUT: ≤ 0.3–0.4 s; DEM: ≤ 0.5 s | **ALIGNED** — strictest target (DEAF ≤ 0.3 s) is strict subset; serves all |
| Background noise | DEAF: ≤ 30–35 dB(A) | NDV/SENS, NEU, OFS, PAIN: ≤ 30–35 dB(A) | **ALIGNED** — all populations want quiet |
| Hearing loops | DEAF: IEC 60118-4 loops in assembly/reception/service spaces | NDV/SENS: no increase in ambient sound | **NO CONFLICT** — loop signal is electromagnetic (T-coil), inaudible to non-users |
| Sound field amplification (SFA) | DEAF: amplified speech (especially children, Vickers 2013) | NDV/SENS: amplification increases ambient sound level; PAIN: hyperacusis (Geisser 2021); OFS: acoustic sensitivity | **PARTIAL CONFLICT** |
| Sound masking | Workplace acoustics guidance: mask speech for privacy | NDV/AUT, NEU, DEM: contraindicated (PAS 6463; A-13 doctrine) | **DIRECT CONFLICT** |

### Active Conflicts

| Domain | Pop A | Pop B | A spec | B spec | Resolution | Status | Evidence |
|---|---|---|---|---|---|---|---|
| SFA (sound field amplification) | DEAF (classroom/meeting room) | NDV/SENS, PAIN, OFS | Ceiling SFA for group speech intelligibility | Ambient amplification causes distress/pain | Personal FM/DM systems (directed to individual, not ambient) | RESOLVED-EVIDENCE | ● |
| Sound masking | Workplace privacy guidance | NDV/AUT, NEU, DEM | White/pink noise masking for speech privacy | Contraindicated: increases sensory load, masks environmental cues DEM needs for orientation | No sound masking in NDV/NEU/DEM spaces; alternative speech privacy via RT60 design and spatial layout | RESOLVED-CONSENSUS | ◐ |

### Resolution Evidence Register

**Resolution 1 — Personal FM/DM over SFA (for SFA conflict)**
- Source: Anderson & Goldstein 2004 (REF-RAP-21, Tier 1); Iglehart 2004 (REF-RAP-19, Tier 1)
- Mechanism: Personal FM/DM remote microphone transmits directly to hearing device. No ambient sound increase. In high-reverberation rooms, personal FM provides substantial benefit while ceiling SFA provides none (Anderson & Goldstein 2004). Desktop FM provides intermediate benefit.
- Outcome data: Tier 1 — controlled comparison, hearing-impaired children. Personal FM significantly outperforms SFA in reverberant conditions.
- Guidebook implication: Tier 0 specifies FM/DM infrastructure (charging, transmitter at lectern/service counter). SFA remains appropriate as supplementary provision where NDV/SENS population is not primary (e.g., general assembly halls) but is contraindicated in NDV-designated spaces.
- Operability: FM/DM requires no action from non-DEAF occupants. No ambient impact.
- Status: **RESOLVED-EVIDENCE** · Confidence: **HIGH**

**Resolution 2 — No sound masking + acoustic design for privacy (for sound masking conflict)**
- Source: PAS 6463:2022 §10; A-13 doctrine (this guidebook); Bettarello et al. 2021; room-acoustic-performance BPC
- Mechanism: Achieve speech privacy through RT60 design (absorption placement), spatial layout (no direct sound paths between private/public zones), and partition STC rather than acoustic masking. Sound masking adds noise floor that NDV/AUT, NEU, DEM populations cannot filter.
- Outcome data: No controlled comparison of masking vs no-masking for NDV populations. PAS 6463 guidance (Tier 5). NDV evidence base documents harm from unpredictable background noise (Bettarello 2021, Caniato 2024).
- Guidebook implication: Tier 0 prohibition of sound masking in all spaces serving NDV/AUT, NEU, or DEM populations. In buildings where population is unidentified (Tier 0), default to no sound masking — the harm asymmetry favours quiet.
- Status: **RESOLVED-CONSENSUS** · Confidence: **MEDIUM** — Tier 5 guidance + clinical plausibility without controlled comparison

**Resolution 3 — RT60 ≤ 0.3 s as universal target (alignment, not conflict)**
- Source: Iglehart 2020 (Tier 1, PMID 31835909); ANSI/ASA S12.60-2010; Murgia et al. 2022 (Tier 3, systematic review)
- Mechanism: The DEAF/CI-driven 0.3 s target is a strict subset of the general 0.6 s target. Reducing RT60 from 0.6 to 0.3 s provides additional benefit to CI users and no harm to any other population (Iglehart 2016/2020). NDV/AUT evidence supports ≤ 0.3–0.4 s. DEM evidence supports ≤ 0.5 s. The strictest target serves all.
- Outcome data: Tier 1 controlled studies (Iglehart 2016, 2020; Wroblewski 2012; Neuman 2010).
- Guidebook implication: Tier 0 default RT60 ≤ 0.3 s in all speech-critical rooms. This is not a conflict resolution — it is an alignment finding. The 0.6 s code value is the failure threshold, not a design target (per Opus note in acoustics-speech-intelligibility-disability BPC).
- Status: **RESOLVED-EVIDENCE** (alignment) · Confidence: **HIGH**

### Aligned Parameters (No Conflict)

| Parameter | Universal target | Evidence | Confidence |
|---|---|---|---|
| RT60 (speech-critical rooms) | ≤ 0.3 s (500–2000 Hz mid-frequency average) | Iglehart 2020 (Tier 1); ANSI/ASA S12.60; serves DEAF, NDV/AUT, DEM, NEU | HIGH |
| Background noise | ≤ 35 dB(A) unoccupied, HVAC operating; aspiration ≤ 30 dB(A) | ANSI/ASA; BrainXchange DEM; NDV BPC | HIGH |
| Hearing loops | IEC 60118-4 in all assembly/reception/service/speech-critical spaces | No conflict — electromagnetic, inaudible to non-users | HIGH |
| STI | ≥ 0.60 general; ≥ 0.75 DEAF/CI; measured at furthest seat | Iglehart 2020; room-acoustic-performance BPC + Opus adjudication | HIGH |
| NRC | ≥ 0.85 with spectral balance 250 Hz–4 kHz; high-frequency-dominant panels contraindicated | Amlani & Russo 2016 caveat; GAP-RAP-01-b Opus adjudication | HIGH |

### Tier 0 Specification Summary

ACOUSTIC-LVL is one of the few domains where a genuine Tier 0 specification is possible because the strictest targets serve all populations:

1. RT60 ≤ 0.3 s (mid-frequency average 500–2000 Hz) in all speech-critical rooms
2. Background noise ≤ 35 dB(A) (unoccupied, HVAC operating); aspiration ≤ 30 dB(A)
3. Hearing loop (IEC 60118-4) in all assembly, reception, service counter, and speech-critical spaces; Auracast-ready infrastructure as DAR
4. STI ≥ 0.60 general / ≥ 0.75 DEAF/CI at furthest occupied seat (not room average)
5. NRC ≥ 0.85 with balanced spectral absorption 250 Hz–4 kHz; position-specific verification
6. Personal FM/DM infrastructure in classrooms and meeting rooms
7. No sound masking
8. SFA permissible in general assembly; contraindicated where NDV/SENS primary

### Contrast with LIGHT-INT

ACOUSTIC-LVL demonstrates the opposite pattern to LIGHT-INT. In lighting, the conflict is mechanistically irreconcilable (shared ipRGC pathway serving opposing clinical objectives). In acoustics, the targets are largely aligned — the strictest population-specific target (DEAF ≤ 0.3 s) is a strict subset that serves all populations. The only genuine conflicts are in amplification method (resolved by personal FM/DM) and sound masking (resolved by prohibition + alternative privacy design).

This contrast is itself an important finding for Part 5 §5.2: not all multi-population domains are conflicting. Some converge to a universal specification through the strictest population-specific target. The guidebook should distinguish between convergent and divergent domains.

### Unresolved Gaps → Gap Register

| Gap ID | Populations | Specification implication | Research needed |
|---|---|---|---|
| GAP-CONF-ACOU-01 | NDV/AUT, PAIN | No controlled comparison of sound masking vs no-masking for NDV/PAIN populations. Current prohibition is PAS 6463 guidance + clinical plausibility. | Tier 3 study: masking effect on NDV/PAIN self-regulation or pain |
| GAP-CONF-ACOU-02 | DEAF, NDV/SENS | SFA in mixed-population educational settings: no study measures NDV/SENS response to classroom SFA. Prohibition in NDV-designated spaces is extrapolated from general noise sensitivity evidence. | Study: SFA effect on NDV/AUT students in inclusive classroom |

### Sources

| Source | Tier | Role in matrix |
|---|---|---|
| Iglehart 2020, AJA, PMID 31835909 | 1 | RT60 ≤ 0.3 s for DEAF/CI — primary specification driver |
| Iglehart 2016, AJA, PMID 27244568 | 1 | RT60 reduction benefits CI users specifically |
| Anderson & Goldstein 2004, LSHSS, PMID 15191328 | 1 | Personal FM > SFA in reverberant rooms |
| Amlani & Russo 2016, JAAA, PMID 27885976 | 3 | NRC panel caveat — STI compliance ≠ adequate listening |
| Bettarello et al. 2021, Applied Sciences, DOI:10.3390/app11093942 | 3 | NDV/AUT acoustic thresholds |
| Caniato et al. 2024, Building and Environment | 3 | NDV/AUT noise sensitivity confirmation |
| Murgia et al. 2022, LSHSS, PMID 36260411 | 3 | Systematic review: classroom acoustics |
| Devos et al. 2019, PMC 6950055 | 2 | DEM acoustic intervention |
| Geisser et al. 2021 | 3 | PAIN hyperacusis |
| PAS 6463:2022 §10 | 5 | Sound masking contraindication |
| ANSI/ASA S12.60-2010 | 6 | RT60 / background noise standards |
| IEC 60118-4:2014+AMD1:2017 | 4 | Hearing loop standard |
| DIN 18041:2016 | 5 | DE hearing-impaired room acoustics |
| UNI 11532-2:2020 | 5 | IT NDV-equivalent acoustic provisions |

---
*Opus synthesis 2026-03-29. Cross-population-conflict-mapper ACOUSTIC-LVL.*
