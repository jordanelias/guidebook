# FDR Findings — visual-fire-alarm-seizure-safety
**Slug:** `visual-fire-alarm-seizure-safety`
**Topic directory:** `sensory-environment`
**FDR run date:** 2026-04-08
**Status:** COMPLETE — 2 scenarios complete; diminishing return gate applied
**Sources:** NFPA 72 (2016 revision; flash rate standard); Epilepsy Foundation PSE guidance; PMC11872230 (PSE guidelines gap analysis, Tier 2); Wikipedia PSE article; NKyTribune fire alarm PSE; Birket strobe vs epilepsy analysis; Angelini PSE triggers

---

## FDR-VFA-01 — d570 + photosensitive epilepsy → visual fire alarm (flash rate, synchronisation)

**Sources:** NFPA 72 (2016 revision lowered max from 3Hz to 2Hz); Epilepsy Foundation PSE; Birket DMX strobe analysis; PMC11872230 (Tier 2)

| Parameter | Value | Condition | Source | Tier | Delta |
|---|---|---|---|---|---|
| Visual fire alarm flash rate — maximum | ≤2 Hz (2 flashes per second) maximum single strobe; ≤2 Hz composite rate when multiple strobes visible simultaneously | PSE: seizures most commonly triggered at 3–30 Hz; NFPA 72 2016 revision specifically lowered from 3 Hz to 2 Hz to ensure composite rate of two adjacent synchronised strobes does not exceed 4 Hz | NFPA 72 (2016); Birket analysis; Epilepsy Foundation | Tier 5–6/Tier 2 | CONFIRMS visual alarm; **NOVEL** — 2 Hz specific maximum and composite rate reasoning absent from BPC |
| Strobe synchronisation — adjacent units | All visible strobe units in same space or sightline must be synchronised to same flash cycle; avoid independent flash patterns | PSE: two unsynchronised strobes at 2 Hz each produce an apparent composite rate of 4 Hz — within seizure-provocative range; synchronisation prevents additive rate | NFPA 72 §18.5.4.3; Birket | Tier 5–6 | **NOVEL** — synchronisation requirement with PSE-specific additive-rate rationale absent from BPC |
| Excluded flash rate range | Strobe flash rate must not fall within 3–70 Hz range in any operational mode including activation bursts | PSE: 3–30 Hz is peak seizure-provocative range; 30–70 Hz can still provoke responses in highly sensitive individuals; rates outside this range are substantially safer | NKyTribune PSE fire alarm; PMC11872230 | Tier 2/Co-2 | **NOVEL** — excluded range specification absent from BPC |
| Distance attenuation — placement | Strobe units positioned to keep photosensitive viewer ≥3m from unit where possible; effect diminishes with distance | PSE: distance significantly reduces risk; close-range high-intensity strobe (<1m) is substantially more provocative than distant strobe at same flash rate | Epilepsy Foundation; NKyTribune; Birket | Co-2/Tier 2 | **NOVEL** — minimum distance specification for PSE safety absent from BPC |

---

## FDR-VFA-02 — d570 + photosensitive epilepsy → general lighting and environmental flash sources

| Parameter | Value | Condition | Source | Tier | Delta |
|---|---|---|---|---|---|
| Fluorescent lighting — PSE interaction | Mains-powered fluorescent at 50/60Hz mains (100/120Hz flicker) is above PSE provocative range; LED replacement at >3000Hz PWM eliminates risk | PSE: legacy fluorescent flicker at 100/120Hz is above 3–30Hz peak range and generally safe; however LED with low-frequency PWM dimming can introduce flicker in provocative range — specify high-frequency PWM or DC-driven LED | Wikipedia PSE; PMC11872230 | Tier 2 | **NOVEL** — PWM dimming as LED-specific PSE flash risk absent from BPC |
| High-contrast patterns — visual environment | Avoid large-area high-contrast regular patterns (stripes >1 cycle/degree at high contrast) on walls, floors, or ceilings | PSE: stationary high-contrast patterns trigger seizures in ~30% of PSE individuals; architectural patterns (feature walls, tile patterns, cladding) are an underrecognised PSE trigger | PMC5438467 (gamma oscillations PSE, Tier 2) | Tier 2 | **NOVEL** — architectural pattern contrast as PSE environmental trigger absent from BPC |
