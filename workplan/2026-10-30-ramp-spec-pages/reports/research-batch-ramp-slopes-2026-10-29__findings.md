# Research batch: ramp slopes (E-03), 2026-10-29

Status: INGESTED 2026-10-29 (migration `data_20261030003751_2026-10-29-ramp-slopes-research-batch.sql`) and reflected in `data/spec_pages/E-03.json` / `site/specs/e-03.html`. Not committed. Every item below is
unreviewed. Literature items were read at **abstract level only** (Consensus free tier, no full text).
Jurisdiction items were read from the **primary document text** unless marked otherwise.

Targets, from the stress-test report (§10): the three E-03 jurisdictions with "values not retrieved" (SG, CN, IE) and
the evidence gaps for cervical SCI, fatigue-limited and ambulant-aid users.

## 1. Jurisdiction values (primary documents)

### IE: Technical Guidance Document M, *Access and Use*, 2022 edition (gov.ie) — PRIMARY-VERIFIED
Source: https://assets.gov.ie/static/documents/technical-guidance-document-m-access-and-use-2022.pdf
(text extracted with pdftotext; clause numbers as printed; page numbers not captured). The 2010 edition is withdrawn
(document states it "ceases to" apply).

- 1.1.3.4: ramp = gradient 1:20 or steeper. Preferred max 1:20. Ramps "not steeper than 1:12 may be provided if
  individual flights are not longer than 2000 mm".
- Table 2 (limits for ramp gradients and lengths): going <= 10 m -> 1:20, max rise 500 mm; <= 5 m -> 1:15, 333 mm;
  <= 2 m -> 1:12, 166 mm. Interpolation permitted between 2 m and 10 m.
- Clear width between walls/upstands/kerbs >= 1500 mm; width between handrails >= 1200 mm; handrails both sides.
- Top and bottom landings >= 1800 x 1800 mm, clear of door swings. Intermediate landings >= 1500 mm long; 1800 x 1800 mm
  passing places if the far end is not visible or the ramp has 3+ flights.
- Edge protection: upstand >= 100 mm high on any open side.
- A **stepped route must also be provided where ramp rise > 300 mm**. Stated reason: some people find steps easier than
  ramps (certain walking-aid users, older people, people with vision impairment).
- Alternative access (platform lift) where total rise > 2000 mm. Stated reason: "Ramps simply become too tiring for
  wheelchair users beyond this height."
- 2.1.3.4 (existing buildings, relaxations): 1:12 flights up to 4500 mm (interpolate from 1:20 at 10 m); handrail-to-handrail
  width >= 1000 mm; top/bottom landing >= 1500 x 1500 mm; intermediate landing >= 1000 mm.

Note for the page: the stepped-route-in-addition rule is evidence that the standard itself treats the ramp as unsuitable
for some groups. It belongs in the "specific group" tier (ambulant aid users, older people, vision impairment), not in
the universal tier.

### SG: Code on Accessibility in the Built Environment 2019 (BCA) — PRIMARY-VERIFIED
Source: https://isomer-user-content.by.gov.sg/338/57384a60-c5ce-4c3e-a621-1709f60ce428/accessibilitycode2019.pdf
(linked from the BCA Code page). Table row alignment read from a layout-mode text extraction.

- 4.5.1, Table 4 (changes in level, gradient not steeper than): rise 0-15 mm 1:2; >15-50 mm 1:5; >50-200 mm 1:10;
  **> 200 mm 1:12**. Row alignment inferred from order; confirm against the page image. It matches the 1995 BFA Code's
  1:2 / 1:5 / 1:10 / 1:12 bands.
- 4.6.2 gradient: must meet Table 4 and be consistent between landings. Cross-fall equal or gentler than 1:40. Curved
  ramps avoided; if used, 1:16 or gentler.
- Width: >= 1200 mm clear unless on an accessible route (then clause 4.2.1).
- 4.6.5.2 landings: level platform >= 1500 mm at top and bottom of each run and at direction changes. Maximum horizontal
  run between landings (Table 5): 1:12 -> 6 m; 1:14 -> 9 m; 1:15 -> 11 m; 1:20 -> 15 m; 1:25 or gentler -> 18 m; linear
  interpolation between. No more than 4 runs (3 intermediate landings). Landings not required at 1:25 or gentler.
- 4.5.2: rises 15-200 mm need contrasting colour or a contrasting band at top and bottom.
- A 2025 edition exists (https://go.gov.sg/bca-coa2025, public consultation 30 Dec 2024 to 27 Jan 2025). **Not read.** The
  status of 2019 versus 2025 must be settled before this goes on a page.
- Kerb ramps: not steeper than 1:10; flared sides not steeper than 1:10.

### CN: GB 50763-2012, *Codes for Accessibility Design* — PARTIAL, unofficial translation
Source: ChineseStandard.net English translation (61 pages). **The preview omits the body of 3.4 "Wheelchair Ramp"**: the
text jumps from 3.1 to 3.5. The main ramp gradient table is therefore NOT retrieved.

Values that were readable:
- 3.1.2 kerb ramps: full-width one-way ramp <= 1:20; three-way ramp front and side <= 1:12; other kerb ramps <= 1:12.
- 4.4.2 ramps at pedestrian overpasses/underpasses: clear width >= 2.00 m; gradient <= 1:12; intermediate platform
  >= 2.00 m deep for each 1.50 m of rise; arc-shaped ramps measured on the inner arc edge.
- Garden bridge: gradient below 8 %, width >= 1.20 m.
- Status from the translation: issued 20 Mar 2012 (the web summary said 30 Mar), implemented 1 Sep 2012. The date
  conflict is unresolved.

Open: obtain clause 3.4 (gradient vs. height/length table, landings). Needs the official text or a purchased copy.
Do not fill 3.4 from memory.

## 2. Literature found (abstract-level; none are in `evidence_sources`)

All twelve checked by author/year/title against the DB: **0 present**.

| # | Citation | Design / n | Finding relevant to E-03 | Population |
|---|----------|-----------|--------------------------|------------|
| 1 | Chow et al. 2009, Arch Phys Med Rehabil | 10 men, paraplegia; 0-12 deg | Major stroking changes and significantly more muscle activity between 4 and 10 deg | manual wheelchair, paraplegia |
| 2 | Hashizume et al. 2015, Stud Health Technol Inform | 5 cervical SCI; 5-12.5 % | Normalised power 0.23 / 0.24 / 0.26 W/kg at 5 / 6.7 / 8.3 %; wide between-subject differences in ability to climb | manual wheelchair, **cervical SCI** |
| 3 | Bertocci et al. 2018, Disabil Rehabil Assist Technol | 7 able-bodied novices; 3.5 / 9.5 / 15 deg | Peak resultant force 107 N to 230 N from 3.5 to 15 deg | proxy only (not wheelchair users) |
| 4 | Choi et al. 2015, J Phys Ther Sci | 24 healthy adults | 1:12 and 1:10 suitable; 1:6 raises blood pressure | proxy only |
| 5 | Lenker et al. 2016, J Public Transp | 27 (manual, power, cane/vision) | 1:8 and 1:12 usable for most; 1:4 unsafe; many manual users lacked strength | mixed; small n; no scooter/ambulation-aid users |
| 6 | Pierret et al. 2014, Appl Ergon | 25 paraplegic; cross-slope 0-12 % | 2 % acceptable, 8 % critical; strain linear | **cross-slope**, not running slope |
| 7 | Flemmer et al. 2026, Disabil Rehabil Assist Technol | mechanical model | critical cross-slope about 3 % at zero running slope | cross-slope; modelling |
| 8 | Har-Nir et al. 2022, Eur J Phys Rehabil Med | 18 pwMS vs 23 controls, treadmill | Uphill is the most demanding task; perceived effort higher than energy expenditure suggests | **MS, ambulant** |
| 9 | Liu et al. 2023, Geriatr Nurs | 26 older adults, cane vs rolling walker | Gait differs by device on incline; walker gait changes up vs down, cane does not | **older adults, walking aids** |
| 10 | Leone et al. 2016, Neurorehab Neural Repair | 208 pwMS, 6MWT | 31 % overall show walking-related motor fatigue; up to about 51 % at EDSS 6.5 | MS, fatigue (context for endurance limits) |
| 11 | Lay et al. 2005, J Biomech | 9 healthy; -39 to +39 % | Hip and knee joint-moment demand change non-uniformly up/down slope | proxy only |
| 12 | Jahanian et al. 2022, J Biomech | 7 SCI; geared wheels, one ramp | Low gear lowers peak force on a ramp | SCI; intervention study |

Other results not tabulated: Hong 2026 (older adults, downhill 5/10/15 deg, higher lateral instability), Yalcin 2026
(transtibial prosthesis, ramp ascent raises asymmetry), Persine 2023 and Hisano 2026 (cross-slope prosthesis), Xie 2024
(pedestrian speed on slopes).

## 3. What this batch does and does not change

Moves:
- E-03 jurisdiction roster: IE and SG move from "values not retrieved" to primary-read; CN stays partial.
- The cervical-SCI gap now has one directly relevant study (Hashizume 2015, n = 5, 5-12.5 %), abstract-level only and too
  small to set a threshold. It does not close the gap; it confirms between-person variability.
- Ambulant-aid and MS groups gain support (items 8, 9, 5, plus IE 1.1.3.4's own stepped-route rule). Still no study sets a
  slope limit for them.
- Several results show effects across ramp slopes but none yields a safe-gradient threshold for any group. That matches
  the stress-test conclusion: the 1:12 value remains a regulatory floor, not an evidence-derived optimum.

Does not move:
- Items 3, 4, 11 use healthy proxies. They must not be tagged as wheelchair-user evidence for a threshold.
- Cross-slope papers (6, 7) belong to the cross-slope item, not E-03 running slope.
- No full texts were read for the literature. Study sizes and findings are from abstracts.

## 4. Proposed next steps (not done)
1. Ingest items 1-12 through `add-source` with `review_status UNREVIEWED`, then tag population/ICF/need.
2. Update the SG, IE and CN entries in `data/spec_pages/E-03.json`, with verification level "primary" for IE and SG.
3. Resolve SG 2019 vs 2025 and obtain GB 50763 clause 3.4.
4. Pull full texts for Chow 2009, Hashizume 2015 and Lenker 2016.

## 5. Applied 2026-10-29 (after owner direction)
- Owner direction applied: current editions only, so Singapore was re-read from the **2025 Code (v1.1)**, not 2019. Section 1's Singapore
  block above is the 2019 reading and is superseded by REF-00751 and the E-03 entry (rise threshold 175 mm, Table 5 runs 6/9/12/15/18 m at
  1:12/1:14/1:16/1:20/1:24). T4-T6 values are accepted as the baseline; no search for their derivation.
- Ingested: REF-00738..REF-00749 (12 studies, UNVERIFIED-1, AUTHOR-TITLE-ONLY, no DOI), REF-00750 (IE TGD M 2022), REF-00751 (SG Code 2025
  ramps). 50 tags, all UNREVIEWED: 14 population, 24 ICF, 12 need. Healthy-proxy studies (REF-00740, 00741, 00748) carry no population tag.
- Known data gap: REF-00074 (SG 2025) stores a URL that points to the 2019 PDF.
