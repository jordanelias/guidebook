# Query plan — batch 09 R1 pass. Priors written before execution.

Each row's `prior` is what goes into `log-search --prior-expectation` verbatim. Committed before
the first query runs. Tier order is R1's: Co-1 → Co-2 → T2. Engine `web` throughout — Step 1 of
multilingual-research says retrieve from publication pages directly, so a general search index is
used to LOCATE a publication page and never as the evidence itself (T3 = navigation only).

| # | Jur | Lang | Target | Query (verbatim) | Prior |
|---|---|---|---|---|---|
| 1 | UK | EN | co1 | Habinteg wheelchair housing design guide ramp gradient | States a gradient, restated from Part M / BS 8300 rather than derived. Habinteg is disability-led, so the document is Co-1-adjacent; the NUMBER will not be its own. |
| 2 | UK | EN | co2 | RCOT housing adaptations without delay ramp gradient occupational therapy | Practice guidance citing the statutory maximum; possibly a preference for shallower. Best chance of a Co-2 working value. |
| 3 | UK | EN | co1 | Disability Rights UK ramp too steep wheelchair independent access | Positional/experiential, no number. Likely an inadequacy finding (R7). |
| 4 | US | EN | co2 | AOTA home modification ramp slope occupational therapy practice | Cites ADA 1:12; may prefer 1:16 or 1:20 for self-propulsion. |
| 5 | US | EN | co1 | Paralyzed Veterans of America ramp slope wheelchair users guidance | PVA is a disabled-led membership organisation; may carry a stated preference distinct from ADA. |
| 6 | CA | EN | co2 | CAOT occupational therapy ramp slope home access guideline | Thin — CAOT publishes less freely-available practice guidance than RCOT. |
| 7 | AU | EN | co1 | Summer Foundation OR Physical Disability Australia ramp gradient housing accessible | Livable Housing Design Guidelines restated (1:14 in AS 1428.1); not independently derived. |
| 8 | INT | EN | co1 | International Spinal Cord Society OR wheelchair user organisation ramp gradient self-propulsion limit | Low yield; if it lands it is the threshold claim the cell needs. |
| 9 | DE | DE | co1 | Rollstuhl Rampe Neigung barrierefrei Selbsthilfe Verband | DIN 18040 restated (6%); DPO framing rather than derivation. |
| 10 | NL | NL | co1 | rolstoel helling hellingbaan percentage toegankelijkheid Ieder(in) | Dutch guidance restates NEN/Bbl; possible practical rule of thumb. |
| 11 | FR | FR | co1 | pente rampe fauteuil roulant accessibilité APF France Handicap | Arrêté 2014 (5%) restated; APF is a large DPO with position papers. |
| 12 | ES | ES | co1 | pendiente rampa silla de ruedas accesibilidad CERMI ONCE | CTE DB-SUA restated; CERMI is the Spanish disability platform. |
| 13 | SE/NO | SV/NO | co1 | rullstol ramp lutning tillgänglighet OR rullestol rampe stigning | Nordic guidance is usually 1:12/1:20 from BBR/TEK17. |
| 14 | JP | JA | co1 | 車椅子 スロープ 勾配 バリアフリー 障害者団体 | Barrier-free Law restates 1:12; DPI Japan may carry position material. |
| 15 | INT | EN | co2 | WFOT OR COTEC occupational therapy environmental accessibility ramp position statement | Likely nothing gradient-specific; attempt recorded either way. |
| 16 | UK | EN | co1 | wheelchair user experience ramp gradient survey participatory research disabled people | The surprise case: a participatory study. I do not expect one. |

**Two things this plan commits me to in advance.** (a) Any number I meet gets traced to its warrant
before admission; if the warrant is a code, the source is evidence of uptake, not of the value.
(b) Every execution is logged, zero-yield included, with R14's four-way diagnosis stated:
genuine absence / wrong index / query-shape failure / retrieval failure.
