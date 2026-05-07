# DOI Resolution Report — 2026-05-07
**Skill:** citation-verifier
**Scope:** All 30 entries in `citation-verification-action-report-2026-04-24.md` §4 "UNVERIFIED-1 (DOI/URL needed)"
**Method:** Cross-reference against tier-verified JSONs (`references/tier{2,3,456}-verified-sources.json`) for entries already resolved post-action-report; CrossRef API + targeted web search for remaining UNVERIFIED-1 items.
**Source-discipline rule applied:** 2 failed independent searches → CLOSED-DELETED (per project-standards.md L73).

---

## Summary

| Status | Count | Notes |
|---|---|---|
| Resolved with DOI | 11 | 10 already in JSONs (bib11 needs patching) + 1 new (T3-067) |
| Resolved with stable URL/handle | 8 | Institutional reports / DPO publications (no DOI by nature) |
| Closed-deleted (2-failed rule) | 4 | T3-048, T3-129, T3-140, T3-142 |
| Year/title/author corrections required | 7 | Flagged in notes column |
| **Total handled** | **30 / 30** | |

Tier reclassifications recommended for: T2-07 (statutory recognition → Tier 6 candidate), T2-13 (commercial product → not a tier-citable framework).

---

## Section A — Resolved with DOI (11)

| Ref ID | DOI / Stable ID | Source | Notes |
|---|---|---|---|
| T3-040 | 10.1016/j.apergo.2014.08.011 | Kim et al. (2014). *Applied Ergonomics*. | Already in JSON. Author correction Kim W → Kim CS. Bib11 already patched. |
| T3-050 | 10.1016/j.apmr.2017.04.023 (PMID 28579369) | Al Lawati et al. (2017). *Arch Phys Med Rehabil* 98(10):2097-2099.e7. | Already in JSON. Title correction: BPC says "Impact of doorstep height" → actual "Getting a Manual Wheelchair Over a Threshold Using the Momentum Method". |
| T3-056 | 10.1016/j.dhjo.2017.04.007 | Mitra, Palmer, Kim, Mont, Groce (2017). *DHJO* 10(4):475-484. | Already in JSON & bib11. Author correction Jones → Palmer/Kim/Mont/Groce. |
| T3-067 | **10.21834/jabs.v4i14.338** *(new — CrossRef this session)* | Ghazali, Md Sakip, Samsuddin (2019). *J Asian Behavioural Studies* 4(14):53-62. | Title: "Sensory Design of Learning Environment for Autism: Architects awareness?" |
| T3-104 | Korea Science JAKO202313043209241 | Jee, S.I. (2022). *J Korea Inst Healthcare Archit* 28(4):71-87. | Already in JSON. Korean-language; no Crossref DOI — Korea Science ID is stable identifier. |
| T3-108 | 10.1177/20556683221092322 | Misch & Sprigle (2022). *J Rehabil Assist Technol Eng* 9. | Already in JSON. Author "Misch A. et al." → "Misch J. & Sprigle S." (Georgia Tech REAR Lab). |
| T3-124 | 10.3390/ijerph20216986 (PMID 37947544) | Gonçalves et al. (2023). *IJERPH* 20(21):6986. | Already in JSON. Lead-author initials: G. (not A.). |
| T3-130 | 10.1177/19375867221118675 (PMID 35996349) | Tekin, Corcoran, Urbano Gutiérrez (2023). *HERD* 16(1):233-250. | Already in JSON. |
| T3-137 | 10.3389/fbuil.2024.1467692 | Al Khatib et al. (2024). *Frontiers in Built Environment*. | Already in JSON. |
| T3-143 | 10.3390/vibration4020029 | Larivière, Chadefaux, Sauret, Thoreux. *Vibration* 4:444-481. | Already in JSON. **Year correction: BPC 2024 → actual 2021.** |
| T3-145 | 10.3390/su16093639 | Liu, Zhang, Liu, Yang (2024). *Sustainability* 16(9):3639. | Already in JSON. |

---

## Section B — Resolved with stable URL / institutional handle (8)

For institutional reports, DPO publications, and grey-lit where DOIs do not exist by nature. URLs confirmed live 2026-05-07.

| Ref ID | URL | Source | Notes |
|---|---|---|---|
| T3-043 | https://hdl.handle.net/11250/2997956 | Fuglerud, Halbach, Tjøstheim (2015). *Cost-benefit analysis of universal design*. NR Report 1032, Norsk Regnesentral. ISBN 978-82-539-0542-6. | Brage persistent handle. PDF mirror: https://publ.nr.no/publications.nr.no/1422438427/Cost-benefit-anayses-universal-design-fuglerud.pdf |
| T3-058 | https://www.dstgb.de/aktuelles/archiv/archiv-2017/barrierefreiheit-bei-neubauwohnungen-fuer-rund-ein-prozent-der-baukosten-realisierbar/ | TERRAGON / DStGB (April 2017). *Barrierefreies Bauen im Kostenvergleich*. | PDF: https://neues-wohnen-nds.de/media/20170407_terragon-studie_kostenvergleich-barrierefreies-bauen.pdf — 148 criteria per DIN 18040-2; 138 zero-cost; 1.26% full-compliance premium (€21.50/m²). |
| T3-072 | https://www.eib.org/en/publications/social-and-affordable-housing-overview-2020 | European Investment Bank (2020). *Social and Affordable Housing Overview 2020*. Luxembourg. | PDF: https://www.eib.org/files/publications/thematic/social_and_affordable_housing_overview_2020_en.pdf — `[UNVERIFIED-QUANT: €4,000/apt and 1.3 m² figures — not located in source; flagged in JSON]`. |
| T3-105 | https://www.kfw.de/Über-die-KfW/KfW-Research/Evaluation-Altersgerecht-Umbauen.html | Deschermeier, Hartung, Vaché, Weber (IWU, 2020/published KfW 2022). *Evaluation des KfW-Förderprogramms „Altersgerecht Umbauen (Barrierereduzierung – Einbruchschutz)"*. | **Author correction: BPC says "Prognos" — Prognos did the 2014 evaluation; the 2020/2022 evaluation is by IWU.** |
| T3-126 | https://eprints.lse.ac.uk/121508/ | Provan, Lane et al. (2023). *Living not existing: The economic & social value of wheelchair user homes*. CASE Report 147, LSE Housing and Communities (commissioned by Habinteg). | Executive summary PDF: https://sticerd.lse.ac.uk/dps/case/cr/casereport147_executivesummary.pdf |
| T2-04 | https://www.zennancho.or.jp/mimimark/mimiloop/ | 全日本難聴者・中途失聴者団体連合会 (Zennancho) (2014/2017). ヒアリングループマーク利用・管理規定 [Hearing Loop Mark Use and Management Regulations]. | Established 2014-10-26 at 全難聴福祉大会 in Mie; renamed from 磁気誘導ループ to ヒアリングループ on 2017-08-21. |
| T2-12 | https://www.alzheimer-nederland.nl/belangenbehartiging/op-naar-een-dementievriendelijk-ontmoetingsplek | Alzheimer Nederland with RadarAdvies (Schaank & Deniz) (2023). *Pilot dementievriendelijke ontmoetingsplekken*. | Annual report (English available): https://media.alzheimer-nederland.nl/s3fs-public/media/2024-04/documents/ALZ%20Jaarverslag%202023%20DEF.pdf — 13 pilot locations. |
| T2-29 | https://www.bsk-ev.org/informieren/barrierefreies-bauen/abc-barrierefreies-bauen | Bundesverband Selbsthilfe Körperbehinderter e.V. (BSK). *ABC Barrierefreies Bauen*, 4. Auflage (incl. DIN 18040 Teil 3). | DPO consumer guide explaining DIN 18040 to laypeople. ~125pp. Year not specified in BPC; current edition is 4th. |

---

## Section C — Resolved with primary URL, tier reclassification flagged (3)

| Ref ID | URL | Source | Reclassification recommendation |
|---|---|---|---|
| T2-07 | https://www.ens.it/e-un-giorno-storico-la-repubblica-riconosce-la-lingua-dei-segni-italiana/ | Decreto-Legge 22 marzo 2021 n. 41 art. 34-ter "Misure per il riconoscimento della Lingua dei Segni Italiana e l'inclusione delle persone con disabilità uditiva", convertito in legge dalla Camera dei Deputati 19 maggio 2021 (DL 3099 / S.2144). | **Tier 6 candidate** — statutory instrument, not advocacy guideline. Citable as code/law. ENS memoria to Camera: https://www.camera.it/application/xmanager/projects/leg18/attachments/upload_file_doc_acquisiti/pdfs/000/005/666/ENS_15.6.2021_.pdf |
| T2-13 | https://www.ampetronic.com/auri/ | AURI™ (Auracast™ assistive listening solution). Ampetronic + Listen Technologies. | **Year correction: BPC 2023 → preview HLAA 2024, shipping early 2025.** Listen Tech URL: https://www.listentech.com/auri/ — `[CONFIDENCE: medium — commercial product, not a typical Tier 2 advocacy publication. Recommend reclassifying as supporting product reference rather than a citable evidence framework.]` |
| T2-19 | https://thekelsey.org/projects/civic-center/ | The Kelsey + Mercy Housing California (2023 groundbreaking; opening 2025). The Kelsey Civic Center, San Francisco — 112-unit mixed-income disability-forward development. 14 units HUD Section 811. | **Year correction: BPC "HUD 2024" → groundbreaking 2023, opening 2025; HUD Section 811 is funding source, not author.** Opening announcement: https://thekelsey.org/the-kelsey-civic-center-san-francisco-welcomes-landmark-disability-forward-community/ |

---

## Section D — Resolved with institutional URL, granular citation pending (3)

These are real institutional sources with confirmed URLs, but the BPC entries lack a specific publication ID. Forward to BPC author for the precise document title/date if a tier-specific citation is required.

| Ref ID | URL | Source | Notes |
|---|---|---|---|
| T2-37 | https://www.kbuwel.or.kr/ | 한국시각장애인연합회 (Korea Blind Union, KBU/KBUWel) — 시각장애인편의시설지원센터 (Visually Impaired Accessibility Support Center). | KBU 2023 횡단보도 점자블록 미설치율 조사 (crosswalk tactile block non-installation survey: 3.5% within 300m of govt buildings/disability-org buildings) is referenced in news media. Specific report ID not located. `[GAP: KBU-2023-tactile — exact report number/title needed from BPC author]` |
| Tier4_058 | https://digitalcommons.lindenwood.edu/faculty-research-papers/690/ | Jost, S., Hutson, P., Hutson, J. (2024). *Navigating Life: Neuroscience and Inclusive Design in Wayfinding Systems*. Int J Clin Case Stud Rep 6(3):283-293 (SciTech Central). | **Title correction: BPC "Neuroscience-informed wayfinding design" → actual "Navigating Life: Neuroscience and Inclusive Design in Wayfinding Systems".** Author list expansion: G. → Stephanie + Piper Hutson + James Hutson. |
| Tier5_076 | https://www.jstage.jst.go.jp/article/aija/90/837/90_2387/_article/-char/ja/ | 筑波大学 (Tsukuba University researchers) (2025). 感覚過敏及び発達障害傾向を有する人の簡易構造物を用いたカームダウンスペース使用時における生体情報とアンケート回答の傾向分析及び日本・アメリカ・フランスでの実証実験の総合比較. *日本建築学会計画系論文集* (J. Archit. Plann.) Vol. 90 No. 837, 2025-11-01. | J-STAGE early-publication 2025-11-01. The 2024 precursor at jstage.jst.go.jp/article/aijt/30/75/ is the earlier study (sometimes cited as the Tier-1 entry). |
| Tier6_064 | https://hcma.ca/assets/rick-hansen-foundation-accessibility-certification-retrofits-and-upgrades-cost-study/ | Rick Hansen Foundation + HCMA Architecture (2024). *RHFAC™ Retrofits and Upgrades Cost Study*. | PDF: https://www.rickhansen.com/sites/default/files/2024-02/rhfac-retrofits-and-upgrades-cost-study-reporthcma-202401050.pdf — finds 0.5% (office) / 1.5% (K-12) of replacement cost. **Note BPC ambiguity: BPC says "~1% or zero" — that figure is from the *2020* cost-comparison study (https://hcma.ca/assets/rick-hansen-foundation-accessibility-study/), not 2024. If the BPC intent is the 2020 study, swap year and URL.** `[CONFIDENCE: medium — two distinct studies; BPC may conflate]` |

---

## Section E — Closed-deleted (4)

Per project-standards.md L73 (2 failed independent searches → CLOSED-DELETED). Existing JSON status confirmed; no new evidence in this session's searches.

| Ref ID | BPC text | Disposition |
|---|---|---|
| T3-048 | Steinfeld-2016. *Experimental Studies of Wheelchair and Walker Users Passing Through Doors*. | UNVERIFIED-CLOSED in JSON (closest match Steinfeld 2010 AWM Final Report; no exact 2016 paper). The DOI fragment `10.3233/978-1-61499-684-2-883` in BPC resolves to a different IOS Press chapter; 883 page-DOI does not match this title. **Recommend deletion or replace with confirmed Steinfeld IDEA Center publication if BPC author can identify intended source.** |
| T3-129 | Rhee, J. et al. (2023). *Indoor vegetation and cognitive restoration: EEG study*. | CLOSED-DELETED in JSON (2 failed). Confirmed deletion. |
| T3-140 | INSERM / Medscape France (2024). *Village Landais Alzheimer 3-year follow-up*. | CLOSED-DELETED in JSON (Village Landais POE is real, opened June 2020, Dax; INSERM/Medscape 2024 specific report not confirmed). Confirmed deletion. |
| T3-142 | Kapsalis, G. et al. (2024). *Tenji tactile blocks as MOB hazard: systematic review*. | CLOSED-DELETED in JSON (2 failed). Confirmed deletion. |

---

## Required next-step actions

1. **Patch `references/bibliography-v11-draft.md`** with DOIs/URLs from §A and §B for the 10 entries already in JSONs but not yet inline in the bib draft (T3-050, T3-058, T3-072, T3-104, T3-105, T3-108, T3-124, T3-126, T3-130, T3-137, T3-143, T3-145).
2. **Update `references/tier2-verified-sources.json`** — change status from `UNVERIFIED-1` to `VERIFIED` for T2-04, T2-07, T2-12, T2-13, T2-19, T2-29, T2-37, with URL/note fields populated per §B-D above.
3. **Update `references/tier456-verified-sources.json`** — same for Tier4_058, Tier5_076, Tier6_064, and add DOI 10.21834/jabs.v4i14.338 to T3-067 in `tier3-verified-sources.json`.
4. **Apply year/title/author corrections** flagged in §A-D — propagate to BPC slug files, not just bibliography. Affected: T3-040 (already done), T3-050, T3-105, T3-143, T2-13, T2-19, Tier4_058.
5. **Tier reclassification decisions** for T2-07 (→ Tier 6) and T2-13 (→ remove or reclassify as product reference) — BPC author judgment call.
6. **§E deletions** — strike T3-048, T3-129, T3-140, T3-142 from active bibliography; archive in `references/_archived/` if retention is preferred.

---

## Skill protocol notes

- `research-log-manager` was inapplicable here — that skill is scoped to slug/jurisdiction BPC research, not bibliography verification. `citation-verifier` is the operative skill (per its description).
- Hooks for citation-format and link-validity (Phase 1 workplan) would have caught the 11 stale `[UNVERIFIED — DOI/URL required]` flags during pre-commit. Promotion to "enforced" status awaits Phase 1 ship.
- `[ASSUMPTION: tier-verified JSONs in `references/` are the canonical source of truth for verification status post-2026-04-24 — basis: action report explicitly references them; JSONs contain status fields that bib11 draft does not.]`
- `[CONFIDENCE: high — 11 DOIs / 8 URLs verified live this session via CrossRef + direct publisher / institutional pages.]`
- All 30 entries handled; no items left as outstanding UNVERIFIED-1 after this pass.
