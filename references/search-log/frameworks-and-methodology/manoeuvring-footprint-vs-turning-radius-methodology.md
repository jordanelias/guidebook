# Search-log: manoeuvring-footprint-vs-turning-radius-methodology

```yaml
slug: manoeuvring-footprint-vs-turning-radius-methodology
query: "wheelchair turning swept path manoeuvring space biomechanics + manoeuvring footprint anthropometry clear floor + parameter naming convention turning radius vs swept envelope"
last_searched: 2026-05-25 14:00
early_close_triggered: false
note: "Methodology BPC authored 2026-05-25 per owner directive (closes GAP-272). EN-primary — methodology framing is developed in English wheelchair-biomechanics literature; the substantive evidence on swept-path vs turning-circle is concentrated in US (IDeA Center / Steinfeld), UK / Northumbria (Chaikhot, Taylor et al.), and AU (Trefler & Sawatzky) outputs. Multilingual coverage is shallow because the parameter-name deprecation is a synthesis claim within the Guidebook, not a cross-jurisdictional empirical question."
languages:
  EN: {status: SEARCHED, results: 18, db: [pubmed, web, scholar_gateway_not_used], note: "PubMed 'wheelchair manoeuvring space anthropometry clear floor area' returned PMID 20402047 (Steinfeld 2010 international comparison); cluster search for biomechanics surfaced PMC10293636 (Chaikhot 2023 — corrected from initial mis-attribution as Vergara); web search surfaced AutoTURN swept-path methodology, US 7,182,166 footrest-tuck patent rationale, Trefler & Sawatzky 2008 ResearchGate publication 43533647"}
  DE: {status: NOT-RUN, results: 0, db: [], note: "Methodology BPC — multilingual pass deferred per scope note"}
  FR: {status: NOT-RUN, results: 0, db: [], note: "Methodology BPC — multilingual pass deferred per scope note"}
  ES: {status: NOT-RUN, results: 0, db: [], note: "Methodology BPC — multilingual pass deferred per scope note"}
  NL: {status: NOT-RUN, results: 0, db: [], note: "Methodology BPC — multilingual pass deferred per scope note"}
  SV: {status: NOT-RUN, results: 0, db: [], note: "Methodology BPC — multilingual pass deferred per scope note"}
  NO: {status: NOT-RUN, results: 0, db: [], note: "Methodology BPC — multilingual pass deferred per scope note"}
  DA: {status: NOT-RUN, results: 0, db: [], note: "Methodology BPC — multilingual pass deferred per scope note"}
  FI: {status: NOT-RUN, results: 0, db: [], note: "Methodology BPC — multilingual pass deferred per scope note"}
  JA: {status: NOT-RUN, results: 0, db: [], note: "Methodology BPC — multilingual pass deferred per scope note"}
  KO: {status: NOT-RUN, results: 0, db: [], note: "Methodology BPC — multilingual pass deferred per scope note"}
  ZH: {status: NOT-RUN, results: 0, db: [], note: "Methodology BPC — multilingual pass deferred per scope note"}
  PT: {status: NOT-RUN, results: 0, db: [], note: "Methodology BPC — multilingual pass deferred per scope note"}
  IT: {status: NOT-RUN, results: 0, db: [], note: "Methodology BPC — multilingual pass deferred per scope note"}
top_sources:
  - Chaikhot 2023 PMC10293636 / DOI 10.3389/fspor.2023.1127514 (Tier 1 — primary biomechanical study; corrected from initial mis-attribution as Vergara)
  - Steinfeld 2010 DOI 10.1080/10400430903520280 (Tier 1 — international convergence-not-evidence diagnosis)
  - Steinfeld 2006 RESNA proceedings (Tier 3 — empirical envelope values, AUTHOR-TITLE-ONLY pending retrieval)
  - Bauman 2010 DSDG (Co-1 Tier 1 — independent-evidence-stream 2440 mm corridor convergence)
  - Vaughn 2018 DeafScape (Co-1 Tier 1)
  - Cloete 2025 (Tier 3 — cross-cultural DeafSpace scoping review)
  - Trefler & Sawatzky 2008 (Tier 2 sr_meta — five-rig public-transport manoeuvring tests)
  - BS 8300-2:2018 (Tier 5 — UK best-practice framework anthropometric annex)
bpc_ref: "manoeuvring-footprint-vs-turning-radius-methodology"
thin_flags: []
no_data_flags: []
note: "Methodology BPC — parameter-name deprecation backed by 4 independent grounds (no in-place pivot per Chaikhot 2023; forward-swept geometry excluded; drive-system-dependent envelopes; manoeuvre-type conflation). EN-primary by scope: this is a synthesis claim, not a cross-jurisdictional empirical question. Multilingual coverage deferred."
```

```yaml
jurisdiction_coverage:
  US: {status: SEARCHED, co1_attempted: true, tier5_attempted: false, tier6_attempted: false, note: "IDeA Center anthropometric work (Steinfeld team SUNY Buffalo)"}
  UK: {status: SEARCHED, co1_attempted: false, tier5_attempted: true, tier6_attempted: false, note: "BS 8300-2:2018 anthropometric annex; University of Essex (Taylor et al. 2023)"}
  AU: {status: PARTIAL, co1_attempted: false, tier5_attempted: true, tier6_attempted: false, note: "Trefler & Sawatzky public-transport manoeuvring rigs"}
  CH: {status: PARTIAL, co1_attempted: false, tier5_attempted: false, tier6_attempted: false, note: "Swiss Paraplegic Research (de Vries 2023 co-author)"}
  TH: {status: PARTIAL, co1_attempted: false, tier5_attempted: false, tier6_attempted: false, note: "Christian University of Thailand (Chaikhot 2023 first author)"}
  INT: {status: SEARCHED, co1_attempted: true, tier5_attempted: true, tier6_attempted: false, note: "Independent-evidence-stream convergence (DSDG corridor + IDeA wheelchair anthropometry)"}
```

## Authoring note

This methodology BPC was authored as a single English-language synthesis pass in session_2026-05-23-bpc-rewrite-phase-b-closure on 2026-05-25 in direct response to owner directive: "yes, but you have to include a discussion about why turning radius is disingenuous compared to swept path/turning maneouvres".

The four grounds for deprecation (§2 of the BPC: no in-place pivot; forward-swept geometry; drive-system variation; manoeuvre-type conflation) are independently established in the literature. The §3 application of the convergence-not-evidence principle to the 1500 mm code convergence rests on Steinfeld 2010's explicit diagnosis ("U.S. standards, which are based on research conducted in the 1970s, need to be updated").

Authorship correction recorded at first revision: the primary biomechanical study cited throughout was initially attributed to "Vergara et al." from a misread of the PMC10293636 full-text snippet. Per PubMed PMID 37383064 the correct authors are Chaikhot D, Taylor MJD, de Vries WHK, Hettinga FJ 2023. Migration `data_20260525090000_chaikhot_2023_authorship_correction.sql` corrects the evidence_sources row in lock-step.

Multilingual coverage is intentionally English-only at first authoring. The deprecation is a synthesis claim about parameter naming and modelling adequacy, not a cross-jurisdictional empirical question. Code-name variants in 19 languages (DIN 18040 Bewegungsfläche, NBR 9050 módulo de referência, etc.) are cited in §1 from the existing mobility-built-environment.md BPC's prior multilingual pass; this BPC inherits that coverage rather than repeating it.
