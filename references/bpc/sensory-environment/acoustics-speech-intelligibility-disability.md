## acoustics-speech-intelligibility-disability

**Updated:** 2026-03-18 22:00  **Evidence tier:** 1–3
**Opus synthesis:** YES [OPUS-SYNTHESIS]
**Consensus finding:** Reverberation above 0.6 sec prevents 100% speech perception even at high SNR. Hearing-impaired listeners are significantly more affected than normal-hearing listeners by both reduced SNR and reverberation. RT differentiation between hearing-impaired and general population is well-evidenced and should be explicit in all specification items.
**Key evidence:**
  - Classroom acoustics: reverberation >0.6 sec prevents 100% speech perception; ANSI/ASA S12.60-2010 standard: ≤35 dBA unoccupied noise; 0.3 sec RT for hearing-impaired children (vs 0.6–0.7 sec general population) (Murgia et al. 2023, Tier 1 systematic review)
  - Binaural study: hearing-impaired listeners significantly more affected than normal-hearing by both reduced SNR and reverberation; reverberation temporally smears noise masker, reducing dip listening benefit (PLOS ONE 2025, DOI: 10.1371/journal.pone.0317266, Tier 2)
  - DEAF loop specification: IEC 60118-4; ±3 dB field uniformity; STI ≥0.5; RT60 ≤0.6 s
  - Speech perception benefit for hearing aid users requires RT60 ≤0.6 s — longer reverberation reduces benefit from hearing aids
**Ranges:**
  - RT60 general population (classroom): ≤0.6 s
  - RT60 hearing-impaired (classroom): ≤0.3 s
  - Background noise: ≤35 dBA (ANSI/ASA S12.60-2010)
  - STI: ≥0.5 for hearing aid and hearing loop users
**Jurisdictions confirmed:** US (ANSI/ASA S12.60-2010) · UK (BB93) · ISO 3382
**Early-close:** No  **Thin/No-data:** Non-English language acoustic standards converge on the same RT60 targets but do not separately specify disability-differentiated thresholds
### best_practice_synthesis
**Opus synthesis:** YES [OPUS-SYNTHESIS] — 2026-03-28

**Most inclusive provision:** RT60 ≤ 0.3 s in all rooms where speech intelligibility is functionally required (classrooms, meeting rooms, consultation rooms, reception areas); background noise ≤ 35 dBA unoccupied; STI ≥ 0.5 at all listener positions. The 0.3 s ceiling that serves hearing-impaired listeners fully contains the 0.6 s general-population ceiling — adopting the stricter value excludes no one.

**Most targeted provision:** Hearing-aid and cochlear-implant users in reverberant, multi-talker environments. Reverberation temporally smears masking noise, eliminating the dip-listening benefit these users depend on; SNR improvement alone cannot compensate when RT60 exceeds 0.6 s. The 0.3 s target restores temporal fine structure access.

**Conflict resolution:** N/A — the hearing-impaired threshold is a strict subset of the general-population threshold. No population is disadvantaged by the lower RT60.

**Highest-ambition actionable specification:** RT60 ≤ 0.3 s (mid-frequency average, 500–2000 Hz) in all speech-critical rooms; background noise ≤ 35 dBA (unoccupied, HVAC operating); field uniformity of hearing-loop signal ±3 dB per IEC 60118-4; STI ≥ 0.5 measured at the furthest listener position with loop or sound-field system active. Tier 1 (Murgia et al. 2023 systematic review) governs the RT60 target; Tier 2 (PLOS ONE 2025 binaural study) confirms the mechanism; Tier 4 (ANSI/ASA S12.60, IEC 60118-4) provides measurement protocol.

**Evidence confidence:** HIGH — Tier 1 systematic review establishes 0.3 s threshold for hearing-impaired populations with replication across classroom and clinical settings; mechanism (temporal smearing of masking noise) independently confirmed by Tier 2 binaural study.

**Opus note:** The 0.6 s value in most building codes is not an evidence-based target for inclusive design — it is the threshold at which even normal-hearing listeners begin to lose speech intelligibility. Treating it as a design target rather than a failure threshold is a category error repeated across ADA, BS 8300, and NCC. The guidebook should frame 0.6 s explicitly as the outer failure boundary, not as a compliant specification.

**Guidebook items affected:** Part 7 acoustic specification items; any item referencing RT60, background noise limits, or hearing-loop performance criteria.

**Key sources (see ## Key sources table below)**

## Key sources

| REF-ID | Authors | Year | Title | Tier | Jurisdiction | Notes |
|---|---|---|---|---|---|---|
| ASI-01 | Murgia, S., Webster, J., Cantor Cutiva, L.C. & Bottalico, P. | 2023 | Systematic Review of Literature on Speech Intelligibility and Classroom Acoustics in Elementary Schools. Lang Speech Hear Serv Sch 54(1):322-335. DOI:10.1044/2022_LSHSS-21-00181. PMID:36260411 | 1 | INT | Systematic review; RT60 >0.6s prevents 100% speech perception even at high SNR — GREY RESOLVED 2026-05-04 |
| ASI-02 | (author TBC) | 2025 | Binaural study: hearing-impaired listeners and reverberation. PLOS ONE. DOI:10.1371/journal.pone.0317266 | 2 | INT | Temporal smearing mechanism |
| ASI-03 | ISO | 2009 | ISO 3382-1:2009 — Measurement of room acoustic parameters | 4 | INT | https://www.iso.org/standard/40979.html |
| ASI-04 | ASA | 2010 | ANSI/ASA S12.60-2010 — Acoustical Performance Criteria for Schools | 4 | US | ≤35 dBA; RT ≤0.3s for HI |
| ASI-05 | IEC | 2017 | IEC 60118-4:2014+AMD1:2017 — Hearing loop performance | 4 | INT | See ALS-01 / DAB-01 |
| ASI-06 | Cueille, R., Lavandier, M. & Grimault, N. | 2022 | Effects of reverberation on speech intelligibility in noise for hearing-impaired listeners. R Soc Open Sci 9:210342. DOI:10.1098/rsos.210342. PMC9428532 | 3 | FR | HI listeners: SRT increase 18dB (RT 0→1s) vs 10dB NH; quantifies HI penalty |
| ASI-07 | [Authors TBC — Korean] | 2022 | Investigation of the Appropriate Reverberation Time in Learning Spaces for Elderly People Using Speech Intelligibility Tests. Buildings 12(11):1943 | 3 | KR | Elderly incomplete-hearing: RT60 >0.6s degrades scores; suggests ≤0.4s for elderly learning |
| ASI-08 | [Authors TBC] | 2024 | Adaptation to Reverberation for Speech Perception: A Systematic Review. PMC11384524 | 3 (SR) | INT | 23 studies; NH adapt to reverberation, HI do not — supports fixed RT specification |
**Divergent findings:** Standards specify RT60 ≤0.6 s for classrooms generally; hearing-impaired evidence base requires ≤0.3 s — a 2× difference not reflected in most regulatory documents
**Notes:** RT differentiation (hearing-impaired vs general) is well-evidenced but absent from most national building codes. Cross-reference A-items with VIS/DEAF BPC entry for hearing loop integration. NDV/ASD and NEU/ABI populations also benefit from RT ≤0.3 s — see NDV/MH BPC entry.

### Citation mining
**Date:** 2026-05-04 09:00
| Source | Direction | New sources added |
|---|---|---|
| ASI-01 Murgia 2023 | GREY resolved | Lang Speech Hear Serv Sch, DOI confirmed, first author Silvia (not "A.") |
| ASI-01 Murgia 2023 | Forward | Cueille 2022 (ASI-06); Korean elderly learning RT60 study 2022 (ASI-07) |
| ASI-02 | Forward | Adaptation to reverberation SR 2024 (ASI-08) |
**Notes:** Cueille 2022 quantifies the HI penalty: 18dB SRT increase (RT 0→1s) vs 10dB for NH — the most precise quantification of the hearing-impaired reverberation penalty. ASI-08 confirms that NH listeners adapt to reverberation but HI listeners do not — supports fixed RT specification rather than adaptive approach. Korean study adds non-Western evidence for elderly populations.

## Metadata

```yaml
slug: acoustics-speech-intelligibility-disability
population: DEAF, NEU, NDV
last_updated: 2026-05-04
co0006_migration: true
citation_mining_date: 2026-05-04
```
