# Per-query priors — written BEFORE each query is fired (R8)

Batch-level priors P1–P4 are in `priors.md`, committed at 4f053bc. These are the per-query
expectations, committed before the first archive query runs. Engine names are the instrument;
the point of this batch is that none of them has been fired on this slug before.

| # | Target | Engine | Prior, before running |
|---|---|---|---|
| Q1 | Elmer C. D. (1957), *A study to determine the specifications of wheelchair ramps* | archive (HathiTrust/IA/Open Library) | Locatable to a bibliographic record at p~0.6; this is the oldest and most likely to be a university thesis or an institutional report. Full text p~0.3. If it IS the 1:12 measurement, it will state a slope in degrees or a ratio for a named wheelchair population. |
| Q2 | Walter F. (1971), *Four architectural movement studies… Part 3 – Ramp gradients* | archive (HathiTrust/IA/Open Library) | Locatable p~0.65 — a UK polytechnic/DoE research report, the kind that reaches national library catalogues. Full text p~0.25. Title names the parameter outright, so if retrieved it almost certainly states gradients; whether it *recommends* one is the open question. |
| Q3 | van der Voordt (1981), *Accessibility by means of ramps – Some research data from the Netherlands* | archive + NL repository | Locatable p~0.7 — van der Voordt is a named TU Delft academic with an institutional repository. Highest chance of full text of the five, p~0.5. Expect measured data; expect it to be about Dutch practice rather than a universal maximum. |
| Q4 | Steinfeld E. (1979), *Accessible buildings for people with walking and reaching limitations* | archive / NARIC REHABDATA | Locatable p~0.75 — Steinfeld is a major, well-indexed figure (IDEA Center). This is likely a HUD or federal report. It is the most likely single item to be the proximate source the US codes drew on. |
| Q5 | The 1:12 provenance question, asked directly of the archive layer | web/archive | This is the synthesis query, not an item retrieval. Prior: I expect to find *secondary* accounts attributing 1:12 to mid-century US work (Nugent / University of Illinois, ANSI A117.1 1961) more readily than a primary measurement. That asymmetry is itself the finding P2 predicts. |
| Q6 | REF-01002 (Vredenburgh 2009) — two previously unattempted routes only | archive | p~0.2 of full text, per P4. **Two routes, then stop.** A second null here is a predicted result, not new work, and will be reported as such. |

**Screen discipline:** any relevance count in this batch names a screen from
`governance/mining-screens.yaml` and is derived by `scripts/research/mining_screen.py`. No inline
regex (owner rule, 2026-09-18 22:55).
